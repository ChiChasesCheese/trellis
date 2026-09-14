"""Shared pytest fixtures for the Stripe OA drill repo.

`impl` loads the module under test for the problem directory the test lives in.
By default it loads `solution.py` (the reference solution).  Set the env var
IMPL=starter to run the same test-suite against your own `starter.py` when
drilling (that's what `drill.py` does).
"""
from __future__ import annotations

import importlib.util
import os
import resource
import subprocess
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent


def _load(problem_dir: Path, name: str):
    path = problem_dir / f"{name}.py"
    if not path.exists():
        pytest.skip(f"{path} does not exist")
    spec = importlib.util.spec_from_file_location(f"{problem_dir.name}_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = mod  # so @dataclass / pickling / typing.get_type_hints can find the module
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def impl(request):
    """Module object for solution.py (or starter.py when IMPL=starter)."""
    problem_dir = Path(request.fspath).resolve().parent
    return _load(problem_dir, os.environ.get("IMPL", "solution"))


@pytest.fixture(scope="module")
def impl_path(request) -> Path:
    problem_dir = Path(request.fspath).resolve().parent
    return problem_dir / f"{os.environ.get('IMPL', 'solution')}.py"


class RunResult:
    def __init__(self, stdout: str, stderr: str, returncode: int, seconds: float, max_rss_mb: float):
        self.stdout, self.stderr, self.returncode = stdout, stderr, returncode
        self.seconds, self.max_rss_mb = seconds, max_rss_mb

    def __repr__(self):  # pragma: no cover
        return f"RunResult(rc={self.returncode}, {self.seconds:.3f}s, {self.max_rss_mb:.1f}MB)"


@pytest.fixture
def run_script(impl_path, tmp_path):
    """Run the module as a script: feed stdin, capture stdout, measure wall time + the child's own
    peak RSS (written by a tiny wrapper at exit, so runs never inherit a previous child's peak)."""

    wrapper = (
        "import atexit, os, resource, runpy, sys\n"
        "out = os.environ['STRIPE_OA_RSS_FILE']\n"
        "atexit.register(lambda: open(out, 'w').write(str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)))\n"
        "sys.argv = [sys.argv[1]]\n"
        "runpy.run_path(sys.argv[0], run_name='__main__')\n"
    )

    def _run(stdin_text: str, timeout: float = 30.0) -> RunResult:
        rss_file = tmp_path / "rss.txt"
        env = dict(os.environ, STRIPE_OA_RSS_FILE=str(rss_file))
        t0 = time.perf_counter()
        proc = subprocess.run(
            [sys.executable, "-c", wrapper, str(impl_path)],
            input=stdin_text,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(impl_path.parent),
            env=env,
        )
        seconds = time.perf_counter() - t0
        rss = int(rss_file.read_text()) if rss_file.exists() else 0
        # macOS reports ru_maxrss in bytes, Linux in KiB.
        rss_mb = rss / (1024 * 1024) if sys.platform == "darwin" else rss / 1024
        return RunResult(proc.stdout, proc.stderr, proc.returncode, seconds, rss_mb)

    return _run
