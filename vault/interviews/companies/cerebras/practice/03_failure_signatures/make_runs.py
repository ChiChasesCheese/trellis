"""Write runs/run_01.xml .. run_06.xml: six CI runs of the same suite in JUnit XML (the format pytest --junitxml,
Maven and most CI tools write). Deterministic. Messages carry run-specific noise (addresses, temp paths, ids,
timings) so that the same bug never has the same raw text twice.

    uv run --project <repo root> python make_runs.py
"""
from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import quoteattr

HERE = Path(__file__).resolve().parent
RUNS = 6


def outcome(test: str, r: int) -> tuple[str, str] | None:
    """(status, message) of a test in run r (1-based); status pass | failure | error | skipped; None = not in run."""
    addr = f"0x7f{(r * 7919) % 65536:04x}a{r}c0"
    tmp = f"/tmp/pytest-of-ci/pytest-{100 + r}/test_paths0/out_{r}.bin"
    uuid = f"{r:08x}-1b2c-4d5e-8f90-{r * 1111:012x}"
    table = {
        "tests.test_math::test_add": ("pass", ""),
        "tests.test_api::test_login": ("failure", f"AssertionError: expected 200, got 500 (request {uuid})")
        if r >= 4 else ("pass", ""),
        "tests.test_io::test_upload": ("failure", f"TimeoutError: upload took {30 + r * 0.7:.1f}s > 30s")
        if r in (2, 5) else ("pass", ""),
        "tests.test_device::test_compile": ("error", f"ConnectionRefusedError: [Errno 61] Connection refused: "
                                                     f"10.0.3.{10 + r}:8443") if r == 3 else ("pass", ""),
        "tests.test_model::test_logits": ("failure", f"AssertionError: max abs diff {0.01 * r:.4f} > 1e-3 at index "
                                                     f"{r * 13}") if r <= 2 else ("pass", ""),
        "tests.test_cache::test_eviction": ("failure", f"KeyError: 'k{r * 3}' not found in LRU at {addr}"),
        "tests.test_tmp::test_paths": ("failure", f"FileNotFoundError: [Errno 2] No such file or directory: '{tmp}'")
        if r >= 5 else ("pass", ""),
        "tests.test_mixed::test_infra_then_real": (
            ("error", "OSError: [Errno 28] No space left on device") if r == 2
            else ("failure", f"ValueError: shape mismatch ({r}, 4096) vs (4096,)") if r >= 5 else ("pass", "")),
        "tests.test_gpu::test_cuda": ("skipped", "no GPU on this runner"),
        "tests.test_new::test_feature": ("pass", "") if r >= 4 else None,
    }
    return table[test] if test in table else None


TESTS = ["tests.test_math::test_add", "tests.test_api::test_login", "tests.test_io::test_upload",
         "tests.test_device::test_compile", "tests.test_model::test_logits", "tests.test_cache::test_eviction",
         "tests.test_tmp::test_paths", "tests.test_mixed::test_infra_then_real", "tests.test_gpu::test_cuda",
         "tests.test_new::test_feature"]


def write_run(r: int) -> Path:
    cases = []
    for t in TESTS:
        o = outcome(t, r)
        if o is None:
            continue
        status, msg = o
        cls, name = t.split("::")
        head = f'    <testcase classname="{cls}" name="{name}" time="{0.05 * r + len(name) / 100:.3f}"'
        if status == "pass":
            cases.append(head + "/>")
        else:
            first = msg.split(":")[0]
            body = f"Traceback (most recent call last):\n  ...\n{msg}" if status != "skipped" else ""
            tag = f'<{status} message={quoteattr(msg)}' + (f' type="{first}"' if status != "skipped" else "")
            cases.append(f"{head}>\n      {tag}>{body}</{status}>\n    </testcase>")
    fails = sum("<failure" in c for c in cases)
    errors = sum("<error" in c for c in cases)
    skipped = sum("<skipped" in c for c in cases)
    xml = (f'<?xml version="1.0" encoding="utf-8"?>\n<testsuites>\n  <testsuite name="pytest" tests="{len(cases)}" '
           f'failures="{fails}" errors="{errors}" skipped="{skipped}" timestamp="2026-11-{r:02d}T03:00:00">\n'
           + "\n".join(cases) + "\n  </testsuite>\n</testsuites>\n")
    path = HERE / "runs" / f"run_{r:02d}.xml"
    path.parent.mkdir(exist_ok=True)
    path.write_text(xml)
    return path


if __name__ == "__main__":
    for r in range(1, RUNS + 1):
        print("wrote", write_run(r).relative_to(HERE))
