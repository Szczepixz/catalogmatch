"""Replay F1 observations and adjudications without inferring catalog identities."""

import argparse
from collections import defaultdict
import csv
import hashlib
import io
import json
from pathlib import Path
import sys
import tarfile
import zlib

from alaska_monitor import InvalidInput, prepare, unique_keys
from diagnostic_pairs import select


DATA = Path(__file__).parent / "docs/data"
LABELS = {"same_variant", "different_variant", "insufficient_evidence"}
REVIEW_FIELDS = ["id", "eligibility_left", "eligibility_right", "judgment",
                 "rationale", "reviewer_origin"]
KEY_FIELDS = ["id", "original_id", "first_judgment"]
MAX_INPUT = 4 * 1024 * 1024


def digest(payload):
    return hashlib.sha256(payload).hexdigest()


def require(condition, message):
    if not condition:
        raise InvalidInput(message)


def read_input(path, expected=None, normalize_lf=False):
    with Path(path).open("rb") as stream:
        payload = stream.read(MAX_INPUT + 1)
    require(len(payload) <= MAX_INPUT, "ledger input exceeds size limit")
    if normalize_lf:
        payload = payload.replace(b"\r\n", b"\n")
    require(expected is None or digest(payload) == expected, "ledger input checksum mismatch")
    return payload


def read_json(payload):
    return json.loads(payload.decode("utf-8-sig"), object_pairs_hook=unique_keys)


def read_csv(payload, fields):
    reader = csv.DictReader(io.StringIO(payload.decode("utf-8-sig"), newline=""), strict=True)
    require(reader.fieldnames == fields, "unexpected CSV header")
    rows = {}
    for row in reader:
        require(set(row) == set(fields) and all(isinstance(v, str) and v.strip()
                                              for v in row.values()), "incomplete CSV row")
        require(row["id"] not in rows, "duplicate CSV ID")
        if fields == REVIEW_FIELDS:
            require(row["judgment"] in LABELS, "unsupported review judgment")
            # This importer deliberately accepts the preserved AI worksheets only.
            require(row["reviewer_origin"] == "AI", "unsupported reviewer origin")
            require(all(row[f"eligibility_{side}"] == "eligible" for side in ("left", "right")),
                    "unexpected eligibility in pinned review")
        else:
            require(row["first_judgment"] in LABELS, "unsupported key judgment")
        rows[row["id"]] = row
    require(bool(rows), "empty CSV")
    return rows


def check_mapping(first, second, key, excluded):
    require(set(second) == set(key), "second review/key ID mismatch")
    require(set(excluded) <= set(first), "unknown excluded review ID")

    def rank(kind, pair_id):
        return digest(f"f1-r14-v1|{kind}|{pair_id}".encode("utf-8"))

    chosen = [i for i, row in first.items() if row["judgment"] == "same_variant"]
    for label in ("different_variant", "insufficient_evidence"):
        pool = [i for i, row in first.items() if row["judgment"] == label and i not in excluded]
        require(len(pool) >= 5, "insufficient masked controls")
        chosen.extend(sorted(pool, key=lambda i: (rank("control", i), i))[:5])
    order = sorted(chosen, key=lambda i: (rank("order", i), i))
    require(set(key) == {f"R{n:03}" for n in range(1, len(order) + 1)}, "review packet size mismatch")
    for n, pair_id in enumerate(order, 1):
        row = key[f"R{n:03}"]
        require(row["original_id"] == pair_id and row["first_judgment"] == first[pair_id]["judgment"],
                "private mapping disagrees with deterministic review packet")
    return {row["original_id"]: review_id for review_id, row in key.items()}


def observation(row, pair_id, name, revision):
    return {"event_id": f"{name}:{pair_id}", "kind": "observation", "revision": revision, "date": None,
            "review_id": row["id"], "input": f"{name}_review", "policy": "monitor-identity-v1",
            "origin": row["reviewer_origin"], "judgment": row["judgment"],
            "eligibility_left": row["eligibility_left"], "eligibility_right": row["eligibility_right"],
            "rationale_sha256": digest(row["rationale"].encode("utf-8"))}


def pair_history(pair, first, second, adjudications, revisions):
    pair_id = pair["id"]
    events = [observation(first, pair_id, "first", revisions["first"])]
    if second is not None:
        events.append(observation(second, pair_id, "second", revisions["second"]))
    for event in adjudications:
        require(event["left"] == pair["left"] and event["right"] == pair["right"],
                "adjudication orientation mismatch")
        require(event["judgment"] in LABELS and event["origin"] == "AI-assisted",
                "unsupported adjudication category")
        require(event["policy"] in {"monitor-identity-v1", "monitor-identity-v1.1"},
                "unsupported adjudication policy")
        require(bool(event["reason"]) and bool(event["evidence_reference"]), "missing adjudication evidence")
        events.append(dict(event, kind="adjudication"))
    events.sort(key=lambda event: event["revision"])
    require(len({e["revision"] for e in events}) == len(events), "ambiguous event order")
    require(len({e["event_id"] for e in events}) == len(events), "duplicate event ID")
    current = events[0]["judgment"]
    basis = events[0]["event_id"]
    for previous, event in zip(events, events[1:]):
        if event["kind"] == "adjudication":
            require(event["supersedes"] == previous["event_id"], "broken adjudication supersession")
            current = event["judgment"]
            basis = event["event_id"]
        elif event["judgment"] != current:
            current = "insufficient_evidence"
            basis = "unresolved_review_disagreement"
        elif previous["kind"] == "observation":
            basis = "review_consensus"
    return {**pair, "events": events, "current_judgment": current, "current_basis": basis}


def exposure_report(dataset, pilot, manifest, additional_holds):
    groups = defaultdict(set)
    membership = defaultdict(set)
    for entity, record in dataset.assignments:
        require(record in dataset.records, "assignment references missing record")
        groups[entity].add(record)
        membership[record].add(entity)
    parent = {e: e for e in groups}

    def root(entity):
        while parent[entity] != entity:
            parent[entity] = parent[parent[entity]]
            entity = parent[entity]
        return entity

    def join(entities):
        roots = sorted({root(e) for e in entities})
        for e in roots[1:]:
            parent[e] = roots[0]

    links = []
    for record, entities in sorted(membership.items()):
        if len(entities) > 1:
            join(entities)
            links.append({"reason": "shared_membership", "records": [record], "entities": sorted(entities)})
    duplicates = defaultdict(list)
    for record in sorted(membership):
        payload = json.dumps(dataset.records[record], sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        duplicates[digest(payload.encode("utf-8"))].append(record)
    for records in duplicates.values():
        entities = {e for record in records for e in membership[record]}
        if len(records) > 1:
            join(entities)
            links.append({"reason": "exact_object_duplicate", "records": records, "entities": sorted(entities)})

    exposed = set(pilot["semantically_inspected_source_entities"])
    diagnostic = {e for p in manifest["pairs"] for e in p["entities"]}
    require(exposed | diagnostic <= set(groups), "unknown exposed group")
    holds = defaultdict(list)
    for reason, quarantine in dataset.report["quarantine"].items():
        for e in quarantine["entities"]:
            holds[e].append(reason)
    for e, reason in additional_holds.items():
        require(e in groups, "unknown held group")
        holds[e].append(reason)
    components = defaultdict(list)
    for e in sorted(groups):
        components[root(e)].append(e)
    blocks = []
    for entities in sorted(components.values()):
        records = sorted({r for e in entities for r in groups[e]})
        seeds = sorted(set(entities) & (exposed | diagnostic))
        held = sorted(set(entities) & set(holds))
        blocks.append({"block_id": entities[0], "entities": entities, "records": records,
                       "exposure_seeds": seeds, "development_only": bool(seeds),
                       "held_entities": held, "automatic_identity_release_blocked": bool(held)})
    return {"groups": [{"entity": e, "records": sorted(groups[e]),
                         "exposure_reasons": (["pilot"] if e in exposed else []) +
                         (["diagnostic"] if e in diagnostic else []), "hold_reasons": sorted(holds.get(e, []))}
                        for e in sorted(groups)],
            "blocks": blocks, "links": links,
            "semantic_alias_review": "not_performed; blocks are not certified identities or test eligibility",
            "counts": {"source_groups": len(groups), "directly_exposed_groups": len(exposed | diagnostic),
                       "exposed_groups_after_propagation": sum(len(b["entities"]) for b in blocks if b["development_only"]),
                       "held_groups": len(holds), "assigned_records": len(membership)}}


def identity_warnings(pairs, exposure):
    """Report evidence conflicts; never output identity membership or release approval."""
    parent = {r: r for p in pairs for r in (p["left"], p["right"])}

    def root(record):
        while parent[record] != record:
            record = parent[record]
        return record

    for p in pairs:
        if p["current_judgment"] == "same_variant":
            parent[root(p["right"])] = root(p["left"])
    held = {g["entity"] for g in exposure["groups"] if g["hold_reasons"]}
    positives = defaultdict(list)
    conflicts = []
    for p in pairs:
        if p["current_judgment"] == "same_variant":
            for e in set(p["entities"]):
                positives[e].append(p)
        elif root(p["left"]) == root(p["right"]):
            conflicts.append(p["id"])
    return {"positive_pairs_in_held_groups": sorted(p["id"] for p in pairs
                if p["current_judgment"] == "same_variant" and held.intersection(p["entities"])),
            "disconnected_positive_pairs_by_source_group": {e: sorted(p["id"] for p in ps)
                for e, ps in sorted(positives.items()) if len({root(p["left"]) for p in ps}) > 1},
            "nonpositive_edges_inside_positive_components": sorted(conflicts),
            "identity_release": "not_attempted; positive connectivity is not identity validation"}


def build_ledger(dataset, pilot, manifest, first, second, key, config):
    pairs = manifest["pairs"]
    require(len({p["id"] for p in pairs}) == len(pairs), "duplicate manifest pair ID")
    require(set(first) == {p["id"] for p in pairs}, "first review/manifest ID mismatch")
    require(dataset.report["sha256"] == manifest["archive_sha256"] == pilot["archive_sha256"]
            == config["archive_sha256"], "archive provenance mismatch")
    assignments = set(dataset.assignments)
    for p in pairs:
        require(p["left"] != p["right"] and len(p["entities"]) == 2, "invalid pair endpoints")
        require(all((e, p[side]) in assignments for e, side in zip(p["entities"], ("left", "right"))),
                "manifest orientation/assignment mismatch")
    mapping = check_mapping(first, second, key, config["excluded_second_review_ids"])
    adjudications = defaultdict(list)
    for event in config["adjudications"]:
        require(event["pair_id"] in first, "unknown adjudicated pair")
        for side in ("left", "right"):
            fields = event["evidence_fields"][side]
            require(bool(fields) and event[side] in dataset.records and
                    all(field in dataset.records[event[side]] for field in fields),
                    "adjudication evidence field missing")
        adjudications[event["pair_id"]].append(event)
    histories = [pair_history(p, first[p["id"]], second[mapping[p["id"]]] if p["id"] in mapping else None,
                              adjudications[p["id"]], config["review_revisions"])
                 for p in sorted(pairs, key=lambda p: p["id"])]
    counts = {label: sum(p["current_judgment"] == label for p in histories) for label in sorted(LABELS)}
    require(counts == config["expected_counts"], "adjudicated tally mismatch")
    exposure = exposure_report(dataset, pilot, manifest, config["additional_holds"])
    return {"schema_version": 1, "policy": config["policy"], "status": "ok",
            "scope": "AI-assisted diagnostic ledger; not a catalog, split or gold set",
            "provenance": {"archive_sha256": config["archive_sha256"], **config["input_sha256"]},
            "counts": counts, "pairs": histories, "exposure": exposure, "source_structure": dataset.report,
            "identity_warnings": identity_warnings(histories, exposure)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("first_review", type=Path)
    parser.add_argument("second_review", type=Path)
    parser.add_argument("key", type=Path)
    args = parser.parse_args()
    try:
        config_bytes = read_input(DATA / "alaska-monitor-adjudications.json", normalize_lf=True)
        config = read_json(config_bytes)
        require(config["schema_version"] == 1, "unsupported ledger configuration")
        paths = {"manifest": DATA / "alaska-monitor-diagnostic.json", "pilot": DATA / "alaska-monitor-pilot.json",
                 "first_review": args.first_review, "second_review": args.second_review, "key": args.key}
        inputs = {name: read_input(path, config["input_sha256"][name], normalize_lf=name in {"pilot", "manifest"})
                  for name, path in paths.items()}
        manifest, pilot = read_json(inputs["manifest"]), read_json(inputs["pilot"])
        dataset = prepare(args.archive)
        require(select(dataset, pilot) == manifest, "diagnostic manifest replay mismatch")
        ledger = build_ledger(dataset, pilot, manifest,
                              read_csv(inputs["first_review"], REVIEW_FIELDS),
                              read_csv(inputs["second_review"], REVIEW_FIELDS),
                              read_csv(inputs["key"], KEY_FIELDS), config)
        ledger["provenance"]["adjudications_sha256"] = digest(config_bytes)
        ledger["provenance"]["hash_encoding"] = "public JSON: CRLF normalized to LF; archive and private CSV: exact bytes"
        print(json.dumps(ledger, indent=2, ensure_ascii=True))
        return 0
    except (OSError, EOFError, tarfile.TarError, zlib.error, ValueError, KeyError, TypeError, csv.Error) as exc:
        # Do not echo paths, raw CSV fields or parser excerpts into logs.
        message = str(exc) if isinstance(exc, InvalidInput) else "invalid or unreadable ledger input"
        print(json.dumps({"status": "error", "error": message}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
