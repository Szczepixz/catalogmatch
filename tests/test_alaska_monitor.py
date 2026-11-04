"""Offline tests using only invented monitor sources, attributes and annotations."""

import contextlib
import gzip
import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

import alaska_monitor as loader


class SyntheticArchive(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.path = Path(tmp.name) / "synthetic.tar.gz"

    def write(self, extra=None, er=None):
        files = {
            f"monitor/monitor_specs/invented/{i:03}.json": b'{"model":[" X-01/EU ","X-01/US"]}'
            for i in range(1, 7)
        }
        pairs = [(54, 1), (54, 1), (63, 1), (54, 2), (32, 3), (205, 4), (9, 5), (9, 99)]
        files[loader.GT] = er if er is not None else (
            "entity_id,spec_id\n" + "".join(f"ENTITY#{e:03},invented//{r:03}\n" for e, r in pairs)
        ).encode()
        files.update(extra or {})
        with tarfile.open(self.path, "w:gz") as tar:
            for name, payload in files.items():
                member = tarfile.TarInfo(name)
                member.size = len(payload)
                tar.addfile(member, io.BytesIO(payload))

    def cli(self):
        out = io.StringIO()
        with patch.object(sys, "argv", ["alaska_monitor", str(self.path)]), contextlib.redirect_stdout(out):
            status = loader.main()
        return status, out.getvalue()

    def test_views(self):
        self.write()
        ds = loader.prepare(self.path)
        self.assertEqual(ds.records["invented//005"]["model"], [" X-01/EU ", "X-01/US"])
        self.assertEqual(ds.assignments[:2], [("ENTITY#054", "invented//001")] * 2)
        self.assertEqual(ds.candidates, [("ENTITY#009", "invented//005")])
        self.assertEqual(ds.report["issues"], {
            "duplicate_assignments": [["ENTITY#054", "invented//001", 2]],
            "missing_records": ["invented//099"],
            "multiple_memberships": {"invented//001": ["ENTITY#054", "ENTITY#063"]},
        })
        self.assertEqual(ds.report["quarantine"]["membership_conflicts"]["records"], 2)
        first = self.cli()
        self.assertEqual(first, self.cli())
        self.assertEqual(first[0], 0)
        self.assertEqual(json.loads(first[1]), ds.report)

    def assert_failure(self):
        code, output = self.cli()
        self.assertEqual(code, 1)
        report = json.loads(output)
        self.assertEqual(set(report), {"status", "error"})
        self.assertEqual(report["status"], "error")

    def test_limits(self):
        self.write()
        for limit in ("MAX_FILE", "MAX_MEMBERS", "MAX_TAR", "MAX_ARCHIVE"):
            with self.subTest(limit=limit), patch.object(loader, limit, 1):
                self.assert_failure()

    def test_corrupt_or_missing_archive(self):
        self.assert_failure()
        self.write()
        original = self.path.read_bytes()
        for bad in (original[:-4], gzip.compress(b"broken tar"), b"broken gzip"):
            self.path.write_bytes(bad)
            self.assert_failure()

    def test_format_errors(self):
        for extra, er in [
            ({"../escape": b"x"}, None),
            ({"monitor/monitor_specs/invented/007.json": b"[]"}, None),
            ({"monitor/monitor_specs/invented/007.json": b"{"}, None),
            ({}, b"wrong,header\n"),
            ({}, b"entity_id,spec_id\ninvalid\n"),
        ]:
            with self.subTest(extra=list(extra), er=er):
                self.write(extra, er)
                self.assert_failure()
