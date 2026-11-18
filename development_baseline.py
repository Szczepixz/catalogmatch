"""Run the fixed, offline F2-D1 development ranking diagnostic."""

import argparse
from collections import Counter, defaultdict
import csv
from fractions import Fraction
from itertools import groupby
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tarfile
import zlib

from annotation_ledger import digest, replay, require
from deterministic_baseline import (HANDLE_VERSION, IDENTIFIER_FIELDS, VARIANTS, configuration,
                                    evidence_key, normalize, project, rank)
from development_identities import host, load_validated_manifest, object_hash


DEVELOPMENT_SHA256 = "d453ef90eeb92601e2b350d34e32d1dce523343941431579a931a3773d35b84a"
KS = (1, 3, 5, 15)
SENSITIVITY_PAIR = "D112"
SOURCE_FILES = ("alaska_monitor.py", "annotation_ledger.py", "deterministic_baseline.py",
                "development_baseline.py", "development_identities.py", "diagnostic_pairs.py")


def prepare_inputs(identities, records):
    """Keep evaluation labels and source locators outside the projected offers."""
    references, queries, mapping = {}, {}, {"catalog": {}, "queries": {}}
    locators = [locator for identity in identities for locator in (identity["reference"], *identity["queries"])]
    require(len(locators) == len(set(locators)), "duplicate or overlapping catalog/query locator")
    entries, handles, occurrences = {}, set(), Counter()
    for locator in sorted(locators):
        offer = project(records[locator])
        payload_hash = object_hash(offer)
        handle = object_hash([HANDLE_VERSION, offer, occurrences[payload_hash]])
        require(handle not in handles, "projected offer handle collision")
        occurrences[payload_hash] += 1
        handles.add(handle)
        entries[locator] = (handle, offer)

    for identity in identities:
        locator = identity["reference"]
        reference, reference_offer = entries[locator]
        references[reference] = reference_offer
        mapping["catalog"][reference] = {"locator": locator, "identity_id": identity["identity_id"]}
        for query_locator in identity["queries"]:
            require(host(locator) != host(query_locator), "query and target share a host")
            query, query_offer = entries[query_locator]
            queries[query] = query_offer
            mapping["queries"][query] = {
                "locator": query_locator,
                "target": reference,
                "identity_id": identity["identity_id"],
                "pair_ids": sorted(identity["pair_ids"]),
            }
    return references, queries, mapping


def extraction_status(features):
    return {"title": features["title_status"],
            **{name: status for name, (status, _) in features["identifiers"].items()}}


def availability(statuses):
    return {
        "records": len(statuses),
        "title": {state: sum(row["title"] == state for row in statuses.values())
                  for state in ("available", "missing", "empty")},
        "identifiers": {
            name: {state: sum(row[name] == state for row in statuses.values())
                   for state in ("available", "unavailable", "ambiguous")}
            for name in IDENTIFIER_FIELDS
        },
    }


def evaluate_query(handle, info, ranking, catalog_handles, variant):
    order = [candidate["handle"] for candidate in ranking]
    target = info["target"]
    require(len(order) == len(catalog_handles) and set(order) == catalog_handles,
            "ranking does not contain the complete candidate inventory")
    require(target in catalog_handles, "query target is outside the catalog")
    target_rank = order.index(target) + 1
    ties = []
    for _, group in groupby(ranking, key=lambda candidate: evidence_key(candidate, variant)):
        tied = [candidate["handle"] for candidate in group]
        if len(tied) > 1:
            ties.append(tied)
    return {
        "handle": handle,
        **info,
        "ranking": ranking,
        "target_rank": target_rank,
        "top_1_hit": target_rank == 1,
        "recall_hits": {str(k): target_rank <= k for k in KS},
        "tied_score_groups": ties,
        "target_score_tie_size": next((len(group) for group in ties if target in group), 1),
        "all_title_scores_zero": all(row["intersection"] == 0 for row in ranking),
        "all_scores_zero": all(evidence_key(row, variant) == (0, 0) for row in ranking),
        "empty_union_candidates": [row["handle"] for row in ranking if row["union"] == 0],
    }


def rate(numerator, denominator):
    value = Fraction(numerator) / denominator
    return {"numerator": numerator, "denominator": denominator, "fraction": str(value),
            "percent": round(float(value * 100), 6)}


def hit_rates(rows):
    return {
        "top_1": rate(sum(row["top_1_hit"] for row in rows), len(rows)),
        **{f"recall_at_{k}": rate(sum(row["recall_hits"][str(k)] for row in rows), len(rows)) for k in KS},
    }


def aggregate(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["identity_id"]].append(row)
    by_identity = {identity: hit_rates(group) for identity, group in sorted(grouped.items())}
    micro = hit_rates(rows)
    macro = {}
    for metric in micro:
        total = sum(Fraction(rates[metric]["numerator"], rates[metric]["denominator"])
                    for rates in by_identity.values())
        value = total / len(by_identity)
        macro[metric] = {
            **rate(value.numerator, value.denominator),
            "sum_identity_rates": str(total),
            "identities": len(by_identity),
        }
    return {"micro": micro, "per_identity": by_identity, "macro": macro}


def evaluate(references, queries, mapping):
    catalog = {handle: normalize(offer) for handle, offer in references.items()}
    query_features = {handle: normalize(offer) for handle, offer in queries.items()}
    statuses = {"catalog": {handle: extraction_status(features) for handle, features in catalog.items()},
                "queries": {handle: extraction_status(features) for handle, features in query_features.items()}}
    scored = {handle: rank(features, catalog) for handle, features in sorted(query_features.items())}
    catalog_handles = set(catalog)
    sensitivity = [handle for handle, info in mapping["queries"].items()
                   if SENSITIVITY_PAIR in info["pair_ids"]]
    require(len(sensitivity) == 1, "expected one D112 sensitivity query")
    sensitivity_handle = sensitivity[0]
    results = {}
    for variant in VARIANTS:
        rows = []
        for handle, rankings in scored.items():
            row = evaluate_query(handle, mapping["queries"][handle], rankings[variant], catalog_handles, variant)
            row["query_extraction"] = statuses["queries"][handle]
            rows.append(row)
        comparisons = sum(len(row["ranking"]) for row in rows)
        sensitivity_row = next(row for row in rows if row["handle"] == sensitivity_handle)
        without = [row for row in rows if row["handle"] != sensitivity_handle]
        results[variant] = {
            "queries": rows,
            "comparisons": comparisons,
            "metrics": aggregate(rows),
            "sensitivity": {"pair": SENSITIVITY_PAIR, "query_handle": sensitivity_handle,
                            "target_rank": sensitivity_row["target_rank"],
                            "only_query": hit_rates([sensitivity_row]),
                            "without_query": aggregate(without)},
            "diagnostics": {
                "queries_with_score_ties": sum(bool(row["tied_score_groups"]) for row in rows),
                "queries_with_target_tied": sum(row["target_score_tie_size"] > 1 for row in rows),
                "all_title_scores_zero_queries": sum(row["all_title_scores_zero"] for row in rows),
                "all_scores_zero_queries": sum(row["all_scores_zero"] for row in rows),
                "empty_union_comparisons": sum(len(row["empty_union_candidates"]) for row in rows),
            },
        }
    pairs = [candidate for rankings in scored.values() for candidate in rankings["T"]]
    return {
        "counts": {"input_queries": len(queries), "eligible_queries": len(queries),
                   "scored_queries": len(scored), "catalog_size": len(catalog),
                   "candidates_per_query": len(catalog)},
        "extraction_statuses": statuses,
        "availability": {pool: availability(entries) for pool, entries in statuses.items()},
        "identifier_effect": {
            "agreement_comparisons": sum(row["identifier_agreement"] for row in pairs),
            "comparisons": len(pairs),
            "namespace_comparisons": {
                name: dict(Counter(row["identifier_statuses"][name] for row in pairs))
                for name in IDENTIFIER_FIELDS
            },
            "queries_with_agreement": sum(any(row["identifier_agreement"] for row in rankings["T"])
                                          for rankings in scored.values()),
            "rankings_changed": sum(rankings["T"] != rankings["I+T"] for rankings in scored.values()),
            "queries": len(scored),
        },
        "variants": results,
    }


def code_provenance():
    directory = Path(__file__).resolve().parent

    def git(*args):
        return subprocess.check_output(["git", "--no-optional-locks", *args], cwd=directory,
                                       stderr=subprocess.DEVNULL).decode("ascii").strip()

    commit, dirty = None, None
    try:
        commit = git("rev-parse", "HEAD")
        dirty = bool(git("status", "--porcelain=v1", "--untracked-files=all", "--", *SOURCE_FILES))
    except (OSError, subprocess.CalledProcessError):
        pass
    return {"commit": commit, "ranking_source_dirty": dirty, "file_sha256": {
        name: digest((directory / name).read_bytes()) for name in SOURCE_FILES
    }}


def run(archive, first_review, second_review, key, manifest_path):
    dataset, ledger = replay(archive, first_review, second_review, key)
    manifest, counts, hashes = load_validated_manifest(manifest_path, dataset, ledger)
    require(hashes["current"] == DEVELOPMENT_SHA256, "expected the accepted F2-D1 development manifest")
    require((counts["identities"], counts["identity_members"], counts["references"], counts["queries"])
            == (15, 32, 15, 17), "unexpected F2-D1 catalog capacity")
    references, queries, mapping = prepare_inputs(manifest["identities"], dataset.records)
    config = {**configuration(), "recall_k": KS, "sensitivity_pair": SENSITIVITY_PAIR,
              "eligibility_policy": manifest["eligibility_policy"], "identity_policy": manifest["policy"],
              "reference_rule": manifest["reference_rule"]}
    provenance = {
        "inputs": ledger["provenance"],
        "development_manifest_sha256": hashes["current"],
        "owner_review_snapshot_v1_sha256": hashes["owner_review_snapshot_v1"],
        "canonical_ledger_sha256": object_hash(ledger),
        "ordered_mapping_sha256": object_hash(mapping),
        "projected_inputs_sha256": object_hash({"catalog": references, "queries": queries}),
        "configuration_sha256": object_hash(config),
        "derived_hash_encoding": "sorted-key compact ASCII JSON encoded as UTF-8",
        "code": code_provenance(),
        "python": {"implementation": platform.python_implementation(), "version": platform.python_version(),
                   "platform": sys.platform, "machine": platform.machine()},
    }
    return {
        "schema_version": 1,
        "status": "ok",
        "scope": "F2-D1 exposed, present-product development ranking",
        "decision_policy": "not_evaluated",
        "configuration": config,
        "provenance": provenance,
        "ordered_mapping": mapping,
        "annotation_scope": {"origin": manifest["origin"], "human_verified": manifest["human_verified"],
                             "owner_review_independent_blinded": manifest["owner_review"]["independent_blinded"]},
        "template_overlap_reviews": [
            {key: row[key] for key in ("members", "equal_fields", "common_fields", "decision")}
            for row in manifest["template_overlap_reviews"]
        ],
        **evaluate(references, queries, mapping),
    }


def publish_report(path, report):
    payload = (json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True) + "\n").encode("utf-8")
    stream = path.open("xb")
    try:
        with stream:
            stream.write(payload)
    except (OSError, KeyboardInterrupt):
        path.unlink()
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("archive", "first_review", "second_review", "key"):
        parser.add_argument(name, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if os.path.lexists(args.output):
        print(json.dumps({"status": "error", "error": "report path already exists"}))
        return 1
    try:
        report = run(args.archive, args.first_review, args.second_review, args.key, args.manifest)
    except (OSError, EOFError, tarfile.TarError, zlib.error, ValueError, KeyError, TypeError, csv.Error):
        print(json.dumps({"status": "error", "error": "invalid or unreadable F2-D1 input"}))
        return 1
    try:
        publish_report(args.output, report)
    except OSError:
        print(json.dumps({"status": "error", "error": "cannot publish report to a new path"}))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
