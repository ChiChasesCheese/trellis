from __future__ import annotations

from pathlib import Path

import pytest

RUNS = sorted((Path(__file__).resolve().parent / "runs").glob("run_*.xml"))


def junit(tmp_path, body: str, name: str = "r.xml") -> Path:
    p = tmp_path / name
    p.write_text(f'<?xml version="1.0"?>\n<testsuite name="s">{body}</testsuite>\n')
    return p


def hist(impl, *statuses: str, test: str = "t::x"):
    """'P', 'F' (real bug), 'I' (infra), 'S' (skip) -> one Outcome per run."""
    msg = {"P": ("pass", ""), "F": ("fail", "AssertionError: 1 != 2"), "S": ("skip", ""),
           "I": ("fail", "OSError: [Errno 28] No space left on device")}
    return [impl.Outcome(test, f"run_{i + 1:02d}", *msg[s]) for i, s in enumerate(statuses)]


# ---------------------------------------------------------------- Part 1: parse


@pytest.mark.part1
def test_parse_one_run(impl):
    out = impl.parse_junit(RUNS[4])  # run_05
    assert len(out) == 10 and all(o.run == "run_05" for o in out)
    by = {o.test: o for o in out}
    assert by["tests.test_math::test_add"].status == "pass"
    assert by["tests.test_gpu::test_cuda"].status == "skip"
    assert by["tests.test_io::test_upload"].status == "fail"
    assert by["tests.test_io::test_upload"].message == "TimeoutError: upload took 33.5s > 30s"


@pytest.mark.part1
def test_error_counts_as_fail_and_message_falls_back_to_text(impl, tmp_path):
    p = junit(tmp_path, '<testcase classname="a" name="b"><error type="E">\n\nRuntimeError: boom\nmore</error>'
                        '</testcase><testcase name="solo"/>')
    a, b = impl.parse_junit(p, run="r9")
    assert (a.test, a.status, a.message, a.run) == ("a::b", "fail", "RuntimeError: boom", "r9")
    assert (b.test, b.status) == ("solo", "pass")


@pytest.mark.part1
def test_testsuites_root_and_single_testsuite_root(impl, tmp_path):
    one = junit(tmp_path, '<testcase classname="a" name="b"/>', "one.xml")
    many = tmp_path / "many.xml"
    many.write_text('<testsuites><testsuite><testcase classname="a" name="b"/></testsuite>'
                    '<testsuite><testcase classname="c" name="d"/></testsuite></testsuites>')
    assert [o.test for o in impl.parse_junit(one)] == ["a::b"]
    assert [o.test for o in impl.parse_junit(many)] == ["a::b", "c::d"]


# ---------------------------------------------------------------- Part 2: signatures


@pytest.mark.part2
def test_same_bug_same_signature_across_runs(impl):
    a = "KeyError: 'k3' not found in LRU at 0x7f1ef3a1c0"
    b = "KeyError: 'k18' not found in LRU at 0x7fbb12a6c0"
    assert impl.signature(a) == impl.signature(b)
    assert "0x" not in impl.signature(a)


@pytest.mark.part2
def test_strips_temp_paths_ids_timestamps(impl):
    a = ("FileNotFoundError: '/tmp/pytest-of-ci/pytest-101/t0/out_1.bin' at 2026-11-01T03:00:00Z "
         "req 00000001-1b2c-4d5e-8f90-000000000457")
    b = ("FileNotFoundError: '/tmp/pytest-of-ci/pytest-245/t0/out_9.bin' at 2026-11-14 22:10:59.123 "
         "req 0000abcd-1b2c-4d5e-8f90-0000000015b3")
    assert impl.signature(a) == impl.signature(b)
    assert impl.signature("timeout after 31.2s") == impl.signature("timeout after 7s")


@pytest.mark.part2
def test_different_bugs_stay_apart(impl):
    assert impl.signature("KeyError: 'k3' missing") != impl.signature("ValueError: 'k3' missing")
    assert impl.signature("shape mismatch (3, 4)") != impl.signature("dtype mismatch (3, 4)")


@pytest.mark.part2
def test_whitespace_and_length(impl):
    assert impl.signature("  a   b\n\tc  ") == "a b c"
    assert len(impl.signature("x" * 1000)) <= 200


@pytest.mark.part2
def test_infra_patterns(impl):
    assert impl.is_infra(impl.signature("ConnectionRefusedError: [Errno 61] Connection refused: 10.0.3.13:8443"))
    assert impl.is_infra(impl.signature("OSError: [Errno 28] No space left on device"))
    assert impl.is_infra("pod OOMKilled")
    assert not impl.is_infra("AssertionError: expected 200, got 500")
    assert impl.is_infra("weird lab glitch", patterns=[r"lab glitch"])


# ---------------------------------------------------------------- Part 3: classify


@pytest.mark.part3
@pytest.mark.parametrize("seq,kind,since", [
    ("PPPPPP", "pass", None),
    ("PPPFFF", "regression", "run_04"),
    ("FFFFFF", "regression", "run_01"),
    ("PFPPFP", "flaky", None),
    ("PPPFFP", "flaky", None),
    ("FFPPPP", "fixed", "run_03"),
    ("PPIPPP", "infra", None),
    ("PIPPFF", "regression", "run_05"),
    ("PPPIFF", "regression", "run_05"),
    ("SSSSSS", "skipped", None),
    ("SPSFSF", "regression", "run_04"),
])
def test_classify_sequences(impl, seq, kind, since):
    r = impl.classify(hist(impl, *seq))
    assert (r.kind, r.since) == (kind, since)


@pytest.mark.part3
def test_counts_and_signatures(impl):
    r = impl.classify(hist(impl, *"PIPPFF"))
    assert (r.fails, r.runs) == (3, 6)  # infra failures still count as failures
    assert r.top_signature == impl.signature("AssertionError: 1 != 2")
    assert sum(r.signatures.values()) == 3
    s = impl.classify(hist(impl, *"SPSF"))
    assert (s.fails, s.runs) == (1, 2)  # skipped runs are not runs


@pytest.mark.part3
def test_analyze_the_six_runs(impl):
    got = {r.test: (r.kind, r.since) for r in impl.analyze(RUNS)}
    assert got == {
        "tests.test_math::test_add": ("pass", None),
        "tests.test_api::test_login": ("regression", "run_04"),
        "tests.test_io::test_upload": ("flaky", None),
        "tests.test_device::test_compile": ("infra", None),
        "tests.test_model::test_logits": ("fixed", "run_03"),
        "tests.test_cache::test_eviction": ("regression", "run_01"),
        "tests.test_tmp::test_paths": ("regression", "run_05"),
        "tests.test_mixed::test_infra_then_real": ("regression", "run_05"),
        "tests.test_gpu::test_cuda": ("skipped", None),
        "tests.test_new::test_feature": ("pass", None),
    }


@pytest.mark.part3
def test_one_signature_per_real_bug_in_the_runs(impl):
    by = {r.test: r for r in impl.analyze(RUNS)}
    for t in ("tests.test_api::test_login", "tests.test_cache::test_eviction", "tests.test_tmp::test_paths",
              "tests.test_io::test_upload"):
        assert len(by[t].signatures) == 1, t
    assert len(by["tests.test_mixed::test_infra_then_real"].signatures) == 2  # the infra one and the real one
    assert by["tests.test_new::test_feature"].runs == 3  # absent from the first three runs


# ---------------------------------------------------------------- Part 4: table


@pytest.mark.part4
@pytest.mark.fmt
def test_table_order_and_content(impl, capsys):
    impl.main([str(p) for p in reversed(RUNS)])  # main sorts the file names itself
    out = capsys.readouterr().out.strip().splitlines()
    body = out[1:]
    assert len(body) == 10
    kinds = [next(k for k in ("regression", "flaky", "infra", "fixed", "skipped", "pass") if f" {k} " in ln + " ")
             for ln in body]
    order = ["regression", "flaky", "infra", "fixed", "skipped", "pass"]
    assert kinds == sorted(kinds, key=order.index), "worst first"
    assert "run_04" in next(ln for ln in body if "test_login" in ln)


# ---------------------------------------------------------------- edge cases


@pytest.mark.edge
def test_malformed_xml(impl, tmp_path):
    p = tmp_path / "bad.xml"
    p.write_text("<testsuite><testcase name='x'></testsuite")
    with pytest.raises(ValueError):
        impl.parse_junit(p)


@pytest.mark.edge
def test_not_junit(impl, tmp_path):
    p = tmp_path / "other.xml"
    p.write_text("<html><body/></html>")
    with pytest.raises(ValueError):
        impl.parse_junit(p)


@pytest.mark.edge
def test_empty_suite_and_empty_message(impl, tmp_path):
    assert impl.parse_junit(junit(tmp_path, "")) == []
    (o,) = impl.parse_junit(junit(tmp_path, '<testcase name="x"><failure/></testcase>', "e.xml"))
    assert o.status == "fail" and o.message == ""
    assert impl.signature("") == ""
