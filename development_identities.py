"""Validate the bounded, AI-assisted F1-I membership and reference proposal."""

import argparse
import csv
import itertools
import json
from pathlib import Path
import sys
import tarfile
import zlib

from alaska_monitor import InvalidInput
from annotation_ledger import DATA, digest, read_input, read_json, replay, require


POLICY = "monitor-identity-v1.1"
INFORMATION_CATEGORIES = {"identifier", "size", "resolution", "panel", "touch",
                          "color", "refresh", "condition", "bundle", "coverage"}


def object_hash(value):
    return digest(json.dumps(value, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=True).encode("utf-8"))


def host(locator):
    return locator.split("//", 1)[0]


def select_reference(members, records, information=None):
    """Rank by query capacity, reviewed information category count, then fixed hash."""
    information = information or {}
    hashes = {r: object_hash(records[r]) for r in members}

    def queries(reference):
        representatives = {}
        for record in sorted(members):
            if host(record) != host(reference) and hashes[record] != hashes[reference]:
                representatives.setdefault(hashes[record], record)
        return sorted(representatives.values())

    ranked = sorted(members, key=lambda r: (-len(queries(r)), -len(information.get(r, {})),
                    digest(f"f1-catalog-v1|reference|{r}".encode("utf-8")), r))
    if not ranked or not queries(ranked[0]):
        return None, []
    return ranked[0], queries(ranked[0])


def duplicate_groups(locators, records):
    groups = {}
    for locator in sorted(locators):
        groups.setdefault(object_hash(records[locator]), []).append(locator)
    return [rs for _, rs in sorted(groups.items()) if len(rs) > 1]


def template_overlaps(locators, records):
    """Audit trigger only: >=90% equal values in >=3 common non-title fields."""
    overlaps = []
    for a, b in itertools.combinations(sorted(locators), 2):
        shared = (set(records[a]) & set(records[b])) - {"<page title>"}
        equal = sum(records[a][k] == records[b][k] for k in shared)
        if len(shared) >= 3 and equal / len(shared) >= 0.9:
            overlaps.append({"members": [a, b], "equal_fields": equal, "common_fields": len(shared)})
    return overlaps


def validate(manifest, dataset, ledger):
    """Check structural/evidence invariants; this cannot prove semantic annotations."""
    require(manifest["schema_version"] in {1, 2} and manifest["policy"] == POLICY
            and manifest["eligibility_policy"] == "D15-v1", "unsupported identity policy/schema")
    require(manifest["origin"] == "AI-assisted" and manifest["human_verified"] is False
            and manifest["scope"] == "bounded-development-proposal", "unsupported review scope/origin")
    require(manifest["provenance"] == ledger["provenance"], "identity provenance mismatch")
    positives = {p["id"]: p for p in ledger["pairs"] if p["current_judgment"] == "same_variant"}
    require(manifest["positive_pair_ids"] == sorted(positives), "positive scope mismatch")
    held = {g["entity"] for g in ledger["exposure"]["groups"] if g["hold_reasons"]}
    require(manifest["held_entities"] == sorted(held), "hold inventory mismatch")
    held_pairs = {i for i, p in positives.items() if held.intersection(p["entities"])}
    candidate_ids = sorted(set(positives) - held_pairs)
    candidate_records = {p[side] for i, p in positives.items() if i in candidate_ids
                         for side in ("left", "right")}
    reviews = manifest["candidate_reviews"]
    require([r["pair_id"] for r in reviews] == candidate_ids, "candidate review coverage mismatch")
    review_by_id = {r["pair_id"]: r for r in reviews}
    reviewed_records = {}
    assignments = set(dataset.assignments)
    for review in reviews:
        pair = positives[review["pair_id"]]
        require(review["pair_basis"] == pair["current_basis"], "pair assessment provenance mismatch")
        require(review["status"] in {"confirmed_membership", "deferred"}
                and bool(review["finding"]), "missing membership decision")
        require([m["locator"] for m in review["members"]] == [pair["left"], pair["right"]],
                "review endpoint orientation mismatch")
        for member in review["members"]:
            locator = member["locator"]
            require(member["source_entities"] == sorted({e for e, r in assignments if r == locator}),
                    "source membership mismatch")
            require(not held.intersection(member["source_entities"]), "held candidate membership")
            record = dataset.records[locator]
            require(member["object_sha256"] == object_hash(record), "record evidence checksum mismatch")
            require(member["eligibility"] == "eligible" and member["condition"] == "unknown",
                    "unsupported bounded eligibility/condition assessment")
            fields = member["evidence_fields"]
            require(bool(fields) and len(fields) == len(set(fields)) and all(f in record for f in fields),
                    "missing identity evidence fields")
            require(bool(member["identifier_key"]), "missing reviewed identifier")
            if locator in reviewed_records:
                require(reviewed_records[locator] == member, "inconsistent repeated member review")
            reviewed_records[locator] = member

    information = {}
    if manifest["schema_version"] == 2:
        require(manifest["reference_rule"] == "capacity-information-hash-v2", "unsupported reference rule")
        information = manifest["reference_information"]
        confirmed = {m["locator"] for r in reviews if r["status"] == "confirmed_membership"
                     for m in r["members"]}
        require(set(information) == confirmed, "reference information coverage mismatch")
        for locator, categories in information.items():
            require(bool(categories) and set(categories) <= INFORMATION_CATEGORIES,
                    "unsupported information category")
            for fields in categories.values():
                require(isinstance(fields, list) and bool(fields) and len(fields) == len(set(fields))
                        and all(f in dataset.records[locator] for f in fields),
                        "missing reference information evidence")
        review = manifest["owner_review"]
        membership = {i["identity_id"]: sorted(i["members"]) for i in manifest["identities"]}
        require(review["origin"] == "human-owner" and review["independent_blinded"] is False
                and review["membership"] == membership
                and review["decision"] == "confirm_membership_no_alias_noticed"
                and review["reference_approval"] == "not_provided"
                and review["field_rationales"] == "not_provided", "owner review scope mismatch")

    aliases = manifest["alias_review"]
    require(aliases["scope_pair_ids"] == candidate_ids and aliases["origin"] == "AI-assisted",
            "alias scope mismatch")
    merged = aliases["same_identity_pairs"]
    deferred_aliases = aliases["unresolved_pairs"]
    comparisons = {tuple(p) for p in itertools.combinations(candidate_ids, 2)}
    exceptions = [tuple(p) for p in merged + deferred_aliases]
    require(len(exceptions) == len(set(exceptions)) and set(exceptions) <= comparisons,
            "invalid alias comparisons")
    require(aliases["other_comparisons"] == "distinct_complete_identifiers"
            and aliases["comparison_count"] == len(comparisons), "incomplete alias review")
    for a, b in comparisons - set(exceptions):
        keys_a = {m["identifier_key"] for m in review_by_id[a]["members"]}
        keys_b = {m["identifier_key"] for m in review_by_id[b]["members"]}
        require(not keys_a.intersection(keys_b), "unreviewed shared identifier")

    identities = manifest["identities"]
    require(len({i["identity_id"] for i in identities}) == len(identities), "duplicate identity ID")
    released, assigned_pairs, references, queries = set(), {}, set(), set()
    for identity in identities:
        pair_ids = identity["pair_ids"]
        require(bool(pair_ids) and len(pair_ids) == len(set(pair_ids))
                and set(pair_ids) <= set(candidate_ids), "invalid identity pair IDs")
        require(all(review_by_id[p]["status"] == "confirmed_membership" for p in pair_ids),
                "unresolved identity membership")
        members = identity["members"]
        expected = {m["locator"] for p in pair_ids for m in review_by_id[p]["members"]}
        require(len(members) == len(set(members)) and set(members) == expected,
                "identity membership mismatch")
        require(not released.intersection(members), "record belongs to multiple identities")
        for p in pair_ids:
            require(p not in assigned_pairs, "pair belongs to multiple identities")
            assigned_pairs[p] = identity["identity_id"]
        for a, b in itertools.combinations(sorted(pair_ids), 2):
            require([a, b] in merged, "identity merge lacks explicit alias evidence")
        for pair in ledger["pairs"]:
            if pair["left"] in expected and pair["right"] in expected:
                require(pair["current_judgment"] == "same_variant", "nonpositive internal edge")
        blocks = [b for b in ledger["exposure"]["blocks"] if expected.intersection(b["records"])]
        require(blocks and all(b["development_only"] and not b["held_entities"] for b in blocks),
                "identity is not eligible development material")
        require(identity["leakage_blocks"] == sorted(b["block_id"] for b in blocks),
                "leakage block mismatch")
        reference, selected_queries = select_reference(members, dataset.records, information)
        require(reference is not None and identity["reference"] == reference
                and identity["queries"] == selected_queries, "reference/query rule mismatch")
        released.update(members)
        references.add(reference)
        queries.update(selected_queries)
    require(not references.intersection(queries), "reference/query overlap")
    for a, b in merged:
        require(a in assigned_pairs and assigned_pairs.get(a) == assigned_pairs.get(b),
                "established alias split between identities")
    for a, b in deferred_aliases:
        require(a not in assigned_pairs and b not in assigned_pairs, "unresolved alias released")

    deferred = manifest["deferred"]
    deferred_ids = [d["pair_id"] for d in deferred]
    require(len(deferred_ids) == len(set(deferred_ids)) and set(deferred_ids).isdisjoint(assigned_pairs)
            and set(deferred_ids) | set(assigned_pairs) == set(positives), "incomplete disposition")
    for item in deferred:
        p = positives[item["pair_id"]]
        require(item["members"] == [p["left"], p["right"]] and bool(item["reason"]),
                "invalid deferral")
        require(item["pair_id"] in held_pairs or review_by_id[item["pair_id"]]["status"] == "deferred"
                or select_reference(item["members"], dataset.records)[0] is None,
                "unsupported deferral")
    duplicates = duplicate_groups(candidate_records, dataset.records)
    require(manifest["exact_duplicate_groups"] == duplicates, "duplicate inventory mismatch")
    overlap_reviews = manifest["template_overlap_reviews"]
    require([{k: r[k] for k in ("members", "equal_fields", "common_fields")} for r in overlap_reviews]
            == template_overlaps(candidate_records, dataset.records), "template overlap coverage mismatch")
    require(all(r["decision"] in {"retain_correlated_cross_source_query", "different_models_shared_template"}
                and bool(r["reason"]) for r in overlap_reviews), "missing template overlap review")
    for group in duplicates:
        owners = {i["identity_id"] for i in identities if set(group).intersection(i["members"])}
        require(len(owners) <= 1, "exact duplicates split between identities")
    counts = {"positive_pairs": len(positives), "reviewed_pairs": len(reviews),
              "reviewed_records": len(candidate_records), "identities": len(identities),
              "identity_members": len(released), "references": len(references), "queries": len(queries),
              "deferred_pairs": len(deferred),
              "deferred_records": len({r for d in deferred for r in d["members"]}),
              "exact_duplicate_groups": len(duplicates),
              "exact_duplicate_excess_records": sum(len(g) - 1 for g in duplicates),
              "template_overlap_pairs": len(overlap_reviews)}
    require(manifest["counts"] == counts, "identity capacity mismatch")
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("archive", "first_review", "second_review", "key"):
        parser.add_argument(name, type=Path)
    parser.add_argument("--manifest", type=Path, default=DATA / "alaska-monitor-development.json")
    args = parser.parse_args()
    try:
        dataset, ledger = replay(args.archive, args.first_review, args.second_review, args.key)
        payload = read_input(args.manifest, normalize_lf=True)
        manifest = read_json(payload)
        if manifest["schema_version"] == 2:
            prior = read_json(read_input(DATA / "alaska-monitor-development-v1.json",
                                        manifest["owner_review"]["reviewed_manifest_sha256"], normalize_lf=True))
            validate(prior, dataset, ledger)
            require(manifest["owner_review"]["membership"] ==
                    {i["identity_id"]: sorted(i["members"]) for i in prior["identities"]},
                    "owner review differs from reviewed snapshot")
        counts = validate(manifest, dataset, ledger)
        print(json.dumps({"status": "ok", "manifest_sha256": digest(payload), "counts": counts,
                          "policy": POLICY, "origin": "AI-assisted", "human_verified": False}, indent=2))
        return 0
    except (OSError, EOFError, tarfile.TarError, zlib.error, ValueError, KeyError, TypeError, csv.Error) as exc:
        message = str(exc) if isinstance(exc, InvalidInput) else "invalid or unreadable identity input"
        print(json.dumps({"status": "error", "error": message}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
