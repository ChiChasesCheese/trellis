"""Every evidence block in model_answer.md and investigation.md is reproducible: each ```-block whose first line is
`$ python3 awsim.py ...` is re-run, and every other line of the block (except `…`) must appear as a line of its output."""
from __future__ import annotations

import re
import shlex
import subprocess
import sys

import pytest

from ic01_helpers import DRILL

BLOCK = re.compile(r"```\n(.*?)```", re.S)


def blocks(doc: str):
    out = []
    for b in BLOCK.findall((DRILL / doc).read_text()):
        lines = b.rstrip("\n").split("\n")
        if lines[0].startswith("$ python3 awsim.py "):
            out.append((lines[0][2:], [l for l in lines[1:] if l.strip() and l.strip() != "…"]))
    return out


def run(cmd: str) -> str:
    argv = shlex.split(cmd)
    assert argv[:2] == ["python3", "awsim.py"]
    r = subprocess.run([sys.executable, str(DRILL / "awsim.py"), *argv[2:]], capture_output=True, text=True, cwd=DRILL,
                       env={"PATH": "", "AWSIM_ENV": str(DRILL / "env")})
    assert r.returncode == 0, (cmd, r.stderr)
    return r.stdout


MODEL = blocks("model_answer.md")


def test_model_answer_has_evidence_blocks():
    assert len(MODEL) >= 25 and all(expected for _, expected in MODEL)


@pytest.mark.parametrize("cmd,expected", MODEL, ids=[f"E{i}" for i in range(len(MODEL))])
def test_model_answer_evidence_reproduces(cmd, expected):
    got = {l.strip() for l in run(cmd).splitlines()}
    missing = [l for l in expected if l.strip() not in got]
    assert not missing, (cmd, missing)


def test_investigation_commands_all_run():
    cmds = []
    for b in BLOCK.findall((DRILL / "investigation.md").read_text()):
        cmds += [l for l in b.splitlines() if l.startswith("python3 awsim.py ")]
    assert len(cmds) >= 15
    for c in cmds:
        run(c.split("  #")[0].strip())
