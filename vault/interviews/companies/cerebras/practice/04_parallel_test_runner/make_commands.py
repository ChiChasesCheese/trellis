"""Write commands.txt: a small list of fake "tests" made of tiny Python commands, for trying the runner by hand.

    uv run --project <repo root> python make_commands.py
    uv run --project <repo root> python solution.py commands.txt --jobs 3 --timeout 2 --retries 2 --transient 75

What each one does:
- fast_pass, slow_pass  exit 0 after 0.1 s / 0.8 s
- real_fail             exit 1 (a real failure: must not be retried)
- flaky_device          exit 75 ("try again") the first two times, then 0; needs --retries 2 to pass
- hang                  starts a child that sleeps 30 s and then sleeps itself: the timeout must kill both
- noisy                 writes 200 000 lines (1 MB) (a runner that does not drain the pipe hangs here)
"""
from __future__ import annotations

import shlex
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def py(code: str) -> str:
    return f"{shlex.quote(sys.executable)} -c {shlex.quote(code)}"


def commands(state_dir: Path) -> list[tuple[str, str]]:
    counter = state_dir / "flaky_device.count"
    flaky = (f"import pathlib,sys; p=pathlib.Path({str(counter)!r}); n=int(p.read_text()) if p.exists() else 0; "
             f"p.write_text(str(n+1)); sys.exit(75 if n < 2 else 0)")
    hang = ("import subprocess,sys,time; subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)']); "
            "time.sleep(30)")
    return [
        ("fast_pass", py("import time; time.sleep(0.1)")),
        ("slow_pass", py("import time; time.sleep(0.8)")),
        ("real_fail", py("import sys; print('assert 1 == 2'); sys.exit(1)")),
        ("flaky_device", py(flaky)),
        ("hang", py(hang)),
        ("noisy", py("import sys; sys.stdout.write('line\\n' * 200000)")),
    ]


if __name__ == "__main__":
    state = Path(tempfile.mkdtemp(prefix="runner-"))  # holds flaky_device's attempt counter
    lines = [f"{n}: {c}" for n, c in commands(state)]
    (HERE / "commands.txt").write_text("\n".join(lines) + "\n")
    print("wrote commands.txt")
