"""Offline tests with an invented catalog, targets and source locators."""

from contextlib import redirect_stdout
from copy import deepcopy
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from alaska_monitor import InvalidInput
from development_baseline import evaluate, evaluate_query, main, prepare_inputs, publish_report
from deterministic_baseline import normalize, rank


class DevelopmentBaselineTests(unittest.TestCase):
    def setUp(self):
        self.identities = [
            {"identity_id": "invented-A", "reference": "fixture-a//1",
             "queries": ["fixture-other//1", "fixture-other//2"], "pair_ids": ["fixture-pair"]},
            {"identity_id": "invented-B", "reference": "fixture-a//2",
             "queries": ["fixture-other//3"], "pair_ids": ["D112"]},
        ]
        self.records = {
            "fixture-a//1": {"<page title>": "alpha catalogue monitor blue"},
            "fixture-a//2": {"<page title>": "delta display"},
            "fixture-other//1": {"<page title>": "alpha catalogue blue wide"},
            "fixture-other//2": {"<page title>": "wrong alpha"},
            "fixture-other//3": {"<page title>": "delta display widescreen"},
        }
        for index, title in enumerate(["wrong", "wrong display", "wrong display bundled"]
                                      + [f"filler{n}" for n in range(10)], start=3):
            locator = f"fixture-a//{index}"
            self.records[locator] = {"<page title>": title}
            self.identities.append({"identity_id": f"invented-{index}", "reference": locator,
                                    "queries": [], "pair_ids": []})

    def test_full_catalog_and_wrong_first_result_with_micro_macro_and_sensitivity(self):
        references, queries, mapping = prepare_inputs(self.identities, self.records)
        results = evaluate(references, queries, mapping)
        for variant in results["variants"].values():
            self.assertEqual(variant["comparisons"], 45)
            for row in variant["queries"]:
                self.assertEqual(len(row["ranking"]), 15)
                self.assertEqual({candidate["handle"] for candidate in row["ranking"]}, set(references))
            failure = next(row for row in variant["queries"] if row["locator"] == "fixture-other//2")
            self.assertEqual(failure["target_rank"], 4)
            self.assertFalse(failure["top_1_hit"])
            self.assertEqual(failure["recall_hits"], {"1": False, "3": False, "5": True, "15": True})
            metrics = variant["metrics"]
            self.assertEqual(metrics["micro"]["top_1"]["fraction"], "2/3")
            self.assertEqual(metrics["micro"]["recall_at_3"]["fraction"], "2/3")
            self.assertEqual(metrics["micro"]["recall_at_5"]["numerator"], 3)
            self.assertEqual(metrics["micro"]["recall_at_15"]["denominator"], 3)
            self.assertEqual(metrics["per_identity"]["invented-A"]["top_1"]["denominator"], 2)
            self.assertEqual(metrics["macro"]["top_1"]["fraction"], "3/4")
            self.assertEqual(metrics["macro"]["top_1"]["identities"], 2)
            self.assertEqual(variant["sensitivity"]["target_rank"], 1)
            sensitivity = variant["sensitivity"]["without_query"]
            self.assertEqual(sensitivity["micro"]["top_1"]["fraction"], "1/2")
            self.assertEqual(sensitivity["macro"]["top_1"]["identities"], 1)
            self.assertEqual(sensitivity["macro"]["top_1"]["fraction"], "1/2")

    def test_projection_and_rank_ignore_metadata_and_source_locators(self):
        references, queries, mapping = prepare_inputs(self.identities, self.records)
        changed = deepcopy(self.identities[::-1])
        records = {}
        forbidden = dict(identifier_key="ANNOTATED", identity_id="untrusted", source_entities=["leaky"],
                         evidence_fields=["secret"], owner_review={"score": 100}, current_judgment="same_variant",
                         reason="fixture", reference_information={"identifier": ["secret"]},
                         development_only=True, held_entities=["fixture"], locator="leaky", host="leaky")
        for identity in changed:
            identity["identity_id"] += "-renamed"
            identity["reference"] = "renamed-" + identity["reference"]
            identity["queries"] = ["renamed-" + locator for locator in reversed(identity["queries"])]
        for locator, fields in self.records.items():
            records["renamed-" + locator] = {**forbidden, **fields}
        new_refs, new_queries, new_mapping = prepare_inputs(changed, records)
        self.assertNotEqual(mapping, new_mapping)
        self.assertEqual((references, queries), (new_refs, new_queries))

        def ranks(refs, requests):
            catalog = {handle: normalize(value) for handle, value in refs.items()}
            return {handle: rank(normalize(value), catalog) for handle, value in requests.items()}

        self.assertEqual(ranks(references, queries), ranks(new_refs, new_queries))
        rerun = evaluate(dict(reversed(list(references.items()))), dict(reversed(list(queries.items()))), mapping)
        self.assertEqual(evaluate(references, queries, mapping), rerun)

    def test_rejects_overlapping_records_bad_candidates_and_targets(self):
        references, queries, mapping = prepare_inputs(self.identities, self.records)
        handle, info = next(iter(mapping["queries"].items()))
        catalog = {ref: normalize(value) for ref, value in references.items()}
        ranking = rank(normalize(queries[handle]), catalog)["T"]
        for bad in (ranking[:-1], ranking[:-1] + [ranking[0]], ranking[:-1] + [{"handle": "unknown"}]):
            with self.subTest(bad=len(bad)), self.assertRaisesRegex(InvalidInput, "candidate inventory"):
                evaluate_query(handle, info, bad, set(references), "T")
        with self.assertRaisesRegex(InvalidInput, "target"):
            evaluate_query(handle, dict(info, target="unknown"), ranking, set(references), "T")
        self.identities[0]["queries"] = [self.identities[0]["reference"]]
        with self.assertRaisesRegex(InvalidInput, "overlapping"):
            prepare_inputs(self.identities, self.records)

    def test_identical_empty_projections_are_distinct_ranked_entries(self):
        for locator in ("fixture-other//1", "fixture-a//1", "fixture-a//3"):
            self.records[locator] = {}
        references, queries, mapping = prepare_inputs(self.identities, self.records)
        self.assertEqual(len(references), 15)
        self.assertEqual(len(queries), 3)
        results = evaluate(references, queries, mapping)
        row = next(row for row in results["variants"]["T"]["queries"] if row["locator"] == "fixture-other//1")
        self.assertTrue(row["all_scores_zero"])
        self.assertEqual(row["target_score_tie_size"], 15)
        self.assertEqual(len(row["empty_union_candidates"]), 2)
        self.assertEqual(row["query_extraction"]["title"], "missing")

    def test_cli_rejects_bad_input_without_report_or_private_error_details(self):
        with TemporaryDirectory() as directory:
            folder = Path(directory)
            output = folder / "report.json"
            args = ["development_baseline", str(folder / "private-source"), "first", "second", "key",
                    "--manifest", "manifest", "--output", str(output)]
            for error in (InvalidInput("private-source: ledger input checksum mismatch"),
                          json.JSONDecodeError("malformed", "private text", 0)):
                stdout = io.StringIO()
                with (patch("sys.argv", args), patch("development_baseline.replay", side_effect=error),
                      redirect_stdout(stdout)):
                    self.assertEqual(main(), 1)
                self.assertFalse(output.exists())
                self.assertEqual(json.loads(stdout.getvalue()),
                                 {"status": "error", "error": "invalid or unreadable F2-D1 input"})

    def test_report_publication_is_exclusive_and_byte_stable(self):
        with TemporaryDirectory() as directory:
            first, second = (Path(directory) / f"{name}.json" for name in ("first", "second"))
            publish_report(first, {"test": 1, "example": 0})
            publish_report(second, {"example": 0, "test": 1})
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with self.assertRaises(FileExistsError):
                publish_report(first, {"test": 2})
            self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_failed_write_removes_only_the_new_partial_report(self):
        with TemporaryDirectory() as directory:
            report = Path(directory) / "report.json"
            with report.open("xb") as stream, patch.object(Path, "open") as open_path:
                def partial_write(payload):
                    stream.write(payload[:2])
                    raise OSError("invented write failure")

                open_path.return_value.write.side_effect = partial_write
                open_path.return_value.__exit__.side_effect = lambda *_: stream.close()
                with self.assertRaisesRegex(OSError, "write failure"):
                    publish_report(report, {"fixture": True})
                open_path.assert_called_once_with("xb")
            self.assertFalse(report.exists())
