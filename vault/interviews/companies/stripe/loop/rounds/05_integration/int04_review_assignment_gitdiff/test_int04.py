"""int04 Review Assignment via git diff + CSV owners — tests. Uses the `impl` fixture
(repo-root conftest.py, loads solution.py or starter.py under IMPL=starter) and
`run_script` for io tests. Each git-backed test builds its own throwaway repo under
`tmp_path` via `subprocess` (git init/commit/branch/mv) and relies on pytest's own
per-test tmp_path cleanup -- nothing is left behind. If `git` isn't on PATH at all, every
test that needs a real repo skips instead of failing (see `_require_git`)."""

from __future__ import annotations

import random
import shutil
import subprocess
import time
from pathlib import Path

import pytest

GIT = shutil.which("git")
DATA_DIR = Path(__file__).parent / "data"
OWNERS_CSV = str(DATA_DIR / "owners.csv")


def _require_git():
    if GIT is None:
        pytest.skip("git executable not found on PATH")


def _run_git(repo, *args) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True)


def _init_repo(tmp_path):
    """A fresh repo with a `main` branch and one commit, ready for a `feature` branch to
    be checked out off it. Renames the branch to `main` *after* the first commit --
    `git init`'s default branch name varies by local config (master/main/etc.), and
    `git branch -m` needs a real commit to rename."""
    _require_git()
    repo = tmp_path / "repo"
    repo.mkdir()
    _run_git(repo, "init", "-q")
    _run_git(repo, "config", "user.email", "test@example.com")
    _run_git(repo, "config", "user.name", "Test User")
    return repo


def _commit_all(repo, message: str) -> None:
    _run_git(repo, "add", "-A")
    _run_git(repo, "commit", "-q", "-m", message)


def _write(repo, rel_path: str, content: str) -> None:
    p = repo / rel_path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)


def _build_worked_example_repo(tmp_path) -> str:
    """Builds the exact scenario from problem.md's Worked examples: a `main` branch with
    5 files, and a `feature` branch with a delete (D), a modify (M), two adds (A) and a
    rename (R100)."""
    repo = _init_repo(tmp_path)
    _write(repo, "README.md", "hello\n")
    _write(repo, "src/payments/checkout.py", "def checkout():\n    pass\n")
    _write(repo, "src/frontend/app.js", "console.log('app');\n")
    _write(repo, "src/utils/helpers.py", "def helper():\n    pass\n")
    _write(repo, "docs/guide.md", "# guide\n")
    _commit_all(repo, "initial commit on main")
    _run_git(repo, "branch", "-m", "main")

    _run_git(repo, "checkout", "-q", "-b", "feature")
    (repo / "src" / "frontend" / "app.js").unlink()  # D
    _write(repo, "src/payments/checkout.py", "def checkout():\n    return True\n")  # M
    _write(repo, "src/payments/gateway.py", "def gateway():\n    pass\n")  # A
    _write(repo, "src/payments/refund.py", "def refund():\n    pass\n")  # A
    _run_git(repo, "mv", "src/utils/helpers.py", "src/utils/helper_v2.py")  # R100
    _commit_all(repo, "feature changes")
    return str(repo)


def _worked_owners_csv(tmp_path) -> str:
    """Copies data/owners.csv verbatim -- keeps the test independent of the shared
    fixture file's on-disk path while still exercising the exact rows from problem.md."""
    dest = tmp_path / "owners.csv"
    shutil.copy(OWNERS_CSV, dest)
    return str(dest)


WORKED_CHANGED = [
    "src/frontend/app.js",
    "src/payments/checkout.py",
    "src/payments/gateway.py",
    "src/payments/refund.py",
    "src/utils/helpers.py",
    "src/utils/helper_v2.py",
]


# --------------------------------------------------------------------------- Part 1


@pytest.mark.part1
def test_worked_example_changed_files(impl, tmp_path):
    repo = _build_worked_example_repo(tmp_path)
    assert impl.changed_files(repo, "main", "feature") == WORKED_CHANGED


@pytest.mark.part1
def test_add_modify_delete_each_contribute_one_path(impl, tmp_path):
    repo = _build_worked_example_repo(tmp_path)
    changed = impl.changed_files(repo, "main", "feature")
    # A/M/D each contribute exactly one entry (not the rename pair).
    for path in ("src/frontend/app.js", "src/payments/checkout.py", "src/payments/gateway.py"):
        assert changed.count(path) == 1


@pytest.mark.part1
def test_rename_contributes_both_old_and_new_path(impl, tmp_path):
    repo = _build_worked_example_repo(tmp_path)
    changed = impl.changed_files(repo, "main", "feature")
    assert "src/utils/helpers.py" in changed
    assert "src/utils/helper_v2.py" in changed
    assert len(changed) == 6  # 4 singles + 2 from the one rename


@pytest.mark.part1
@pytest.mark.edge
def test_identical_branches_return_empty_list(impl, tmp_path):
    repo = _init_repo(tmp_path)
    _write(repo, "README.md", "hello\n")
    _commit_all(repo, "init")
    _run_git(repo, "branch", "-m", "main")
    _run_git(repo, "checkout", "-q", "-b", "feature")  # no changes at all
    assert impl.changed_files(repo, "main", "feature") == []


@pytest.mark.part1
@pytest.mark.edge
def test_three_dot_diff_ignores_unrelated_base_only_commits(impl, tmp_path):
    """`base...head` diffs against the merge base, so commits `main` picks up *after*
    `feature` branched off must not show up -- this is the whole point of using
    three-dot instead of two-dot diff (problem.md Rules / interviewer follow-up #1)."""
    repo = _init_repo(tmp_path)
    _write(repo, "shared.txt", "shared\n")
    _commit_all(repo, "init")
    _run_git(repo, "branch", "-m", "main")

    _run_git(repo, "checkout", "-q", "-b", "feature")
    _write(repo, "feature_only.txt", "feature\n")
    _commit_all(repo, "feature adds a file")

    _run_git(repo, "checkout", "-q", "main")
    _write(repo, "main_only.txt", "main\n")
    _commit_all(repo, "main advances independently")

    changed = impl.changed_files(repo, "main", "feature")
    assert changed == ["feature_only.txt"]
    assert "main_only.txt" not in changed


@pytest.mark.part1
@pytest.mark.edge
def test_repo_error_when_git_not_on_path(impl, tmp_path, monkeypatch):
    repo = _build_worked_example_repo(tmp_path)
    monkeypatch.setenv("PATH", "")
    with pytest.raises(impl.RepoError):
        impl.changed_files(repo, "main", "feature")


@pytest.mark.part1
@pytest.mark.edge
def test_repo_error_when_path_is_not_a_git_repo(impl, tmp_path):
    _require_git()
    not_a_repo = tmp_path / "plain_dir"
    not_a_repo.mkdir()
    (not_a_repo / "file.txt").write_text("hi\n")
    with pytest.raises(impl.RepoError):
        impl.changed_files(str(not_a_repo), "main", "feature")


@pytest.mark.part1
@pytest.mark.edge
def test_repo_error_when_ref_does_not_resolve(impl, tmp_path):
    repo = _build_worked_example_repo(tmp_path)
    with pytest.raises(impl.RepoError):
        impl.changed_files(repo, "main", "does-not-exist-branch")
    with pytest.raises(impl.RepoError):
        impl.changed_files(repo, "no-such-base-either", "feature")


@pytest.mark.part1
@pytest.mark.edge
def test_repo_error_message_is_nonempty_and_type_is_repo_error(impl, tmp_path):
    _require_git()
    not_a_repo = tmp_path / "empty_dir"
    not_a_repo.mkdir()
    try:
        impl.changed_files(str(not_a_repo), "main", "feature")
        pytest.fail("expected RepoError")
    except impl.RepoError as e:
        assert str(e)  # non-empty message
    except Exception as e:  # pragma: no cover - only reached by a buggy impl
        pytest.fail(f"expected RepoError, got {type(e).__name__}: {e}")


@pytest.mark.part1
def test_changed_files_calls_git_exactly_once(impl, tmp_path, monkeypatch):
    """Performance requirement: one `git diff --name-status` call, never one per file
    (problem.md Rules / Part 3 性能 section)."""
    repo = _build_worked_example_repo(tmp_path)
    calls = []
    real_run = subprocess.run

    def _counting_run(*args, **kwargs):
        calls.append(args)
        return real_run(*args, **kwargs)

    monkeypatch.setattr(subprocess, "run", _counting_run)
    result = impl.changed_files(repo, "main", "feature")
    assert result == WORKED_CHANGED
    assert len(calls) == 1


# --------------------------------------------------------------------------- Part 2


@pytest.mark.part2
def test_load_owners_worked_example_csv(impl):
    rows = impl.load_owners(OWNERS_CSV)
    assert rows[0] == ("README.md", "alice")
    assert ("src/payments/*", "alice") in rows
    assert ("src/payments/*", "bob") in rows
    assert ("Src/Payments/*", "carol") in rows
    assert len(rows) == 11  # 11 data rows, header skipped


@pytest.mark.part2
@pytest.mark.edge
def test_load_owners_skips_blank_lines_and_tolerates_missing_header(impl, tmp_path):
    p = tmp_path / "owners.csv"
    p.write_text("a.py,alice\n\nb.py,bob\n")  # no header row, one blank line
    rows = impl.load_owners(str(p))
    assert rows == [("a.py", "alice"), ("b.py", "bob")]


@pytest.mark.part2
def test_match_owners_exact_path_beats_wildcard(impl):
    """The most-easily-broken case from problem.md: an exact match must win outright,
    not just get added to the wildcard owners."""
    rows = impl.load_owners(OWNERS_CSV)
    assert impl.match_owners("src/payments/checkout.py", rows) == ["dave"]


@pytest.mark.part2
def test_match_owners_multiple_owners_at_same_specificity(impl):
    rows = impl.load_owners(OWNERS_CSV)
    owners = impl.match_owners("src/payments/gateway.py", rows)
    assert set(owners) == {"alice", "bob", "carol"}


@pytest.mark.part2
def test_match_owners_casefold_not_lower(impl):
    """Path comparison must use `str.casefold()`, not `.lower()`: German 'ß' casefolds to
    'ss' (so 'straße.py' and 'STRASSE.PY' are the same path) but `.lower()` leaves 'ß'
    untouched, so a `.lower()`-based implementation would miss this match."""
    rows = [("straße.py", "alice")]  # "straße.py"
    assert impl.match_owners("STRASSE.PY", rows) == ["alice"]


@pytest.mark.part2
def test_match_owners_pattern_case_variant_is_same_specificity(impl):
    """`Src/Payments/*` (owners.csv) and `src/payments/*` differ only in case but are the
    same literal length -- both count at the same specificity tier, not one beating the
    other because of how the path itself happens to be cased."""
    rows = impl.load_owners(OWNERS_CSV)
    owners = impl.match_owners("SRC/PAYMENTS/gateway.py", rows)  # path in yet another case
    assert set(owners) == {"alice", "bob", "carol"}


@pytest.mark.part2
@pytest.mark.edge
def test_match_owners_no_match_returns_empty_list(impl):
    rows = impl.load_owners(OWNERS_CSV)
    assert impl.match_owners("src/utils/helper_v2.py", rows) == []


@pytest.mark.part2
def test_tally_owners_worked_example(impl, tmp_path):
    repo = _build_worked_example_repo(tmp_path)
    changed = impl.changed_files(repo, "main", "feature")
    rows = impl.load_owners(OWNERS_CSV)
    tally = impl.tally_owners(changed, rows)
    assert tally == {
        "erin": 1,
        "frank": 1,
        "dave": 1,
        "alice": 2,
        "bob": 2,
        "carol": 2,
        "henry": 1,
        "irene": 1,
        "UNOWNED": 1,
    }


@pytest.mark.part2
@pytest.mark.edge
def test_tally_owners_unmatched_file_goes_to_unowned_bucket(impl):
    rows = [("known.py", "alice")]
    tally = impl.tally_owners(["known.py", "unknown.py"], rows)
    assert tally == {"alice": 1, "UNOWNED": 1}


@pytest.mark.part2
def test_assign_worked_example(impl, tmp_path):
    repo = _build_worked_example_repo(tmp_path)
    changed = impl.changed_files(repo, "main", "feature")
    rows = impl.load_owners(OWNERS_CSV)
    assert impl.assign(changed, rows) == "alice"


@pytest.mark.part2
@pytest.mark.edge
def test_assign_tie_break_lexicographically_smallest(impl):
    rows = [("a.py", "zoe"), ("b.py", "amy")]
    assert impl.assign(["a.py", "b.py"], rows) == "amy"


@pytest.mark.part2
@pytest.mark.edge
def test_assign_unowned_wins_ties_because_uppercase_sorts_first(impl):
    """UNOWNED (starts with 'U', ASCII 85) sorts before any lowercase owner name (ASCII
    97+) -- a tie between UNOWNED and a lowercase owner must let UNOWNED win 'naturally',
    with no special-cased skip of UNOWNED in the tie-break."""
    rows = [("owned.py", "zeta")]
    tally = impl.assign(["owned.py", "unmatched.py"], rows)
    assert tally == "UNOWNED"


@pytest.mark.part2
@pytest.mark.edge
def test_assign_no_changed_files_returns_unowned(impl):
    rows = impl.load_owners(OWNERS_CSV)
    assert impl.assign([], rows) == "UNOWNED"


# --------------------------------------------------------------------------- Part 3


@pytest.mark.part3
def test_top_owners_worked_example(impl, tmp_path):
    repo = _build_worked_example_repo(tmp_path)
    changed = impl.changed_files(repo, "main", "feature")
    rows = impl.load_owners(OWNERS_CSV)
    assert impl.top_owners(changed, rows, 3) == [("alice", 2), ("bob", 2), ("carol", 2)]


@pytest.mark.part3
@pytest.mark.fmt
def test_top_owners_ordering_is_count_desc_then_name_asc(impl):
    rows = [("a.py", "zoe"), ("b.py", "amy"), ("c.py", "amy"), ("d.py", "bob")]
    top = impl.top_owners(["a.py", "b.py", "c.py", "d.py"], rows, 3)
    assert top == [("amy", 2), ("bob", 1), ("zoe", 1)]


@pytest.mark.part3
@pytest.mark.edge
def test_top_owners_k_larger_than_distinct_owners_not_padded(impl):
    rows = [("a.py", "amy")]
    assert impl.top_owners(["a.py"], rows, 5) == [("amy", 1)]


@pytest.mark.part3
def test_main_cli_prints_top_owners(impl, tmp_path, capsys):
    repo = _build_worked_example_repo(tmp_path)
    csv_path = _worked_owners_csv(tmp_path)
    rc = impl.main_cli(
        ["--repo", repo, "--base", "main", "--head", "feature", "--csv", csv_path, "--top", "3"]
    )
    assert rc == 0
    lines = capsys.readouterr().out.splitlines()
    assert lines == ["alice: 2", "bob: 2", "carol: 2"]


@pytest.mark.part3
def test_main_cli_default_top_is_one(impl, tmp_path, capsys):
    repo = _build_worked_example_repo(tmp_path)
    csv_path = _worked_owners_csv(tmp_path)
    rc = impl.main_cli(["--repo", repo, "--base", "main", "--head", "feature", "--csv", csv_path])
    assert rc == 0
    lines = capsys.readouterr().out.splitlines()
    assert lines == ["alice: 2"]


@pytest.mark.part3
@pytest.mark.edge
def test_main_cli_propagates_repo_error(impl, tmp_path):
    _require_git()
    not_a_repo = tmp_path / "plain_dir"
    not_a_repo.mkdir()
    csv_path = _worked_owners_csv(tmp_path)
    with pytest.raises(impl.RepoError):
        impl.main_cli(["--repo", str(not_a_repo), "--base", "main", "--head", "feature", "--csv", csv_path])


# --------------------------------------------------------------------------- io


@pytest.mark.part1
@pytest.mark.io
def test_io_part1(run_script, tmp_path):
    repo = _build_worked_example_repo(tmp_path)
    r = run_script(f"PART 1\n{repo}\nmain\nfeature\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout.splitlines() == WORKED_CHANGED


@pytest.mark.part2
@pytest.mark.io
def test_io_part2(run_script, tmp_path):
    repo = _build_worked_example_repo(tmp_path)
    csv_path = _worked_owners_csv(tmp_path)
    r = run_script(f"PART 2\n{repo}\nmain\nfeature\n{csv_path}\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == "alice"


@pytest.mark.part3
@pytest.mark.io
def test_io_part3(run_script, tmp_path):
    repo = _build_worked_example_repo(tmp_path)
    csv_path = _worked_owners_csv(tmp_path)
    r = run_script(f"PART 3\n{repo}\nmain\nfeature\n{csv_path}\n3\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout.splitlines() == ["alice: 2", "bob: 2", "carol: 2"]


@pytest.mark.part1
@pytest.mark.io
def test_io_empty_stdin(run_script):
    r = run_script("")
    assert r.returncode == 0
    assert r.stdout == ""


# --------------------------------------------------------------------------- perf


@pytest.mark.part3
@pytest.mark.perf
def test_perf_tally_and_top_owners_10k_changed_files(impl):
    """10^4 changed files against a few dozen owner rules -- problem.md's stated perf
    budget (< 2s), see Rules / 性能."""
    rng = random.Random(0)
    owner_rows = [(f"dir{i}/*", f"owner{i}") for i in range(40)]
    changed = [f"dir{rng.randrange(40)}/file{i}.py" for i in range(10_000)]

    t0 = time.perf_counter()
    tally = impl.tally_owners(changed, owner_rows)
    top = impl.top_owners(changed, owner_rows, 5)
    elapsed = time.perf_counter() - t0

    assert sum(tally.values()) == 10_000
    assert len(top) == 5
    assert elapsed < 2.0, f"too slow: {elapsed:.2f}s"
