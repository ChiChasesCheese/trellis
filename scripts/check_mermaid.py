#!/usr/bin/env python3
"""Render every mermaid diagram on the changed markdown pages; a diagram that does not render fails the build.

    python3 scripts/check_mermaid.py --base origin/main      # pages changed since the merge base (CI)
    python3 scripts/check_mermaid.py page.md [dir ...]       # explicit pages / folders
    python3 scripts/check_mermaid.py --list --base HEAD~5    # which pages have diagrams, render nothing

Each ```mermaid block is cut out and rendered with `npx -y @mermaid-js/mermaid-cli@$MERMAID_CLI_VERSION` (headless
Chrome; needs Node and network on first use). Web clippings (`*/clippings/*`) are skipped. $MMDC replaces the command
(e.g. `MMDC=mmdc`). Obsidian ships its own mermaid, so a pass here means "valid mermaid", not "pixel-identical".
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from changed_learning_pages import REPO, changed_files  # noqa: E402

VERSION = os.environ.get("MERMAID_CLI_VERSION", "12.0.0")
BLOCK = re.compile(r"^```mermaid[ \t]*\n(.*?)^```[ \t]*$", re.S | re.M)


def pages(args: list[str], base: str | None) -> list[Path]:
    if args:
        out: list[Path] = []
        for a in args:
            p = Path(a)
            out += sorted(p.rglob("*.md")) if p.is_dir() else [p]
    else:
        out = [REPO / f for f in changed_files(base) if f.endswith(".md") and (REPO / f).is_file()]
    return [p for p in out if "clippings" not in p.parts]


def shown(p: Path) -> str:
    return str(p.resolve().relative_to(REPO)) if p.resolve().is_relative_to(REPO) else str(p)


def blocks(page: Path) -> list[tuple[int, str]]:
    text = page.read_text(encoding="utf-8")
    return [(text[:m.start()].count("\n") + 1, m.group(1)) for m in BLOCK.finditer(text)]


def render(job: tuple[Path, int, str, Path, list[str]]) -> tuple[Path, int, str | None]:
    page, line, src, cfg, mmdc = job
    with tempfile.TemporaryDirectory() as tmp:
        mmd, svg = Path(tmp) / "d.mmd", Path(tmp) / "d.svg"
        mmd.write_text(src, encoding="utf-8")
        p = subprocess.run([*mmdc, "-q", "-p", str(cfg), "-i", str(mmd), "-o", str(svg)], capture_output=True, text=True)
        if p.returncode != 0 or not svg.is_file():
            err = [ln for ln in (p.stderr + p.stdout).strip().splitlines() if ln.strip()]
            return page, line, " | ".join(err[:4]) or f"exit {p.returncode}"
    return page, line, None


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", help="markdown files or folders (default: pages changed vs --base)")
    ap.add_argument("--base", help="git ref to compare against (REF...HEAD); default: working tree vs HEAD")
    ap.add_argument("--list", action="store_true", help="list pages with diagrams and block counts, render nothing")
    ap.add_argument("--jobs", type=int, default=3, help="parallel renders (each starts a headless browser)")
    a = ap.parse_args(argv)
    found = [(p, b) for p in pages(a.paths, a.base) if (b := blocks(p))]
    total = sum(len(b) for _, b in found)
    if a.list or not found:
        for p, b in found:
            print(f"{len(b):3d}  {shown(p)}")
        print(f"{total} diagram(s) on {len(found)} page(s)")
        return 0
    mmdc = shlex.split(os.environ.get("MMDC", f"npx -y @mermaid-js/mermaid-cli@{VERSION}"))
    with tempfile.TemporaryDirectory() as td:
        cfg = Path(td) / "puppeteer.json"   # CI containers and Ubuntu 24.04 forbid the Chrome sandbox
        cfg.write_text(json.dumps({"args": ["--no-sandbox", "--disable-setuid-sandbox"]}), encoding="utf-8")
        jobs = [(p, line, src, cfg, mmdc) for p, b in found for line, src in b]
        bad = 0
        with ThreadPoolExecutor(max_workers=a.jobs) as ex:
            for page, line, err in ex.map(render, jobs):
                if err:
                    bad += 1
                    print(f"FAIL {shown(page)}:{line}  {err}")
    print(f"{total - bad}/{total} diagram(s) render on {len(found)} page(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
