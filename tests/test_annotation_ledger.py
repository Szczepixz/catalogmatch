"""Ledger checks use invented records and reviews, never the restricted archive."""

import contextlib
from copy import deepcopy
import csv
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from alaska_monitor import Dataset, InvalidInput
import annotation_ledger as ledger


def csv_bytes(rows, fields):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fields)
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.pairs, self.first, records, assignments = [], {}, {}, []
        for n in range(12):
            pair_id = f"D{n + 1:03}"
            left, right = f"invented-a//{n}", f"invented-b//{n}"
            entity = f"ENTITY#{n + 1:03}"
            self.pairs.append(dict(id=pair_id, left=left, right=right, entities=[entity, entity], source_label=1))
            for record in (left, right):
                records[record] = {"invented": record}
                assignments.append((entity, record))
            self.first[pair_id] = dict(id=pair_id, eligibility_left="eligible", eligibility_right="eligible",
                                      judgment="same_variant" if n < 2 else "different_variant" if n < 7
                                      else "insufficient_evidence", rationale="PRIVATE invented explanation",
                                      reviewer_origin="AI")
        self.dataset = Dataset(records, assignments, assignments, {"sha256": "synthetic", "quarantine": {}})
        self.pilot = {"archive_sha256": "synthetic", "semantically_inspected_source_entities": []}
        self.manifest = {"archive_sha256": "synthetic", "pairs": self.pairs}
        order = sorted(self.first, key=lambda i: ledger.digest(f"f1-r14-v1|order|{i}".encode()))
        self.second, self.key = {}, {}
        for n, pair_id in enumerate(order, 1):
            review_id = f"R{n:03}"
            self.second[review_id] = dict(self.first[pair_id], id=review_id)
            self.key[review_id] = dict(id=review_id, original_id=pair_id,
                                      first_judgment=self.first[pair_id]["judgment"])
        self.config = dict(archive_sha256="synthetic", schema_version=1, policy="monitor-identity-v1.1",
                           excluded_second_review_ids=[], adjudications=[], additional_holds={}, input_sha256={},
                           review_revisions={"first": 12, "second": 15},
                           expected_counts=dict(same_variant=2, different_variant=5, insufficient_evidence=5))

    def build(self):
        return ledger.build_ledger(self.dataset, self.pilot, self.manifest, self.first,
                                   self.second, self.key, self.config)

    def event(self, revision, judgment, supersedes):
        return dict(event_id=f"r{revision}:D001", pair_id="D001", left=self.pairs[0]["left"],
                    right=self.pairs[0]["right"], revision=revision, date="2026-11-12",
                    policy="monitor-identity-v1.1", origin="AI-assisted", judgment=judgment,
                    reason="Invented adjudication", evidence_reference="synthetic evidence", supersedes=supersedes,
                    evidence_fields={"left": ["invented"], "right": ["invented"]})

    def test_observations_are_preserved_and_prose_is_not_exported(self):
        before = deepcopy((self.first, self.second, self.config, self.dataset.records))
        result = self.build()
        self.assertEqual(result, self.build())
        self.assertEqual(result["counts"], self.config["expected_counts"])
        self.assertEqual(before, (self.first, self.second, self.config, self.dataset.records))
        self.assertNotIn("PRIVATE", json.dumps(result))
        self.assertNotIn('"invented":', json.dumps(result))
        self.assertEqual(result["pairs"][0]["events"][0]["rationale_sha256"],
                         ledger.digest(b"PRIVATE invented explanation"))

    def test_disagreement_abstains_and_adjudication_keeps_history(self):
        review_id = next(k for k, row in self.key.items() if row["original_id"] == "D001")
        self.second[review_id]["judgment"] = "insufficient_evidence"
        self.config["expected_counts"].update(same_variant=1, insufficient_evidence=6)
        self.assertEqual(self.build()["pairs"][0]["current_basis"], "unresolved_review_disagreement")
        self.config["adjudications"] = [self.event(16, "insufficient_evidence", "second:D001"),
                                        self.event(17, "same_variant", "r16:D001")]
        self.config["expected_counts"].update(same_variant=2, insufficient_evidence=5)
        pair = self.build()["pairs"][0]
        self.assertEqual([e["judgment"] for e in pair["events"]],
                         ["same_variant", "insufficient_evidence", "insufficient_evidence", "same_variant"])
        self.assertEqual(pair["current_basis"], "r17:D001")

    def test_orientation_and_supersession_errors_are_rejected(self):
        self.config["adjudications"] = [self.event(16, "same_variant", "second:D001")]
        event = self.config["adjudications"][0]
        event["left"], event["right"] = event["right"], event["left"]
        with self.assertRaisesRegex(InvalidInput, "orientation"):
            self.build()
        event["left"], event["right"] = event["right"], event["left"]
        event["supersedes"] = "first:D001"
        with self.assertRaisesRegex(InvalidInput, "supersession"):
            self.build()
        event["supersedes"] = "second:D001"
        event["evidence_fields"]["left"] = ["missing field"]
        with self.assertRaisesRegex(InvalidInput, "evidence field"):
            self.build()

    def test_wrong_mapping_missing_ids_and_tally_rejected(self):
        original = deepcopy(self.key)
        self.key["R001"]["original_id"] = "D999"
        with self.assertRaisesRegex(InvalidInput, "mapping"):
            self.build()
        self.key = original
        self.config["expected_counts"]["same_variant"] = 99
        with self.assertRaisesRegex(InvalidInput, "tally"):
            self.build()
        del self.first["D012"]
        with self.assertRaisesRegex(InvalidInput, "ID mismatch"):
            self.build()

    def test_csv_failures_and_bom(self):
        rows = list(self.first.values())
        self.assertEqual(ledger.read_csv(b"\xef\xbb\xbf" + csv_bytes(rows, ledger.REVIEW_FIELDS),
                                         ledger.REVIEW_FIELDS), self.first)
        invalid = [rows + [rows[0]], [dict(rows[0], judgment="unknown")],
                   [dict(rows[0], rationale=" ")], [dict(rows[0], reviewer_origin="human")],
                   [dict(rows[0], eligibility_left="maybe")]]
        for variant in invalid:
            with self.subTest(variant=variant[-1]["id"]), self.assertRaises(InvalidInput):
                ledger.read_csv(csv_bytes(variant, ledger.REVIEW_FIELDS), ledger.REVIEW_FIELDS)
        for payload in [b"wrong,header\n", b"", csv_bytes([], ledger.REVIEW_FIELDS),
                        csv_bytes(rows, ledger.REVIEW_FIELDS) + b"D999,eligible\n"]:
            with self.assertRaises(InvalidInput):
                ledger.read_csv(payload, ledger.REVIEW_FIELDS)

    def test_group_hold_does_not_change_pair_and_disconnected_pairs_do_not_merge(self):
        second_group = self.pairs[1]["entities"][0]
        self.pairs[1]["entities"] = ["ENTITY#001", "ENTITY#001"]
        self.dataset.assignments = [("ENTITY#001" if e == second_group else e, r)
                                    for e, r in self.dataset.assignments]
        self.config["additional_holds"] = {"ENTITY#001": "synthetic hold"}
        result = self.build()
        self.assertEqual(result["counts"]["same_variant"], 2)
        self.assertEqual(result["identity_warnings"]["positive_pairs_in_held_groups"], ["D001", "D002"])
        self.assertEqual(result["identity_warnings"]["disconnected_positive_pairs_by_source_group"],
                         {"ENTITY#001": ["D001", "D002"]})
        self.assertTrue(result["exposure"]["blocks"][0]["automatic_identity_release_blocked"])

    def test_exposure_propagates_through_duplicate_objects_and_shared_membership(self):
        self.dataset.records["new//1"] = deepcopy(self.dataset.records[self.pairs[0]["left"]])
        self.dataset.assignments += [("ENTITY#100", "new//1"), ("ENTITY#101", "new//1")]
        report = self.build()["exposure"]
        self.assertEqual(report["counts"]["directly_exposed_groups"], 12)
        self.assertEqual(report["counts"]["exposed_groups_after_propagation"], 14)
        block = next(b for b in report["blocks"] if "ENTITY#100" in b["entities"])
        self.assertTrue(block["development_only"])
        self.assertEqual(block["entities"], ["ENTITY#001", "ENTITY#100", "ENTITY#101"])
        self.assertEqual({link["reason"] for link in report["links"]},
                         {"exact_object_duplicate", "shared_membership"})

    def test_negative_and_insufficient_edges_in_positive_chain_are_flagged(self):
        pairs = [dict(id="P1", left="a", right="b", entities=["E", "E"], current_judgment="same_variant"),
                 dict(id="P2", left="b", right="c", entities=["E", "E"], current_judgment="same_variant")]
        for label in ("different_variant", "insufficient_evidence"):
            with self.subTest(label=label):
                result = ledger.identity_warnings(pairs + [dict(id="P3", left="a", right="c",
                    entities=["E", "E"], current_judgment=label)], {"groups": []})
                self.assertEqual(result["nonpositive_edges_inside_positive_components"], ["P3"])
                self.assertIn("not_attempted", result["identity_release"])

    def test_cli_success_and_failure_emit_one_complete_document(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            payloads = {"pilot": json.dumps(self.pilot).encode(), "manifest": json.dumps(self.manifest).encode(),
                        "first_review": csv_bytes(self.first.values(), ledger.REVIEW_FIELDS),
                        "second_review": csv_bytes(self.second.values(), ledger.REVIEW_FIELDS),
                        "key": csv_bytes(self.key.values(), ledger.KEY_FIELDS)}
            names = {"pilot": "alaska-monitor-pilot.json", "manifest": "alaska-monitor-diagnostic.json",
                     "first_review": "first.csv", "second_review": "second.csv", "key": "key.csv"}
            for name, payload in payloads.items():
                (directory / names[name]).write_bytes(payload)
            self.config["input_sha256"] = {name: ledger.digest(payload) for name, payload in payloads.items()}
            (directory / "alaska-monitor-adjudications.json").write_text(json.dumps(self.config), encoding="utf-8")
            argv = ["annotation_ledger", "synthetic.tar.gz"] + [str(directory / names[k])
                    for k in ("first_review", "second_review", "key")]

            def run():
                out = io.StringIO()
                with patch.object(sys, "argv", argv), patch.object(ledger, "DATA", directory), \
                        patch.object(ledger, "prepare", return_value=self.dataset), \
                        patch.object(ledger, "select", return_value=self.manifest), contextlib.redirect_stdout(out):
                    status = ledger.main()
                return status, json.loads(out.getvalue())

            status, result = run()
            self.assertEqual(status, 0)
            self.assertEqual(result["counts"], self.config["expected_counts"])
            (directory / "first.csv").write_bytes(b"PRIVATE corrupted input")
            status, result = run()
            self.assertEqual(status, 1)
            self.assertEqual(result, {"status": "error", "error": "ledger input checksum mismatch"})
            with self.assertRaisesRegex(InvalidInput, "size limit"):
                with patch.object(ledger, "MAX_INPUT", 1):
                    ledger.read_input(directory / "first.csv")

    def test_public_newline_normalization_does_not_relax_private_checksums(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "synthetic.json"
            lf = b'{\n  "fixture": true\n}\n'
            path.write_bytes(lf.replace(b"\n", b"\r\n"))
            self.assertEqual(ledger.read_input(path, ledger.digest(lf), normalize_lf=True), lf)
            with self.assertRaisesRegex(InvalidInput, "checksum"):
                ledger.read_input(path, ledger.digest(lf))
            path.write_bytes(b'{\n  "fixture": false\n}\n')
            with self.assertRaisesRegex(InvalidInput, "checksum"):
                ledger.read_input(path, ledger.digest(lf), normalize_lf=True)


if __name__ == "__main__":
    unittest.main()
