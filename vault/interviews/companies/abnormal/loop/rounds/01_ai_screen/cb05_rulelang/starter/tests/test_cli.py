"""``python -m rulelang`` through ``cli.main``."""
from __future__ import annotations

import io

from rulelang.cli import main
from rulelang.config import FIXTURES_DIR


def _run(*argv):
    out = io.StringIO()
    code = main([str(a) for a in argv], out=out)
    return code, out.getvalue()


def test_run_then_signals(tmp_path):
    db = tmp_path / "r.db"
    code, text = _run("run", FIXTURES_DIR / "events", "--tenant", "acme", "--db", db)
    assert code == 0 and text.strip() == "processed 23 events, 10 signals (3 bad records skipped)"
    code, text = _run("signals", "a-011", "--tenant", "acme", "--db", db)
    assert code == 0
    assert "vendor_lookalike" in text and "imitates vendor acme-vendor.example" in text


def test_signals_for_unknown_event_exits_2(tmp_path):
    code, _ = _run("signals", "nope", "--tenant", "acme", "--db", tmp_path / "r.db")
    assert code == 2


def test_detectors_lists_dependencies():
    code, text = _run("detectors")
    assert code == 0 and "vendor_lookalike" in text and "(requires new_sender)" in text


def test_bad_tenant_config_exits_2(tmp_path):
    code, _ = _run("run", FIXTURES_DIR / "events", "--tenant", "../x", "--db", tmp_path / "r.db")
    assert code == 2
