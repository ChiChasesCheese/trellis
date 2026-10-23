#!/usr/bin/env python3
"""Changed learning pages, and the style checks that run only on them.

    python3 scripts/changed_learning_pages.py [--base REF] [--check]     # pages changed since REF (default: working tree vs HEAD)
    python3 scripts/changed_learning_pages.py --base origin/main --check # what CI runs on a pull request
    python3 scripts/changed_learning_pages.py --check --files a.md b.md  # classify + check given files (pre-commit)
    python3 scripts/changed_learning_pages.py --base HEAD~5 --lp         # only LP-style paths, one per line

Pages are `.md` files under `vault/`, added / copied / modified / renamed, excluding web clippings (`*/clippings/*`)
and the pages trellis generates (`vault/Brief.md`, `vault/Codebases/`, `vault/Corpora/`). Two kinds:

  LP-style  `*/lp/**`, `*/behavioral/**`, `vault/interviews/core/stories/**`   -> `plain_style.py --outline`
  other     every remaining page                                                 -> `plain_style.py`
  both                                                                           -> `phone_diagrams.py`

`--check` runs those and exits 1 if any changed page fails. Legacy pages that were not touched are never looked at,
so old style debt cannot turn a build red. With `--base REF` the diff is `REF...HEAD` (changes since the merge base);
an unknown REF (a force-pushed `before` sha, an all-zero sha) falls back to `origin/main`, then `main`.
Without `--base`: staged + unstaged changes against HEAD plus untracked files.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GENERATED = ("vault/Brief.md", "vault/Codebases/", "vault/Corpora/")
LP_PREFIXES = ("vault/interviews/core/stories/",)
LP_DIRS = {"lp", "behavioral"}
BATCH = 100


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True)


def is_page(path: str) -> bool:
    parts = path.split("/")
    return (path.startswith("vault/") and path.endswith(".md") and "clippings" not in parts[:-1]
            and not any(path == g or path.startswith(g) for g in GENERATED))


def is_lp(path: str) -> bool:
    parts = path.split("/")
    return path.startswith(LP_PREFIXES) or any(p in LP_DIRS for p in parts[:-1])


def resolve_base(base: str) -> str:
    for cand in (base, "origin/main", "main"):
        if cand and git("rev-parse", "--verify", "--quiet", f"{cand}^{{commit}}").returncode == 0:
            if cand != base:
                print(f"warning: base {base!r} not found, using {cand!r}", file=sys.stderr)
            return cand
    sys.exit(f"cannot resolve base {base!r} (and neither origin/main nor main exists); fetch with depth 0")


def changed_files(base: str | None) -> list[str]:
    if base:
        r = git("diff", "--name-only", "--diff-filter=ACMR", f"{resolve_base(base)}...HEAD")
        names = r.stdout.splitlines()
    else:
        r = git("diff", "--name-only", "--diff-filter=ACMR", "HEAD")
        names = r.stdout.splitlines() + git("ls-files", "--others", "--exclude-standard").stdout.splitlines()
    if r.returncode != 0:
        sys.exit(r.stderr.strip() or "git diff failed")
    return sorted(set(names))


def split(files: list[str]) -> tuple[list[str], list[str]]:
    pages = [f for f in files if is_page(f) and (REPO / f).is_file()]
    return [f for f in pages if is_lp(f)], [f for f in pages if not is_lp(f)]


def run(script: str, files: list[str], *flags: str) -> int:
    rc = 0
    for i in range(0, len(files), BATCH):
        rc |= subprocess.run([sys.executable, "-B", str(REPO / "scripts" / script), *flags, *files[i:i + BATCH]], cwd=REPO).returncode
    return rc


def check(lp: list[str], rest: list[str]) -> int:
    rc = 0
    if lp:
        print(f"== plain_style --outline: {len(lp)} LP page(s)", flush=True)
        rc |= run("plain_style.py", lp, "--outline")
    if rest:
        print(f"== plain_style: {len(rest)} page(s)", flush=True)
        rc |= run("plain_style.py", rest)
    if lp or rest:
        print(f"== phone_diagrams: {len(lp) + len(rest)} page(s)", flush=True)
        rc |= run("phone_diagrams.py", lp + rest)
    else:
        print("no changed learning pages")
    return 1 if rc else 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", help="git ref to compare against (REF...HEAD); default: working tree vs HEAD")
    ap.add_argument("--files", nargs="+", metavar="FILE", help="classify these files instead of asking git (pre-commit)")
    ap.add_argument("--check", action="store_true", help="run plain_style.py and phone_diagrams.py on the pages")
    which = ap.add_mutually_exclusive_group()
    which.add_argument("--lp", action="store_true", help="print only LP-style pages, one per line")
    which.add_argument("--rest", action="store_true", help="print only the other pages, one per line")
    a = ap.parse_args(argv)
    files = [str(Path(f).resolve().relative_to(REPO)) if Path(f).is_absolute() else f for f in a.files] if a.files else changed_files(a.base)
    lp, rest = split(files)
    if a.check:
        return check(lp, rest)
    if a.lp or a.rest:
        print("\n".join(lp if a.lp else rest))
        return 0
    print(f"LP-style pages ({len(lp)}):" + "".join(f"\n  {f}" for f in lp))
    print(f"other pages ({len(rest)}):" + "".join(f"\n  {f}" for f in rest))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
