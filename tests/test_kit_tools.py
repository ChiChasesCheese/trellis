"""The shared interview-kit tools (trellis/kit/): pareto, contents and the progress runtime, on small fixtures."""

import json
from pathlib import Path

import pytest

from trellis.cli import main
from trellis.kit import PROFILES, progress, resolve_kit

RANK = """# RANK

## 总表

| ID | 题 | 轮次 | 最近 | #refs | 置信度 |
|---|---|---|---|---:|---|
| q01 | Grouped totals | OA | 未知 | 4 | HIGH |
| q02 | Intervals | 电面 | 未知 | 2 | MED |
| q03 | Tell me about a conflict | recruiter | 未知 | 2 | LOW |
"""

TREE = """version: 1
rounds:
  - id: 01_oa
    name: Online assessment
    skills:
      - id: grouping
        name: Group and total
        problems: [q01]
      - id: intervals
        name: Interval merging
        problems: [q02]
"""


@pytest.fixture
def kit(tmp_path):
    root = tmp_path / "vault" / "interviews" / "companies" / "acme"
    research = tmp_path / "research" / "companies" / "acme"
    for name in ("q01_grouped_totals", "q02_intervals"):
        d = root / "problems" / name
        d.mkdir(parents=True)
        (d / "problem.md").write_text(f"# {name.split('_')[0]} · {name[4:].replace('_', ' ').title()}\n", encoding="utf-8")
    (root / "loop" / "rounds" / "01_oa").mkdir(parents=True)
    (research / "catalog").mkdir(parents=True)
    (research / "catalog" / "RANK.md").write_text(RANK, encoding="utf-8")
    (research / "tree").mkdir()
    (research / "tree" / "interview-loop.yaml").write_text(TREE, encoding="utf-8")
    return root, research


def run_kit(capsys, tool, root, research, *args):
    code = main(["kit", tool, "--co", "acme", "--kit", str(root), "--research", str(research), *args])
    return code, capsys.readouterr().out


def test_co_defaults_derive_both_directories(tmp_path):
    (tmp_path / "vault" / "interviews" / "companies" / "acme").mkdir(parents=True)
    k = resolve_kit("acme", root=tmp_path)
    assert k.kit == (tmp_path / "vault/interviews/companies/acme").resolve()
    assert k.research == (tmp_path / "research/companies/acme").resolve()


def test_profiles_carry_the_known_forks():
    assert PROFILES["abnormal"].codebase and not PROFILES["snowflake"].codebase
    assert PROFILES["millennium"].coverage_labels["pc"] == "第一轮 coding"
    assert PROFILES["stripe"].summary_dirs == ("problems",)


def test_pareto_ranks_by_round_weight_and_prints_cut_line(kit, capsys):
    root, research = kit
    code, out = run_kit(capsys, "pareto", root, research, "--focus", "OA")
    assert code == 0
    rows = [l for l in out.splitlines() if l.startswith("| ") and l[2].isdigit()]
    # OA 4 refs x 0.5 (no date) x 1.0 = 2.0 beats phone-screen 2 x 0.5 x 0.8 = 0.8 beats recruiter 2 x 0.5 x 0.6 = 0.6
    assert [r.split("|")[2].strip() for r in rows] == ["Grouped totals", "Intervals", "Tell me about a conflict"]
    assert "2.00" in rows[0] and "0.80" in rows[1] and "0.60" in rows[2]
    assert "**3 行 · 累计 80% 出现在第 2 行（前 67%）**" in out


def test_pareto_focus_changes_the_order(kit, capsys):
    root, research = kit
    _, out = run_kit(capsys, "pareto", root, research, "--focus", "电面")
    rows = [l for l in out.splitlines() if l.startswith("| ") and l[2].isdigit()]
    # OA is now a non-focus technical round: 4 x 0.5 x 0.8 = 1.60; the focused phone screen: 2 x 0.5 x 1.0 = 1.00
    assert "1.60" in rows[0] and "1.00" in rows[1]
    assert rows[1].split("|")[2].strip() == "Intervals"


def test_contents_writes_the_tree_ordered_by_score(kit, capsys):
    root, research = kit
    code, out = run_kit(capsys, "contents", root, research, "--focus", "OA")
    assert code == 0 and "2 题" in out
    text = (root / "CONTENTS.md").read_text(encoding="utf-8")
    assert "## 01_oa · Online assessment" in text
    assert "### Group and total" in text and "### Interval merging" in text
    line = next(l for l in text.splitlines() if "**q01**" in l)
    assert line.startswith("| ★ |")  # inside the cut line
    assert "[`problems/q01_grouped_totals/`](problems/q01_grouped_totals/)" in line
    # the footer names the company's own LeetCode tag list
    assert "core/leetcode/companies/acme.md" in text


def test_contents_codebase_mode_takes_titles_from_rank(kit, capsys):
    root, research = kit
    run_kit(capsys, "contents", root, research, "--focus", "OA", "--codebase")
    text = (root / "CONTENTS.md").read_text(encoding="utf-8")
    assert "**q01** Grouped totals" in text and "ai_screen.py" in text


def test_check_tree_reports_unresolvable_problems(kit, capsys):
    root, research = kit
    (research / "tree" / "interview-loop.yaml").write_text(TREE.replace("[q02]", "[q99]"), encoding="utf-8")
    code, out = run_kit(capsys, "check_tree", root, research)
    assert code == 0 and "problem not resolvable: q99" in out
    code, out = run_kit(capsys, "check_tree", root, research, "--strict")
    assert code == 1 and "ERROR problem not resolvable: q99" in out


def test_progress_logs_and_renders_a_board(kit, tmp_path):
    root, _ = kit
    (root / "problems" / "q01_grouped_totals" / "test_q01.py").write_text(
        "import pytest\n@pytest.mark.part1\ndef test_a(): pass\n", encoding="utf-8")
    old = (progress.ROOT, progress.LOG, progress.PROBLEMS, progress.ROUNDS)
    try:
        progress.configure(root)
        assert progress.LOG == root.resolve() / "progress.jsonl"
        assert "还没有任何记录" in progress.render(show_all=True)
        progress.append({"id": "q01", "kind": "drill", "impl": "starter", "passed": 3, "failed": 0, "error": 0,
                         "parts": {"part1": {"passed": 3, "failed": 0, "skipped": 0, "error": 0}},
                         "elapsed_min": 12.0, "ts": "2026-10-23T09:00:00"})
        progress.append({"id": "q02", "kind": "drill", "impl": "ref", "passed": 9, "failed": 0, "error": 0})
        assert len(progress.records()) == 2
        board = progress.render(show_all=True, kind="drill")
        assert "1/2 全绿" in board and "✅ q01" in board and "12m" in board
        assert "q02" in board and "—" in board  # the reference run does not count for the candidate
        assert json.loads((root / "progress.jsonl").read_text().splitlines()[0])["id"] == "q01"
    finally:
        progress.ROOT, progress.LOG, progress.PROBLEMS, progress.ROUNDS = old


def test_progress_board_through_the_cli(kit, capsys):
    root, research = kit
    code, out = run_kit(capsys, "progress", root, research, "status", "--all")
    assert code == 0 and "进度：0/2 全绿" in out


def test_pytest_progress_plugin_is_inert_without_the_env_var():
    from trellis.kit import pytest_progress
    pytest_progress.pytest_sessionfinish(None, 0)  # no DRILL_PROGRESS_OUT: writes nothing, raises nothing
