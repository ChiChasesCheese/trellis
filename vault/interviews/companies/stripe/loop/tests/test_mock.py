"""Tests for loop/mock.py. Builds a fake loop/rounds + loop/work tree under tmp_path and
monkeypatches mock.ROUNDS / mock.WORK so nothing here touches the real loop/ tree.

Run: rtk proxy python3 -m pytest loop/tests -q   (from the repo root, so `import mock` resolves
via the sys.path insertion below and the real root conftest.py is not required).
"""

from __future__ import annotations

import importlib.util
import json
import sys
import time
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MOCK_PY = REPO_ROOT / "loop" / "mock.py"

_spec = importlib.util.spec_from_file_location("loop_mock", MOCK_PY)
mock = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = mock
_spec.loader.exec_module(mock)


# ---------------------------------------------------------------------------
# fixture: fake rounds/ + work/ tree
# ---------------------------------------------------------------------------


@pytest.fixture
def tree(tmp_path, monkeypatch):
    rounds = tmp_path / "rounds"
    work = tmp_path / "work"
    rounds.mkdir()

    # ps01: phone-screen shaped item (problem.md + starter_template.py + solution.py)
    ps01 = rounds / "03_phone_screen" / "ps01_widget_levels"
    ps01.mkdir(parents=True)
    (ps01 / "problem.md").write_text("# Widget levels\n\nsome problem body.\n")
    (ps01 / "starter_template.py").write_text("def part1(lines):\n    raise NotImplementedError\n")
    (ps01 / "starter.py").write_text("STALE = True\n")  # should get overwritten by `start`
    (ps01 / "solution.py").write_text("def part1(lines):\n    return lines\n")

    # a second ps item to exercise ambiguity when someone types just "ps"
    ps02 = rounds / "03_phone_screen" / "ps02_other"
    ps02.mkdir(parents=True)
    (ps02 / "problem.md").write_text("# Other\n")

    # bs01: bug-squash shaped item (README.md + src/ + tests/ + solution/FIX.patch)
    bs01 = rounds / "04_bug_squash" / "bs01_calc"
    bs01.mkdir(parents=True)
    (bs01 / "README.md").write_text("# Calc bug\n\nrun the tests, find the bug.\n")
    (bs01 / "src" / "pkg").mkdir(parents=True)
    (bs01 / "src" / "pkg" / "__init__.py").write_text("")
    (bs01 / "src" / "pkg" / "calc.py").write_text("def add(a, b):\n    return a - b  # bug: should be +\n")
    (bs01 / "tests").mkdir()
    (bs01 / "tests" / "test_calc.py").write_text(
        "import sys, pathlib\n"
        "sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / 'src'))\n"
        "from pkg.calc import add\n\n"
        "def test_add():\n"
        "    assert add(2, 3) == 5\n"
    )
    (bs01 / "solution").mkdir()
    (bs01 / "solution" / "FIX.patch").write_text(
        "--- a/src/pkg/calc.py\n"
        "+++ b/src/pkg/calc.py\n"
        "@@ -1,2 +1,2 @@\n"
        " def add(a, b):\n"
        "-    return a - b  # bug: should be +\n"
        "+    return a + b\n"
    )

    # bs02: trivial 1-line-test bug-squash item, for the plain start/copy/run-pytest check
    bs02 = rounds / "04_bug_squash" / "bs02_trivial"
    bs02.mkdir(parents=True)
    (bs02 / "README.md").write_text("# Trivial\n")
    (bs02 / "tests").mkdir()
    (bs02 / "tests" / "test_trivial.py").write_text("def test_ok():\n    assert True\n")

    # sd01: system-design shaped item (prompt.md + rubric.md, no tests)
    sd01 = rounds / "07_system_design" / "sd01_ledger"
    sd01.mkdir(parents=True)
    (sd01 / "prompt.md").write_text("# Ledger service\n\ndesign a ledger.\n")
    (sd01 / "rubric.md").write_text("# Rubric\n\n- correctness\n- scalability\n")

    # int01: integration item with a mockserver metadata comment
    int01 = rounds / "05_integration" / "int01_bikemap"
    int01.mkdir(parents=True)
    (int01 / "problem.md").write_text("<!-- mockserver: maps -->\n# Bikemap\n\nbody.\n")

    # non-coding rounds: bank.json question banks
    for name, q in (
        ("01_recruiter", [{"round": "recruiter", "q": "Why Stripe?", "principle": "", "source": "x"}]),
        (
            "02_hm",
            [
                {"round": "hm", "q": "Tell me about a conflict.", "principle": "Move fast", "source": "y"},
                {"round": "hm", "q": "Biggest failure.", "principle": "Ownership", "source": "y"},
            ],
        ),
        (
            "08_behavioral",
            [
                {"round": "behavioral", "q": "STAR story 1", "principle": "User focus", "source": "z"},
                {"round": "behavioral", "q": "STAR story 2", "principle": "Simplify", "source": "z"},
                {"round": "behavioral", "q": "STAR story 3", "principle": "Rigor", "source": "z"},
            ],
        ),
    ):
        d = rounds / name
        d.mkdir(parents=True)
        (d / "bank.json").write_text(json.dumps(q))

    mockserver_dir = tmp_path / "mockserver"  # left empty: exercises the "not implemented yet" path
    mockserver_dir.mkdir()

    monkeypatch.setattr(mock, "ROUNDS", rounds)
    monkeypatch.setattr(mock, "WORK", work)
    monkeypatch.setattr(mock, "MOCKSERVER", mockserver_dir)
    return rounds, work


class Args:
    """Minimal stand-in for argparse.Namespace."""

    def __init__(self, **kw):
        self.__dict__.update(kw)


# ---------------------------------------------------------------------------
# id resolution
# ---------------------------------------------------------------------------


def test_dir_resolves_unique(tree):
    d = mock._dir("ps01")
    assert d.name == "ps01_widget_levels"


def test_dir_not_found(tree):
    with pytest.raises(SystemExit) as exc:
        mock._dir("zz99")
    assert "no round item matching" in str(exc.value)


def test_dir_ambiguous(tree):
    rounds, _work = tree
    # create a second item that legitimately collides on the full id "ps01"
    dup = rounds / "03_phone_screen" / "ps01_duplicate"
    dup.mkdir(parents=True)
    with pytest.raises(SystemExit) as exc:
        mock._dir("ps01")
    assert "ambiguous" in str(exc.value)


# ---------------------------------------------------------------------------
# list / show
# ---------------------------------------------------------------------------


def test_list_includes_all_rounds(tree, capsys):
    mock.cmd_list(Args())
    out = capsys.readouterr().out
    assert "03_phone_screen" in out
    assert "ps01" in out and "Widget levels" in out and "45min" in out
    assert "04_bug_squash" in out and "60min" in out
    assert "02_hm: bank.json" not in out  # sanity: not the literal wrong format
    assert "bank.json: 2 题" in out  # 02_hm has 2 questions


def test_show_ps_prints_problem_md(tree, capsys):
    mock.cmd_show(Args(id="ps01"))
    assert "Widget levels" in capsys.readouterr().out


def test_show_bs_prints_readme(tree, capsys):
    mock.cmd_show(Args(id="bs01"))
    assert "Calc bug" in capsys.readouterr().out


def test_show_sd_prints_prompt(tree, capsys):
    mock.cmd_show(Args(id="sd01"))
    out = capsys.readouterr().out
    assert "Ledger service" in out
    assert "design a ledger" in out


# ---------------------------------------------------------------------------
# start
# ---------------------------------------------------------------------------


def test_start_ps_resets_starter_from_template(tree, capsys):
    mock.cmd_start(Args(id="ps01", minutes=None))
    d = mock._dir("ps01")
    assert (d / "starter.py").read_text() == (d / "starter_template.py").read_text()
    out = capsys.readouterr().out
    assert "Widget levels" in out
    assert "计时开始：45 分钟" in out


def test_start_writes_timer_file(tree):
    mock.cmd_start(Args(id="ps01", minutes=10))
    f = mock._timer_file("ps01")
    assert f.exists()
    st = json.loads(f.read_text())
    assert st["minutes"] == 10


def test_start_bs_copies_and_runs_pytest(tree, capfd):
    mock.cmd_start(Args(id="bs02", minutes=None))
    work = mock.WORK / "bs02"
    assert (work / "tests" / "test_trivial.py").exists()
    out = capfd.readouterr().out
    assert "1 passed" in out


def test_start_bs_wipes_existing_work_dir(tree):
    work = mock.WORK / "bs02"
    work.mkdir(parents=True)
    (work / "stale.txt").write_text("old")
    mock.cmd_start(Args(id="bs02", minutes=None))
    assert not (work / "stale.txt").exists()
    assert (work / "tests" / "test_trivial.py").exists()


# ---------------------------------------------------------------------------
# time
# ---------------------------------------------------------------------------


def test_time_computes_remaining(tree, capsys):
    mock.WORK.mkdir(parents=True, exist_ok=True)
    (mock.WORK / ".timers").mkdir(parents=True, exist_ok=True)
    mock._timer_file("ps01").write_text(json.dumps({"t0": time.time(), "minutes": 45}))
    mock.cmd_time(Args(id="ps01"))
    out = capsys.readouterr().out.strip()
    assert out.endswith("left")
    assert out.startswith("44:") or out.startswith("45:")


def test_time_expired(tree, capsys):
    mock.WORK.mkdir(parents=True, exist_ok=True)
    (mock.WORK / ".timers").mkdir(parents=True, exist_ok=True)
    mock._timer_file("ps01").write_text(json.dumps({"t0": time.time() - 100000, "minutes": 1}))
    mock.cmd_time(Args(id="ps01"))
    assert "TIME IS UP" in capsys.readouterr().out


def test_time_no_timer_errors(tree):
    with pytest.raises(SystemExit) as exc:
        mock.cmd_time(Args(id="ps01"))
    assert "no timer" in str(exc.value)


# ---------------------------------------------------------------------------
# test / ref for non-coding round (sd) -> no autotest
# ---------------------------------------------------------------------------


def test_cmd_test_sd_has_no_autotest(tree, capsys):
    mock.cmd_test(Args(id="sd01", k=None))
    assert "无自动测试" in capsys.readouterr().out


def test_cmd_ref_bs_applies_patch_and_passes(tree, capfd):
    with pytest.raises(SystemExit) as exc:
        mock.cmd_ref(Args(id="bs01", k=None))
    assert exc.value.code == 0
    assert "1 passed" in capfd.readouterr().out


# ---------------------------------------------------------------------------
# bq
# ---------------------------------------------------------------------------


def test_bq_draws_n_questions(tree, capsys):
    mock.cmd_bq(Args(round=None, n=3, minutes=3, seed=1))
    out = capsys.readouterr().out
    assert out.count("[") == 3  # "[1/3]" "[2/3]" "[3/3]"


def test_bq_seed_deterministic(tree, capsys):
    mock.cmd_bq(Args(round=None, n=3, minutes=3, seed=42))
    out1 = capsys.readouterr().out
    mock.cmd_bq(Args(round=None, n=3, minutes=3, seed=42))
    out2 = capsys.readouterr().out
    assert out1 == out2


def test_bq_single_round_filter(tree, capsys):
    mock.cmd_bq(Args(round="recruiter", n=5, minutes=3, seed=0))
    out = capsys.readouterr().out
    assert "Why Stripe?" in out
    assert "STAR story" not in out


def test_bq_missing_bank_errors(tree, monkeypatch):
    monkeypatch.setattr(mock, "NONCODING_ROUNDS", ["99_nope"])
    with pytest.raises(SystemExit) as exc:
        mock.cmd_bq(Args(round=None, n=1, minutes=1, seed=0))
    assert "no bank.json" in str(exc.value)


# ---------------------------------------------------------------------------
# serve
# ---------------------------------------------------------------------------


def test_serve_reads_metadata_and_reports_missing_module(tree):
    with pytest.raises(SystemExit) as exc:
        mock.cmd_serve(Args(id="int01", port=0))
    assert "maps.py" in str(exc.value) or "mockserver" in str(exc.value)


def test_serve_non_int_id_errors(tree):
    with pytest.raises(SystemExit) as exc:
        mock.cmd_serve(Args(id="ps01", port=0))
    assert "integration" in str(exc.value)
