"""Offline structural preparation of ALASKA Monitor source annotations."""

import argparse
from collections import Counter, defaultdict
import csv
from dataclasses import dataclass
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import tarfile
import zlib


MIB = 1024 * 1024
MAX_ARCHIVE = 8 * MIB
MAX_TAR = 128 * MIB
MAX_MEMBERS = 25_000
MAX_FILE = MIB
GT = "monitor/monitor_ground_truths/monitor_entity_resolution_gt.csv"
SCHEMA = "monitor/monitor_ground_truths/monitor_schema_matching_gt.csv"
SPEC = re.compile(r"monitor/monitor_specs/([^/#]+)/([0-9]+)\.json")
KNOWN_CONFLICTS = {"ENTITY#054", "ENTITY#063"}
PILOT_DISPUTES = {"ENTITY#032", "ENTITY#205"}


class InvalidInput(ValueError):
    """A reportable structural failure with no usable partial result."""


@dataclass
class Dataset:
    records: dict  # source//id -> original JSON object
    assignments: list  # ordered (entity_id, spec_id) pairs, including duplicates
    candidates: list  # distinct, resolvable assignments for subsequent review
    report: dict


def unique_keys(items):
    result = {}
    for key, value in items:
        if key in result:
            raise InvalidInput("duplicate JSON attribute")
        result[key] = value
    return result


def invalid_constant(value):
    raise InvalidInput("invalid JSON number")


def read_members(data):
    records = {}
    rows = None
    seen = set()
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:") as archive:
        for index, member in enumerate(archive, 1):
            name = member.name
            if index > MAX_MEMBERS or not 0 <= member.size <= MAX_FILE:
                raise InvalidInput("tar member limit exceeded")
            if name in seen or any(p in {"", ".", ".."} for p in name.split("/")) or "\\" in name:
                raise InvalidInput("duplicate or unsafe archive path")
            seen.add(name)
            if member.isdir():
                continue
            if member.type not in (tarfile.REGTYPE, tarfile.AREGTYPE) or member.sparse is not None:
                raise InvalidInput("unsupported archive member type")
            payload = archive.extractfile(member).read()
            match = SPEC.fullmatch(name)
            if match:
                locator = "//".join(match.groups())
                try:
                    obj = json.loads(payload.decode("utf-8"), object_pairs_hook=unique_keys, parse_constant=invalid_constant)
                    if not isinstance(obj, dict):
                        raise InvalidInput("expected JSON object")
                except (ValueError, RecursionError) as exc:
                    raise InvalidInput(f"invalid JSON record at {locator}") from exc
                records[locator] = obj
            elif name == GT:
                rows = []
                reader = csv.reader(io.StringIO(payload.decode("utf-8"), newline=""), strict=True)
                if next(reader, None) != ["entity_id", "spec_id"]:
                    raise InvalidInput("invalid ER header")
                for row in reader:
                    if (len(row) != 2 or not re.fullmatch(r"ENTITY#[0-9]+", row[0])
                            or not re.fullmatch(r"[^/#]+//[0-9]+", row[1])):
                        raise InvalidInput(f"invalid ER assignment at line {reader.line_num}")
                    rows.append(tuple(row))
            elif name != SCHEMA:
                raise InvalidInput("unrecognized data member")
        end = archive.offset
        if len(data) < end + 1024 or any(memoryview(data)[end:]):
            raise InvalidInput("invalid tar ending")
    if rows is None or not records:
        raise InvalidInput("missing ER table or records")
    return records, rows


def prepare(path):
    with Path(path).open("rb") as stream:
        compressed = stream.read(MAX_ARCHIVE + 1)
    if len(compressed) > MAX_ARCHIVE:
        raise InvalidInput("compressed size limit exceeded")
    with gzip.GzipFile(fileobj=io.BytesIO(compressed)) as stream:
        data = stream.read(MAX_TAR + 1)
    if len(data) > MAX_TAR:
        raise InvalidInput("decompressed size limit exceeded")
    records, rows = read_members(data)
    frequencies = Counter(rows)
    groups = defaultdict(set)
    membership = defaultdict(set)
    for entity, record in frequencies:
        groups[entity].add(record)
        membership[record].add(entity)
    conflicts = {r: sorted(es) for r, es in membership.items() if len(es) > 1}
    structural = KNOWN_CONFLICTS.union(*(conflicts.values()))
    missing = sorted(membership.keys() - records.keys())
    excluded = structural | PILOT_DISPUTES
    candidates = sorted((e, r) for e, r in frequencies if e not in excluded and r in records)

    def quarantine(entities):
        present = entities.intersection(groups)
        return {"entities": sorted(present), "records": len(set().union(*(groups[e] for e in present)))}

    report = {
        "status": "ok", "sha256": hashlib.sha256(compressed).hexdigest(),
        "counts": {"archive_bytes": len(compressed), "records": len(records),
                   "sources": len({r.split("//")[0] for r in records}), "er_rows": len(rows),
                   "unique_assignments": len(frequencies), "duplicate_rows": len(rows) - len(frequencies),
                   "labeled_records": len(membership), "entities": len(groups),
                   "candidate_assignments": len(candidates)},
        "issues": {"duplicate_assignments": [[e, r, n] for (e, r), n in sorted(frequencies.items()) if n > 1],
                   "multiple_memberships": conflicts, "missing_records": missing},
        "quarantine": {"membership_conflicts": quarantine(structural),
                       "ai_assisted_pilot_disputes": quarantine(PILOT_DISPUTES)},
    }
    return Dataset(records, rows, candidates, report)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    try:
        report = prepare(args.archive).report
    except (OSError, EOFError, tarfile.TarError, ValueError, csv.Error, zlib.error) as exc:
        message = str(exc) if isinstance(exc, InvalidInput) else f"cannot read archive ({type(exc).__name__})"
        print(json.dumps({"status": "error", "error": message}, sort_keys=True))
        return 1
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
