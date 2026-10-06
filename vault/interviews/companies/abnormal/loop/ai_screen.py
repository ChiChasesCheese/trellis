#!/usr/bin/env python3
"""AI Technical Screen mock runner: an unfamiliar codebase + an underspecified ticket, 60 minutes.

  python3 loop/ai_screen.py list                          # codebases and tickets
  python3 loop/ai_screen.py start cb02 t1 [--dest DIR]    # fresh git repo with the starter, prints BRIEF + ticket + clock
  python3 loop/ai_screen.py check cb02 t1 DIR             # hidden acceptance tests + the repo's own tests + your diff
  python3 loop/ai_screen.py reveal cb02 t1                # the interviewer's notes for that ticket (after you finish)
  python3 loop/ai_screen.py time DIR                      # minutes elapsed in a started session

Open DIR in VS Code and run `claude` there: the session is the codebase, nothing else (no kit, no solution).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
ROUND = KIT / "loop" / "rounds" / "01_ai_screen"
REPO_ROOT = KIT.parents[3]  # trellis (the uv project)
DEFAULT_DEST = Path.home() / "abnormal-practice"
PLAN = [(0, "Explore: build the mental model with Claude (no code yet)"),
        (10, "Say the 60-second mental model out loud; read the ticket; ask 2-3 clarifying questions"),
        (13, "State assumptions + milestones; M1 must be demoable by ~minute 30"),
        (30, "M1 working end-to-end + a test; then M2"),
        (45, "Stop building: run everything, walk through the diff, name known gaps"),
        (60, "Questions for them")]


def _codebase(cb: str) -> Path:
    hits = sorted(ROUND.glob(f"{cb}_*"))
    if len(hits) != 1:
        sys.exit(f"unknown codebase {cb!r}; try: python3 loop/ai_screen.py list")
    return hits[0]


def _ticket(d: Path, t: str) -> Path:
    hits = sorted((d / "tickets").glob(f"{t}_*.md"))
    if len(hits) != 1:
        sys.exit(f"unknown ticket {t!r} in {d.name}: {[p.stem for p in (d / 'tickets').glob('*.md')]}")
    return hits[0]


def _git(dest: Path, *args: str) -> str:
    p = subprocess.run(["git", "-C", str(dest), *args], capture_output=True, text=True)
    return p.stdout


def cmd_list(_a) -> None:
    for d in sorted(ROUND.glob("cb*_*")):
        print(d.name)
        for t in sorted((d / "tickets").glob("*.md")):
            first = next((l.strip("# ").strip() for l in t.read_text().splitlines() if l.strip()), "")
            print(f"   {t.stem:32s} {first[:70]}")


def cmd_start(a) -> None:
    d = _codebase(a.cb)
    ticket = _ticket(d, a.t)
    stamp = dt.datetime.now().strftime("%m%d-%H%M")
    dest = Path(a.dest or DEFAULT_DEST / f"{a.cb}-{a.t}-{stamp}").expanduser().resolve()
    if dest.exists():
        sys.exit(f"{dest} exists")
    shutil.copytree(d / "starter", dest, ignore=shutil.ignore_patterns("__pycache__", "*.db", ".pytest_cache"))
    _git(dest, "init", "-q")
    _git(dest, "add", "-A")
    subprocess.run(["git", "-C", str(dest), "-c", "user.name=practice", "-c", "user.email=practice@local",
                    "commit", "-qm", "starter"], check=True)
    (dest / ".ai_screen.json").write_text(json.dumps({"cb": a.cb, "t": a.t, "started": dt.datetime.now().isoformat()}))
    _git(dest, "update-index", "--assume-unchanged", ".ai_screen.json")
    print(f"workspace: {dest}\n  code {dest}    # then `claude` in its terminal\n")
    print((d / "BRIEF.md").read_text())
    print("\n--- the ticket (read it at minute 10, not before) ---\n")
    print(ticket.read_text())
    print("--- clock ---")
    for m, what in PLAN:
        print(f"  {m:2d}' {what}")
    print(f"\nwhen done: python3 loop/ai_screen.py check {a.cb} {a.t} {dest}")


def _pytest(args: list[str], cwd: Path, env: dict) -> tuple[int, str]:
    p = subprocess.run(["uv", "run", "--project", str(REPO_ROOT), "--with", "pytest", "python", "-m", "pytest",
                        *args, "-q", "-o", "addopts=", "-p", "no:cacheprovider"], cwd=cwd, env=env, capture_output=True, text=True)
    lines = [l for l in re.sub(r"\x1b\[[0-9;]*m", "", p.stdout).splitlines() if l.strip()]
    return p.returncode, "\n".join(lines[-25:])


def cmd_check(a) -> None:
    d = _codebase(a.cb)
    _ticket(d, a.t)
    ws = Path(a.dir).expanduser().resolve()
    env = dict(os.environ, CODEBASE=str(ws))
    env.pop("IMPL", None)
    print(f"== acceptance {a.cb} {a.t} (hidden tests) against {ws}")
    for tier in ("core", "stretch", "regression"):
        rc, out = _pytest([str(d / "acceptance"), "-m", f"{a.t} and {tier}"], KIT, env)
        last = out.splitlines()[-1] if out else "(no output)"
        print(f"  {tier:10s} {'PASS' if rc == 0 else ('none' if rc == 5 else 'FAIL')}  {last}")
        if rc not in (0, 5) and a.verbose:
            print(out)
    rc, out = _pytest([], ws, dict(os.environ))
    print(f"== the repo's own test suite: {'green' if rc == 0 else 'RED'}  {out.splitlines()[-1] if out else ''}")
    diff = _git(ws, "diff", "--stat", "HEAD") + _git(ws, "status", "--short")
    added = _git(ws, "diff", "HEAD", "-U0")
    new_tests = len(re.findall(r"^\+\s*def test_", added, re.M))
    untracked = [l[3:] for l in _git(ws, "status", "--porcelain").splitlines() if l.startswith("??")]
    for f in untracked:
        p = ws / f
        files = [p] if p.is_file() else list(p.rglob("*.py")) if p.is_dir() else []
        new_tests += sum(len(re.findall(r"^\s*def test_", x.read_text(errors="ignore"), re.M)) for x in files)
    print(f"== your change\n{diff.strip() or '(nothing changed)'}\n  new test functions: {new_tests}")
    print("\n== self-score (0/1 each, honestly) — then: python3 loop/ai_screen.py reveal", a.cb, a.t)
    for q in ["Said a mental model of the system out loud by minute ~10 (entry point, data flow, extension point)",
              "Asked clarifying questions, then wrote down assumptions instead of waiting",
              "Named milestones; M1 was demoable before minute ~30",
              "Reused the existing abstractions (registry / settings / store / utils) instead of new parallel ones",
              "Told Claude what to look at (files, patterns) before asking it to write code",
              "Reviewed AI output at the right altitude and rejected or changed at least one thing",
              "Added tests in the repo's convention and ran the whole suite",
              "Demoed end-to-end through the real entry point (CLI / API), not just unit tests",
              "Closed with known gaps + what v2 would be"]:
        print(f"  [ ] {q}")


def cmd_reveal(a) -> None:
    d = _codebase(a.cb)
    text = (d / "interviewer.md").read_text()
    m = re.search(rf"^##+ [^\n]*\b{a.t}\b.*?(?=^## |\Z)", text, re.S | re.M | re.I)
    print(m.group(0) if m else text)
    print(f"\nreference walkthrough: {(d / 'walkthrough.md').relative_to(KIT)} · solution: {(d / 'solution').relative_to(KIT)}")


def cmd_time(a) -> None:
    meta = json.loads((Path(a.dir).expanduser() / ".ai_screen.json").read_text())
    mins = (dt.datetime.now() - dt.datetime.fromisoformat(meta["started"])).total_seconds() / 60
    now = max((m, w) for m, w in PLAN if m <= mins)
    print(f"{mins:.0f}' elapsed · now: {now[1]}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list").set_defaults(fn=cmd_list)
    s = sub.add_parser("start"); s.add_argument("cb"); s.add_argument("t"); s.add_argument("--dest"); s.set_defaults(fn=cmd_start)
    c = sub.add_parser("check"); c.add_argument("cb"); c.add_argument("t"); c.add_argument("dir"); c.add_argument("-v", "--verbose", action="store_true"); c.set_defaults(fn=cmd_check)
    r = sub.add_parser("reveal"); r.add_argument("cb"); r.add_argument("t"); r.set_defaults(fn=cmd_reveal)
    t = sub.add_parser("time"); t.add_argument("dir"); t.set_defaults(fn=cmd_time)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
