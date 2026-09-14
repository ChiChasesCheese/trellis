"""pytest plugin: dump a one-shot run summary for the drill progress log.

Loaded by `drill.py test` / `loop/mock.py test` via `-p tools.pytest_progress`.
Writes JSON to the path in $DRILL_PROGRESS_OUT and does nothing when that env var
is unset, so the plugin is inert for ordinary `pytest` runs.
"""

from __future__ import annotations

import json
import os
import time

_PART_MARKERS = ("part1", "part2", "part3", "part4", "part5")


class _Collector:
    def __init__(self):
        self.t0 = time.time()
        self.totals = {"passed": 0, "failed": 0, "skipped": 0, "error": 0}
        self.parts: dict[str, dict[str, int]] = {}

    def record(self, report):
        if report.when == "call":
            outcome = report.outcome  # passed / failed / skipped
        elif report.when in ("setup", "teardown") and report.failed:
            outcome = "error"
        else:
            return
        self.totals[outcome] = self.totals.get(outcome, 0) + 1
        for name in _PART_MARKERS:
            if name in report.keywords:
                bucket = self.parts.setdefault(name, {"passed": 0, "failed": 0, "skipped": 0, "error": 0})
                bucket[outcome] = bucket.get(outcome, 0) + 1


_C = _Collector()


def pytest_runtest_logreport(report):
    if os.environ.get("DRILL_PROGRESS_OUT"):
        _C.record(report)


def pytest_sessionfinish(session, exitstatus):
    out = os.environ.get("DRILL_PROGRESS_OUT")
    if not out:
        return
    payload = {
        "passed": _C.totals["passed"],
        "failed": _C.totals["failed"],
        "skipped": _C.totals["skipped"],
        "error": _C.totals["error"],
        "duration": round(time.time() - _C.t0, 2),
        "parts": _C.parts,
        "exitstatus": int(exitstatus),
    }
    try:
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(payload, fh)
    except OSError:
        pass
