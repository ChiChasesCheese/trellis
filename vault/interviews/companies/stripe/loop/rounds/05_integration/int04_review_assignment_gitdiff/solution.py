"""int04 Review Assignment via git diff + CSV owners — reference solution.

Given two branches of the same git repo, compute the changed files (via `git diff
--name-status`, the interview's original wording used JGit; here it's the `git` CLI
through subprocess, stdlib only) and a `path -> owner` CSV mapping (supporting a
trailing-`*` prefix wildcard and multiple owners per path), find the owner(s) with the
most changed files.

Public API (same shape as starter.py / starter_template.py):
    changed_files(repo, base, head) -> list[str]              Part 1 (raises RepoError)
    load_owners(csv_path) -> list[tuple[str, str]]             Part 2
    match_owners(path, owner_rows) -> list[str]                Part 2
    tally_owners(changed, owner_rows) -> dict[str, int]        Part 2
    assign(changed, owner_rows) -> str                         Part 2
    top_owners(changed, owner_rows, k) -> list[tuple[str,int]] Part 3
    main_cli(argv) -> int                                      Part 3 (--repo/--base/--head/--csv/--top)
    main(stdin=sys.stdin, stdout=sys.stdout) -> None            PART n driver for io tests

Only stdlib: subprocess, csv, argparse.
"""

from __future__ import annotations

import argparse
import csv
import subprocess
import sys

UNOWNED = "UNOWNED"


class RepoError(Exception):
    """Raised for any git-level failure: git not installed, `repo` is not a git
    repository, or `base`/`head` doesn't resolve to a commit."""


# --------------------------------------------------------------------------- Part 1


def _run_git(repo: str, args: list[str]) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", repo, *args],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except FileNotFoundError as e:
        raise RepoError("git executable not found on PATH") from e
    except OSError as e:
        raise RepoError(f"could not run git: {e}") from e
    if result.returncode != 0:
        raise RepoError(f"git {' '.join(args)} failed in {repo!r}: {result.stderr.strip()}")
    return result.stdout


def changed_files(repo: str, base: str, head: str) -> list[str]:
    """Files that changed between `base` and `head` (three-dot: against their merge
    base), via `git diff --name-status`. A/M/D contribute one path; a rename (R) or
    copy (C) contributes BOTH the old and the new path -- two entries, by design (see
    problem.md). Raises RepoError if git is missing, `repo` isn't a git repo, or
    `base`/`head` doesn't resolve."""
    out = _run_git(repo, ["diff", "--name-status", f"{base}...{head}"])
    paths: list[str] = []
    for line in out.splitlines():
        line = line.rstrip("\n")
        if not line.strip():
            continue
        parts = line.split("\t")
        status = parts[0]
        if status[:1] in ("R", "C"):
            if len(parts) >= 3:
                paths.append(parts[1])
                paths.append(parts[2])
        elif len(parts) >= 2:
            paths.append(parts[1])
    return paths


# --------------------------------------------------------------------------- Part 2


def load_owners(csv_path: str) -> list[tuple[str, str]]:
    """Read `path,owner` CSV rows (an optional `path,owner` header is skipped; blank
    lines ignored) into an ordered list of (pattern, owner) pairs -- order preserved,
    duplicates (same pattern, different owner; or a case-different pattern) all kept."""
    rows: list[tuple[str, str]] = []
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if not row or not "".join(c.strip() for c in row):
                continue
            if (
                i == 0
                and len(row) >= 2
                and row[0].strip().lower() == "path"
                and row[1].strip().lower() == "owner"
            ):
                continue
            path, owner = row[0].strip(), row[1].strip()
            if path and owner:
                rows.append((path, owner))
    return rows


def _pattern_matches(pattern: str, path: str) -> bool:
    """Case-insensitive (casefold): a trailing '*' is a prefix wildcard, anything else
    must match the path exactly."""
    p, f = pattern.casefold(), path.casefold()
    if p.endswith("*"):
        return f.startswith(p[:-1])
    return f == p


def match_owners(path: str, owner_rows: list[tuple[str, str]]) -> list[str]:
    """All owners for `path` at the MOST SPECIFIC matching pattern (longest pattern
    string wins -- an exact-path rule beats any wildcard, and a longer wildcard prefix
    beats a shorter one). Multiple owner rows sharing that most-specific pattern (or a
    case-different spelling of it) all count. [] means unowned -- callers fold that into
    the UNOWNED bucket, this function doesn't know about UNOWNED."""
    matches = [(pat, owner) for pat, owner in owner_rows if _pattern_matches(pat, path)]
    if not matches:
        return []
    max_len = max(len(pat) for pat, _ in matches)
    owners: list[str] = []
    for pat, owner in matches:
        if len(pat) == max_len and owner not in owners:
            owners.append(owner)
    return owners


def tally_owners(changed: list[str], owner_rows: list[tuple[str, str]]) -> dict[str, int]:
    """owner -> number of changed files credited to them (a file with N matching owners
    at the winning specificity credits all N; an unmatched file credits UNOWNED)."""
    counts: dict[str, int] = {}
    for path in changed:
        owners = match_owners(path, owner_rows) or [UNOWNED]
        for owner in owners:
            counts[owner] = counts.get(owner, 0) + 1
    return counts


def assign(changed: list[str], owner_rows: list[tuple[str, str]]) -> str:
    """The single owner with the most changed files. Ties broken by lexicographically
    smallest owner name. No changed files at all -> UNOWNED (nothing to assign)."""
    counts = tally_owners(changed, owner_rows)
    if not counts:
        return UNOWNED
    max_count = max(counts.values())
    return min(owner for owner, c in counts.items() if c == max_count)


# --------------------------------------------------------------------------- Part 3


def top_owners(changed: list[str], owner_rows: list[tuple[str, str]], k: int) -> list[tuple[str, int]]:
    """Top `k` owners by changed-file count, ordered (count desc, owner name asc);
    fewer than `k` distinct owners -> shorter list, never padded."""
    counts = tally_owners(changed, owner_rows)
    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return ordered[:k]


def main_cli(argv: list[str] | None = None) -> int:
    """--repo REPO --base BASE --head HEAD --csv CSV [--top K]"""
    parser = argparse.ArgumentParser(prog="int04-review-assign")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--csv", required=True)
    parser.add_argument("--top", type=int, default=1)
    args = parser.parse_args(argv)

    owner_rows = load_owners(args.csv)
    changed = changed_files(args.repo, args.base, args.head)
    for owner, count in top_owners(changed, owner_rows, args.top):
        print(f"{owner}: {count}")
    return 0


# --------------------------------------------------------------------------- PART n stdin driver


def _read_nonblank(stdin) -> list[str]:
    return [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    """Dispatches on a leading 'PART n' line, remaining non-blank lines are that part's
    positional arguments (see problem.md's "main() / PART n 驱动")."""
    lines = _read_nonblank(stdin)
    if not lines or not lines[0].upper().startswith("PART"):
        return
    part = int(lines[0].split()[1])
    args = lines[1:]
    out: list[str] = []

    if part == 1:
        repo, base, head = args
        out = changed_files(repo, base, head)

    elif part == 2:
        repo, base, head, csv_path = args
        changed = changed_files(repo, base, head)
        owner_rows = load_owners(csv_path)
        out = [assign(changed, owner_rows)]

    elif part == 3:
        repo, base, head, csv_path, k_str = args
        changed = changed_files(repo, base, head)
        owner_rows = load_owners(csv_path)
        out = [f"{owner}: {count}" for owner, count in top_owners(changed, owner_rows, int(k_str))]

    else:
        raise ValueError(f"unknown PART {part!r}")

    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
