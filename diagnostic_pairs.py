"""Select the fixed F1 diagnostic sample or emit a source-label-free worksheet."""
import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

from alaska_monitor import prepare

PILOT = Path(__file__).parent / "docs/data/alaska-monitor-pilot.json"
SEED = "f1-diagnostic-v1"
STRATA = ("within_sparse", "between_title_overlap", "within_general")


def rank(*parts):
    return hashlib.sha256("\0".join((SEED, *parts)).encode()).digest()


def select(dataset, pilot):
    if dataset.report["sha256"] != pilot["archive_sha256"]:
        raise ValueError("archive differs from audited pilot input")
    prior = {tuple(sorted((p["left"], p["right"]))) for p in pilot["pairs"]}
    exposed = {record for pair in prior for record in pair}
    seen_groups = set(pilot["semantically_inspected_source_entities"])
    groups = {record: entity for entity, record in dataset.candidates}
    tokens = {r: set(re.findall(r"[a-z0-9]+", str(dataset.records[r].get("<page title>", "")).lower()))
              for r in groups}
    used = set()
    rows = []
    for stratum in STRATA:
        count = 0
        anchors = sorted(groups, key=lambda r: rank(stratum, r))
        if stratum == "within_sparse":
            anchors.sort(key=lambda r: len(dataset.records[r]))
        for left in anchors:
            if left in used:
                continue
            partners = []
            for right in groups:
                if right in used or left.partition("//")[0] == right.partition("//")[0]:
                    continue
                if (groups[left] == groups[right]) != (stratum != "between_title_overlap"):
                    continue
                if tuple(sorted((left, right))) in prior:
                    continue
                score = 0
                if stratum == "between_title_overlap":
                    overlap = tokens[left] & tokens[right]
                    if not overlap:
                        continue
                    score = len(overlap) / len(tokens[left] | tokens[right])
                partners.append((-score, rank(stratum, left, right), right))
            if not partners:
                continue
            right = min(partners)[2]
            used.update((left, right))
            rows.append(dict(left=left, right=right, stratum=stratum,
                             source_label=int(groups[left] == groups[right]),
                             entities=[groups[left], groups[right]],
                             pilot_record=[r in exposed for r in (left, right)],
                             pilot_entity=[groups[r] in seen_groups for r in (left, right)]))
            count += 1
            if count == 40:
                break
        if count != 40:
            raise ValueError(f"unfilled stratum {stratum}")
    rows.sort(key=lambda p: rank("order", p["left"], p["right"]))
    for i, row in enumerate(rows, 1):
        row["id"] = f"D{i:03}"
    return dict(seed=SEED, archive_sha256=dataset.report["sha256"],
                quarantine=dataset.report["quarantine"], pairs=rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--worksheet", action="store_true")
    args = parser.parse_args()
    sample = select(prepare(args.archive), json.loads(PILOT.read_text(encoding="utf-8")))
    if args.worksheet:
        fields = ["id", "left", "right", "eligibility_left", "eligibility_right",
                  "judgment", "rationale", "reviewer_origin"]
        writer = csv.DictWriter(sys.stdout, fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(sample["pairs"])
    else:
        print(json.dumps(sample, indent=2))


if __name__ == "__main__":
    main()
