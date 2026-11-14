from __future__ import annotations

import os
import shlex
import sys
import time

import pytest


def py(code: str) -> str:
    return f"{shlex.quote(sys.executable)} -c {shlex.quote(code)}"


def counter_cmd(path, fail_times: int, code: int = 75) -> str:
    """Exits `code` the first `fail_times` calls, then 0. State lives in a file, since every attempt is a new process."""
    return py(f"import pathlib,sys; p=pathlib.Path({str(path)!r}); n=int(p.read_text()) if p.exists() else 0; "
              f"p.write_text(str(n+1)); sys.exit({code} if n < {fail_times} else 0)")


def alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def max_overlap(intervals) -> int:
    events = sorted([(s, 1) for s, _ in intervals] + [(e, -1) for _, e in intervals])
    best = cur = 0
    for _, d in events:
        cur += d
        best = max(best, cur)
    return best


# ---------------------------------------------------------------- Part 1: one command


@pytest.mark.part1
def test_pass_and_fail_and_output(impl):
    a = impl.run_once(py("print('hello'); import sys; print('oops', file=sys.stderr)"), timeout=10)
    assert (a.returncode, a.timed_out) == (0, False)
    assert "hello" in a.output and "oops" in a.output  # stderr is kept too
    b = impl.run_once(py("import sys; sys.exit(3)"), timeout=10)
    assert (b.returncode, b.timed_out) == (3, False)
    assert impl.run_once("exit 7", timeout=10).returncode == 7  # it is a shell command


@pytest.mark.part1
def test_timeout_returns_on_time(impl):
    t0 = time.monotonic()
    a = impl.run_once(py("import time; time.sleep(30)"), timeout=0.5)
    assert a.timed_out and a.returncode is None
    assert time.monotonic() - t0 < 3
    assert 0.4 < a.seconds < 3


@pytest.mark.part1
def test_timeout_kills_grandchildren(impl, tmp_path):
    pid_file = tmp_path / "grandchild.pid"
    cmd = py("import subprocess,sys,time; "
             "c=subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)']); "
             f"open({str(pid_file)!r},'w').write(str(c.pid)); time.sleep(30)")
    a = impl.run_once(cmd, timeout=1.0)
    assert a.timed_out
    pid = int(pid_file.read_text())
    deadline = time.monotonic() + 3
    while alive(pid) and time.monotonic() < deadline:
        time.sleep(0.05)
    assert not alive(pid), "the grandchild survived: kill the process group, not just the shell"


@pytest.mark.part1
def test_big_output_does_not_deadlock(impl):
    a = impl.run_once(py("import sys; sys.stdout.write('line\\n' * 200000); print('END')"), timeout=10)
    assert a.returncode == 0 and not a.timed_out
    assert a.output.rstrip().endswith("END") and len(a.output) <= 2000


# ---------------------------------------------------------------- Part 2: retries


@pytest.mark.part2
def test_transient_code_is_retried_until_it_passes(impl, tmp_path):
    r = impl.run_with_retries("dev", counter_cmd(tmp_path / "c", 2), 10, retries=2, transient=frozenset({75}))
    assert r.status == "pass" and r.returncode == 0 and len(r.attempts) == 3


@pytest.mark.part2
def test_retries_run_out(impl, tmp_path):
    r = impl.run_with_retries("dev", counter_cmd(tmp_path / "c", 5), 10, retries=1, transient=frozenset({75}))
    assert r.status == "fail" and r.returncode == 75 and len(r.attempts) == 2


@pytest.mark.part2
def test_real_failure_is_not_retried(impl, tmp_path):
    r = impl.run_with_retries("bug", counter_cmd(tmp_path / "c", 5, code=1), 10, retries=3,
                              transient=frozenset({75}))
    assert r.status == "fail" and r.returncode == 1 and len(r.attempts) == 1
    r = impl.run_with_retries("dev", counter_cmd(tmp_path / "d", 5), 10, retries=3, transient=frozenset())
    assert len(r.attempts) == 1  # no transient codes configured: nothing is retried


@pytest.mark.part2
def test_timeout_is_not_retried(impl):
    r = impl.run_with_retries("hang", py("import time; time.sleep(30)"), 0.3, retries=3, transient=frozenset({75}))
    assert r.status == "timeout" and r.returncode is None and len(r.attempts) == 1


@pytest.mark.part2
def test_seconds_add_up_over_attempts(impl, tmp_path):
    slow = py("import time; time.sleep(0.2)") + " && " + counter_cmd(tmp_path / "c", 1)
    r = impl.run_with_retries("slow", slow, 10, retries=1, transient=frozenset({75}))
    assert len(r.attempts) == 2 and r.seconds == pytest.approx(sum(a.seconds for a in r.attempts))
    assert r.seconds >= 0.4


# ---------------------------------------------------------------- Part 3: bounded parallelism


def sleeper(tmp_path, i: int, secs: float) -> str:
    out = tmp_path / f"iv_{i}.txt"
    return py(f"import time; s=time.time(); time.sleep({secs}); open({str(out)!r},'w').write(f'{{s}} {{time.time()}}')")


def intervals(tmp_path):
    return [tuple(map(float, p.read_text().split())) for p in sorted(tmp_path.glob("iv_*.txt"))]


@pytest.mark.part3
def test_never_more_than_jobs_at_once(impl, tmp_path):
    cmds = [(f"t{i}", sleeper(tmp_path, i, 0.4)) for i in range(6)]
    t0 = time.monotonic()
    res = impl.run_all(cmds, jobs=2, timeout=10)
    wall = time.monotonic() - t0
    assert all(r.status == "pass" for r in res)
    assert max_overlap(intervals(tmp_path)) == 2
    assert wall >= 1.2  # 6 x 0.4 s on 2 slots


@pytest.mark.part3
def test_actually_runs_in_parallel(impl, tmp_path):
    cmds = [(f"t{i}", sleeper(tmp_path, i, 0.6)) for i in range(4)]
    t0 = time.monotonic()
    impl.run_all(cmds, jobs=4, timeout=10)
    assert time.monotonic() - t0 < 2.0  # serial would take 2.4 s
    assert max_overlap(intervals(tmp_path)) >= 3


@pytest.mark.part3
def test_results_in_input_order(impl):
    cmds = [("slow", py("import time; time.sleep(0.5)")), ("fast", py("pass")), ("fail", py("exit(2)"))]
    res = impl.run_all(cmds, jobs=3, timeout=10)
    assert [r.name for r in res] == ["slow", "fast", "fail"]
    assert [r.status for r in res] == ["pass", "pass", "fail"]


@pytest.mark.part3
def test_one_timeout_does_not_block_the_rest(impl, tmp_path):
    cmds = [("hang", py("import time; time.sleep(30)"))] + [(f"t{i}", sleeper(tmp_path, i, 0.1)) for i in range(4)]
    t0 = time.monotonic()
    res = impl.run_all(cmds, jobs=2, timeout=1.0)
    assert time.monotonic() - t0 < 4
    assert res[0].status == "timeout" and all(r.status == "pass" for r in res[1:])


# ---------------------------------------------------------------- Part 4: summary and CLI


@pytest.mark.part4
@pytest.mark.fmt
def test_summary_counts(impl, tmp_path):
    cmds = [("ok", py("pass")), ("bad", py("exit(1)")), ("hang", py("import time; time.sleep(30)")),
            ("dev", counter_cmd(tmp_path / "c", 1))]
    res = impl.run_all(cmds, jobs=4, timeout=0.8, retries=1, transient={75})
    text = impl.summarize(res, wall=1.0)
    for name in ("ok", "bad", "hang", "dev"):
        assert name in text
    last_lines = text.lower()
    assert "2 passed" in last_lines and "1 failed" in last_lines and "1 timed out" in last_lines
    assert "1 retried" in last_lines


@pytest.mark.part4
def test_cli_exit_code(impl, tmp_path, capsys):
    f = tmp_path / "cmds.txt"
    f.write_text(f"# comment\n\nok: {py('pass')}\n")
    assert impl.main([str(f), "--jobs", "2", "--timeout", "5"]) == 0
    f.write_text(f"ok: {py('pass')}\nbad: {py('exit(4)')}\n")
    assert impl.main([str(f), "--jobs", "2", "--timeout", "5"]) == 1
    assert "FAIL" in capsys.readouterr().out


@pytest.mark.part4
def test_parse_commands(impl):
    assert impl.parse_commands("a: echo x:y\n# c\n\n b : true \n") == [("a", "echo x:y"), ("b", "true")]
    with pytest.raises(ValueError):
        impl.parse_commands("no colon here")


# ---------------------------------------------------------------- edge cases


@pytest.mark.edge
def test_empty_list(impl):
    assert impl.run_all([], jobs=3, timeout=1) == []


@pytest.mark.edge
def test_bad_arguments(impl):
    with pytest.raises(ValueError):
        impl.run_all([("a", "true")], jobs=0, timeout=1)
    with pytest.raises(ValueError):
        impl.run_all([("a", "true")], jobs=1, timeout=0)
    with pytest.raises(ValueError):
        impl.run_all([("a", "true"), ("a", "false")], jobs=1, timeout=1)


@pytest.mark.edge
def test_missing_program(impl):
    r = impl.run_all([("nope", "definitely-not-a-real-program-xyz")], jobs=1, timeout=5)[0]
    assert r.status == "fail" and r.returncode == 127  # the shell's "command not found"
