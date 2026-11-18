"""Synthetic membership validation; no restricted offers or semantic gold labels."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from alaska_monitor import Dataset, InvalidInput
from development_identities import (duplicate_groups, load_validated_manifest, object_hash, select_reference,
                                    template_overlaps, validate)


class IdentityTests(unittest.TestCase):
    def setUp(self):
        records, assignments, pairs, groups, blocks, reviews = {}, [], [], [], [], []
        for n in range(1, 5):
            pid, entity = f"D{n:03}", f"ENTITY#{1 if n == 2 else n:03}"
            locs = [f"invented-a//{n}", f"invented-b//{n}"]
            members = []
            for r in locs:
                records[r] = {"model": "X1" if n < 3 else f"X{n}", "invented": r}
                assignments.append((entity, r))
                members.append(dict(locator=r, source_entities=[entity], object_sha256=object_hash(records[r]),
                                    evidence_fields=["model"], identifier_key="brand|x1" if n < 3 else "brand|x4",
                                    eligibility="eligible", condition="unknown"))
            pairs.append(dict(id=pid, left=locs[0], right=locs[1], entities=[entity, entity],
                              current_judgment="same_variant", current_basis="review_consensus"))
            if n != 3:
                reviews.append(dict(pair_id=pid, pair_basis="review_consensus", members=members,
                                    status="deferred" if n == 4 else "confirmed_membership",
                                    finding="Invented review, not evidence about real products."))
        for entity in sorted({e for e, _ in assignments}):
            locs = sorted(r for e, r in assignments if e == entity)
            held = [entity] if entity == "ENTITY#003" else []
            groups.append(dict(entity=entity, hold_reasons=held))
            blocks.append(dict(block_id=entity, records=locs, development_only=True, held_entities=held))
        self.dataset = Dataset(records, assignments, assignments, {})
        self.ledger = dict(provenance={"archive_sha256": "synthetic"}, pairs=pairs,
                           exposure=dict(groups=groups, blocks=blocks))
        members = sorted(r for e, r in assignments if e == "ENTITY#001")
        reference, queries = select_reference(members, records)
        self.manifest = dict(schema_version=1, policy="monitor-identity-v1.1", eligibility_policy="D15-v1",
                             origin="AI-assisted", human_verified=False, scope="bounded-development-proposal",
                             provenance=self.ledger["provenance"], positive_pair_ids=[p["id"] for p in pairs],
                             held_entities=["ENTITY#003"], candidate_reviews=reviews,
                             alias_review=dict(scope_pair_ids=["D001", "D002", "D004"], origin="AI-assisted",
                                               comparison_count=3, same_identity_pairs=[["D001", "D002"]],
                                               unresolved_pairs=[], other_comparisons="distinct_complete_identifiers"),
                             identities=[dict(identity_id="DEV-1", pair_ids=["D001", "D002"], members=members,
                                              leakage_blocks=["ENTITY#001"], reference=reference, queries=queries)],
                             deferred=[dict(pair_id=p["id"], members=[p["left"], p["right"]], reason="Synthetic hold or uncertainty")
                                       for p in pairs[2:]], exact_duplicate_groups=[], template_overlap_reviews=[],
                             counts=dict(positive_pairs=4, reviewed_pairs=3, reviewed_records=6, identities=1,
                                         identity_members=4, references=1, queries=2, deferred_pairs=2,
                                         deferred_records=4, exact_duplicate_groups=0,
                                         exact_duplicate_excess_records=0, template_overlap_pairs=0))

    def test_valid_manifest_does_not_mutate_inputs(self):
        before = deepcopy((self.manifest, self.dataset, self.ledger))
        self.assertEqual(validate(self.manifest, self.dataset, self.ledger), self.manifest["counts"])
        self.assertEqual(before, (self.manifest, self.dataset, self.ledger))

    def test_rejects_membership_evidence_and_provenance_errors(self):
        for field, value in [("locator", "unreviewed//999"), ("source_entities", ["ENTITY#999"]),
                             ("object_sha256", "wrong"), ("evidence_fields", ["missing"]),
                             ("condition", "new"), ("eligibility", "excluded")]:
            with self.subTest(field=field):
                m = deepcopy(self.manifest)
                m["candidate_reviews"][0]["members"][0][field] = value
                with self.assertRaises(InvalidInput):
                    validate(m, self.dataset, self.ledger)
        m = deepcopy(self.manifest)
        m["provenance"] = {"archive_sha256": "wrong"}
        with self.assertRaisesRegex(InvalidInput, "provenance"):
            validate(m, self.dataset, self.ledger)

    def test_pair_positive_does_not_override_hold_or_unresolved_membership(self):
        m = deepcopy(self.manifest)
        m["candidate_reviews"][0]["status"] = "deferred"
        with self.assertRaisesRegex(InvalidInput, "unresolved identity"):
            validate(m, self.dataset, self.ledger)
        ledger = deepcopy(self.ledger)
        ledger["exposure"]["blocks"][0]["held_entities"] = ["ENTITY#999"]
        with self.assertRaisesRegex(InvalidInput, "eligible development"):
            validate(self.manifest, self.dataset, ledger)

    def test_nonpositive_internal_edge_blocks_identity(self):
        for judgment in ("different_variant", "insufficient_evidence"):
            ledger = deepcopy(self.ledger)
            ledger["pairs"].append(dict(id="D099", left="invented-a//1", right="invented-b//2",
                                        current_judgment=judgment))
            with self.subTest(judgment=judgment), self.assertRaisesRegex(InvalidInput, "nonpositive"):
                validate(self.manifest, self.dataset, ledger)

    def test_source_group_is_not_alias_evidence(self):
        m = deepcopy(self.manifest)
        m["alias_review"]["same_identity_pairs"] = []
        with self.assertRaisesRegex(InvalidInput, "shared identifier"):
            validate(m, self.dataset, self.ledger)
        m["alias_review"]["unresolved_pairs"] = [["D001", "D002"]]
        with self.assertRaisesRegex(InvalidInput, "merge lacks"):
            validate(m, self.dataset, self.ledger)

    def test_coverage_reference_and_duplicate_membership_failures(self):
        for change in ("missing_deferral", "extra_member", "duplicate_identity", "reference_as_query",
                       "wrong_basis", "missing_alias_comparison"):
            m = deepcopy(self.manifest)
            if change == "missing_deferral":
                m["deferred"].pop()
            elif change == "extra_member":
                m["identities"][0]["members"].append("unreviewed//999")
            elif change == "duplicate_identity":
                m["identities"].append(dict(m["identities"][0], identity_id="DEV-2"))
            elif change == "reference_as_query":
                m["identities"][0]["queries"].append(m["identities"][0]["reference"])
            elif change == "wrong_basis":
                m["candidate_reviews"][0]["pair_basis"] = "invented"
            else:
                m["alias_review"]["comparison_count"] = 2
            with self.subTest(change=change), self.assertRaises(InvalidInput):
                validate(m, self.dataset, self.ledger)

    def test_reference_maximizes_cross_source_queries_before_hash(self):
        records = {"a//1": {"v": 1}, "a//2": {"v": 2}, "b//1": {"v": 3}}
        self.assertEqual(select_reference(list(records), records), ("b//1", ["a//1", "a//2"]))
        records = {"a//1": {"v": 1}, "b//1": {"v": 2}}
        expected = min(records, key=lambda r: hashlib.sha256(f"f1-catalog-v1|reference|{r}".encode()).hexdigest())
        self.assertEqual(select_reference(list(reversed(records)), records)[0], expected)

    def test_exact_duplicates_collapse_and_do_not_create_queries(self):
        records = {"a//1": {"v": 1}, "b//1": {"v": 1}}
        self.assertEqual(select_reference(list(records), records), (None, []))
        self.assertEqual(duplicate_groups(records, records), [["a//1", "b//1"]])
        records.update({"c//1": {"v": 2}, "c//2": {"v": 2}})
        reference, queries = select_reference(list(records), records)
        self.assertEqual(len(queries), 1)
        self.assertNotEqual(records[reference], records[queries[0]])
        self.assertEqual(select_reference(["c//1", "c//2"], records), (None, []))

    def test_template_overlap_is_not_exact_duplicate(self):
        records = {"a//1": {"<page title>": "X1", "a": 1, "b": 2, "c": 3},
                   "b//1": {"<page title>": "X2", "a": 1, "b": 2, "c": 3}}
        self.assertEqual(duplicate_groups(records, records), [])
        self.assertEqual(template_overlaps(records, records),
                         [dict(members=["a//1", "b//1"], equal_fields=3, common_fields=3)])

    def test_information_breaks_capacity_ties_but_not_capacity_priority(self):
        records = {"a//1": {"v": 1}, "b//1": {"v": 2}}
        old, _ = select_reference(list(records), records)
        richer = next(r for r in records if r != old)
        information = {richer: {"identifier": ["v"], "size": ["v"]}, old: {"identifier": ["v"]}}
        self.assertEqual(select_reference(list(records), records, information)[0], richer)
        records["a//2"] = {"v": 3}
        information = {"a//1": {str(n): ["v"] for n in range(10)}}
        self.assertEqual(select_reference(list(records), records, information)[0], "b//1")

    def v2_manifest(self):
        m = deepcopy(self.manifest)
        m.update(schema_version=2, reference_rule="capacity-information-hash-v2",
                 reference_information={r: {"identifier": ["model"]} for r in m["identities"][0]["members"]},
                 owner_review=dict(origin="human-owner", independent_blinded=False,
                                   membership={i["identity_id"]: sorted(i["members"]) for i in m["identities"]},
                                   decision="confirm_membership_no_alias_noticed", reference_approval="not_provided",
                                   field_rationales="not_provided"))
        return m

    def test_v2_review_scope_and_information_evidence(self):
        m = self.v2_manifest()
        self.assertEqual(validate(m, self.dataset, self.ledger), m["counts"])
        for kind in ("field", "category", "membership", "claim"):
            bad = deepcopy(m)
            if kind == "field":
                bad["reference_information"]["invented-a//1"]["identifier"] = ["missing"]
            elif kind == "category":
                bad["reference_information"]["invented-a//1"]["verbosity"] = ["model"]
            elif kind == "membership":
                bad["owner_review"]["membership"]["DEV-1"].pop()
            else:
                bad["owner_review"]["independent_blinded"] = True
            with self.subTest(kind=kind), self.assertRaises(InvalidInput):
                validate(bad, self.dataset, self.ledger)

    def test_shared_loader_checks_snapshot_checksum_and_owner_membership_binding(self):
        current = self.v2_manifest()
        prior = deepcopy(self.manifest)
        with TemporaryDirectory() as directory, patch("development_identities.DATA", Path(directory)):
            prior_path = Path(directory) / "alaska-monitor-development-v1.json"
            current_path = Path(directory) / "current.json"

            def write_inputs():
                payload = json.dumps(prior).encode("utf-8")
                prior_path.write_bytes(payload)
                current["owner_review"]["reviewed_manifest_sha256"] = hashlib.sha256(payload).hexdigest()
                current_path.write_text(json.dumps(current), encoding="utf-8")

            write_inputs()
            loaded, counts, hashes = load_validated_manifest(current_path, self.dataset, self.ledger)
            self.assertEqual(loaded, current)
            self.assertEqual(counts, current["counts"])
            self.assertEqual(hashes["owner_review_snapshot_v1"], current["owner_review"]["reviewed_manifest_sha256"])
            prior_path.write_bytes(b"corrupted")
            with self.assertRaisesRegex(InvalidInput, "checksum"):
                load_validated_manifest(current_path, self.dataset, self.ledger)

            prior["identities"][0]["identity_id"] = "invented-different-membership-key"
            write_inputs()
            with self.assertRaisesRegex(InvalidInput, "differs from reviewed snapshot"):
                load_validated_manifest(current_path, self.dataset, self.ledger)


if __name__ == "__main__":
    unittest.main()
