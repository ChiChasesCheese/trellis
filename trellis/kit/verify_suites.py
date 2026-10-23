"""Accept a batch of problem sets.

  single-file sets (solution.py/starter.py): reference green, empty starter red.
  codebase sets (cbNN_*/acceptance/): acceptance green on solution/, every `core` test red on the untouched
  starter/, and both starter/ and solution/ keep their own test suites green.

usage: trellis kit verify_suites --co abnormal "loop/rounds/01_ai_screen/cb*"
       (the glob is relative to the kit; pytest runs with `uv run --project <this repo> --with pytest`)
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess

from .paths import Kit

ANSI = re.compile(r"\x1b\[[0-9;]*m")


def add_arguments(ap: argparse.ArgumentParser, common: argparse.ArgumentParser) -> None:
    ap.add_argument("pattern", help='glob of problem dirs relative to the kit, e.g. "loop/rounds/04_ood/od*"')
    ap.add_argument("--clear-addopts", action=argparse.BooleanOptionalAction, default=None,
                    help="run pytest with -o addopts= (default: the company profile)")


def _run(kit: Kit, clear_addopts: bool, args, cwd, **env):
    e = dict(os.environ, **env)
    extra = ["-o", "addopts=", "-W", "ignore::DeprecationWarning"] if clear_addopts else []
    p = subprocess.run(
        ["uv", "run", "--project", str(kit.project), "--with", "pytest", "python", "-m", "pytest",
         *args, "-q", *extra, "-p", "no:cacheprovider"],
        cwd=cwd, env=e, capture_output=True, text=True,
    )
    lines = [ANSI.sub("", l) for l in p.stdout.strip().splitlines() if l.strip()]
    return p.returncode, (lines[-1] if lines else p.stderr.strip()[-200:])


def run(a, kit: Kit) -> int:
    root = kit.kit
    clear = kit.profile.clear_addopts if a.clear_addopts is None else a.clear_addopts
    ok = True
    for d in sorted(root.glob(a.pattern)):
        if not d.is_dir():
            continue
        rel = d.relative_to(root)
        if (d / "acceptance").is_dir():
            rc_s, sol = _run(kit, clear, [str(rel / "acceptance")], root, IMPL="solution")
            rc_t, sta = _run(kit, clear, [str(rel / "acceptance"), "-m", "core"], root, IMPL="starter")
            starter_all_red = rc_t != 0 and " passed" not in sta
            rc_os, own_s = _run(kit, clear, [], d / "starter")
            rc_ol, own_l = _run(kit, clear, [], d / "solution")
            good = rc_s == 0 and starter_all_red and rc_os == 0 and rc_ol == 0
            print(f"{'OK ' if good else 'BAD'} {d.name}\n    acceptance/solution: {sol}\n    acceptance/starter core: {sta}"
                  f"\n    own tests starter: {own_s}\n    own tests solution: {own_l}")
        else:
            rc_s, sol = _run(kit, clear, [str(rel)], root, IMPL="solution")
            rc_t, sta = _run(kit, clear, [str(rel)], root, IMPL="starter")
            good = rc_s == 0 and rc_t != 0
            print(f"{'OK ' if good else 'BAD'} {d.name:40s} solution: {sol:40s} | starter: {sta}")
        ok &= good
    print("ALL ACCEPTED" if ok else "SOME REJECTED")
    return 0 if ok else 1
