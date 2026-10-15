#!/usr/bin/env python3
"""Run every solution and every lecture code block. Exit code 0 only if all of it passes.

1. coding/solutions/*.py            each file is run alone with `python3 -I` (its own asserts must pass).
2. coding/patterns/*.md              all ```python blocks of one lecture are concatenated in order and run
                                     with `python3 -I` (so templates, helpers and traces are executable).
3. block <-> solution consistency    a lecture block whose first line is `# solutions/<file>.py` must appear
                                     verbatim inside that file's `# --- solution ---` ... `# --- end ---` region,
                                     so what the reader sees is exactly what the asserts test.
Run: python3 coding/run_all.py
"""
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOL = HERE / "solutions"
PAT = HERE / "patterns"
FENCE = re.compile(r"^```python\n(.*?)^```", re.S | re.M)
REF = re.compile(r"^# solutions/(\S+\.py)\n")


def run(path):
    t = time.time()
    p = subprocess.run([sys.executable, "-I", str(path)], capture_output=True, text=True, timeout=300)
    return p.returncode, (p.stdout + p.stderr).strip(), time.time() - t


def core(text):
    m = re.search(r"# --- solution ---\n(.*?)# --- end ---", text, re.S)
    return m.group(1) if m else None


def main():
    failures = []
    sols = sorted(SOL.glob("*.py"), key=lambda p: int(p.name.split("_")[0]))
    print(f"== solutions: {len(sols)} files")
    for f in sols:
        code, out, dt = run(f)
        last = out.splitlines()[-1] if out else ""
        ok = code == 0 and last.startswith("ok ")
        print(f"  {'PASS' if ok else 'FAIL'}  {f.name:<58} {dt:5.2f}s")
        if not ok:
            failures.append(f"{f.name}: {out[-400:]}")

    lectures = sorted(PAT.glob("*.md"))
    print(f"== lectures: {len(lectures)} files")
    total_blocks = refs = 0
    for md in lectures:
        text = md.read_text(encoding="utf-8")
        blocks = FENCE.findall(text)
        total_blocks += len(blocks)
        bad = []
        for b in blocks:
            m = REF.match(b)
            if not m:
                continue
            refs += 1
            target = SOL / m.group(1)
            if not target.exists():
                bad.append(f"missing solution file {m.group(1)}")
                continue
            body = b[m.end():].strip("\n")
            region = core(target.read_text(encoding="utf-8"))
            if region is None or body not in region:
                bad.append(f"block differs from {m.group(1)}")
        with tempfile.TemporaryDirectory() as d:
            script = Path(d) / "lecture.py"
            script.write_text("\n\n".join(blocks), encoding="utf-8")
            code, out, dt = run(script)
        ok = code == 0 and not bad
        print(f"  {'PASS' if ok else 'FAIL'}  {md.name:<46} {len(blocks):>3} blocks {dt:5.2f}s")
        if not ok:
            failures.append(f"{md.name}: {'; '.join(bad)} {out[-400:]}")

    print(f"== {len(sols)} solution files, {len(lectures)} lectures, {total_blocks} code blocks "
          f"({refs} verified verbatim against solutions)")
    if failures:
        print("FAILURES:")
        for f in failures:
            print(" -", f)
        return 1
    print("ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
