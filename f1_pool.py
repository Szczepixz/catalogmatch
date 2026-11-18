"""Summarize the approved F1-S structural inventory from the pinned F1-L replay."""

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

from development_identities import host


def dispositions(ledger):
    exposure = ledger["exposure"]
    duplicate_key = {
        record: link["records"][0]
        for link in exposure["links"] if link["reason"] == "exact_object_duplicate"
        for record in link["records"]
    }
    for block in exposure["blocks"]:
        records = block["records"]
        hosts = {host(record) for record in records}
        objects = {duplicate_key.get(record, record) for record in records}
        if block["development_only"]:
            reason = "exposed"
        elif block["held_entities"]:
            reason = "held"
        elif len(hosts) < 2:
            reason = "single_host"
        elif len(objects) < 2:
            reason = "duplicate_only"
        else:
            reason = "included"
        yield block, reason, hosts


def summarize(ledger):
    totals = defaultdict(Counter)
    pool_hosts = set()
    overlap = 0
    for block, reason, hosts in dispositions(ledger):
        records = block["records"]
        if reason == "exposed":
            overlap += bool(block["held_entities"])
        if reason == "included":
            pool_hosts.update(hosts)
        totals[reason].update(blocks=1, groups=len(block["entities"]), records=len(records))
    return {"counts": totals, "also_held_among_exposed_blocks": overlap,
            "included_hosts": len(pool_hosts)}


def reservation(ledger, checksum):
    def rank(block):
        groups = ",".join(sorted(block["entities"]))
        return hashlib.sha256(("f1-split-v1|block|" + groups).encode()).hexdigest(), groups

    blocks = sorted((b for b, reason, _ in dispositions(ledger) if reason == "included"), key=rank)
    return {"protocol": "f1-split-v1", "ledger_sha256_lf": checksum, "blocks": [
        {"entities": block["entities"], "records": block["records"],
         "partition": "test" if index < len(blocks) // 3 else "development"}
        for index, block in enumerate(blocks)
    ]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--reservation", type=Path, help="Write a new private reservation manifest")
    args = parser.parse_args()
    data = args.ledger.read_bytes().replace(b"\r\n", b"\n")
    checksum = hashlib.sha256(data).hexdigest()
    if checksum != "30d4c163b7bca5d7c3d27008fc1b857f919de2dfb46db252cd1e5d9dc98e0470":
        parser.exit(1, "Unexpected F1-L ledger checksum.\n")
    ledger = json.loads(data)
    if args.reservation:
        payload = (json.dumps(reservation(ledger, checksum), sort_keys=True, indent=2) + "\n").encode()
        with args.reservation.open("xb") as stream:
            stream.write(payload)
        print(hashlib.sha256(payload).hexdigest())
    else:
        print(json.dumps(summarize(ledger), sort_keys=True, indent=2))
