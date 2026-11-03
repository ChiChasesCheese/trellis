#!/usr/bin/env python3
"""Every drill in plan.json has a statement, a reference that passes and an empty starter that fails.

    python3 vault/interviews/core/low-level-design/check_plan.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
BANKS = [HERE / "problems", REPO / "vault/domains/low-level-design/problems"]
DRILLS = REPO / "vault/domains/low-level-design/drills/problems"


def run(folder: Path, impl: str) -> tuple[int, str]:
    cmd = ["uv", "run", "--project", str(REPO), "--with", "pytest", "python", "-m", "pytest", str(folder), "-q",
           "-p", "no:cacheprovider", "--no-header", "--rootdir", str(folder), "-c", "/dev/null"]
    r = subprocess.run(cmd, cwd=folder, env={**os.environ, "IMPL": impl}, capture_output=True, text=True)
    return r.returncode, (r.stdout.strip().splitlines() or [""])[-1]


def main() -> int:
    plan = json.loads((HERE / "plan.json").read_text(encoding="utf-8"))
    bad = n = 0
    for stage in plan["stages"]:
        for t in stage["tasks"]:
            slug = t.get("drill")
            if not slug:
                continue
            n += 1
            src = next((b / slug for b in BANKS if (b / slug / "solution.py").exists()), None)
            if src is None:
                print("MISSING", slug)
                bad += 1
                continue
            has_statement = (src / "problem.md").exists() or (DRILLS / f"design-{slug}.md").exists()
            ref, ref_out = run(src, "solution")
            starter, starter_out = run(src, "starter")
            ok = has_statement and ref == 0 and starter != 0
            bad += not ok
            print(f"{'ok ' if ok else 'BAD'} {slug:28} ref: {ref_out[:34]:34} starter: {starter_out[:30]}")
    print(f"{n - bad}/{n} drills ok")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
