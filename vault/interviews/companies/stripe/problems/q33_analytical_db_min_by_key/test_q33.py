import json
import random

import pytest

EX2 = [{"b": 1}, {"b": -2}, {"a": 10}]
EX3 = [{}, {"a": 10, "b": -10}, {}, {"a": 3, "c": 3}]


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_verbatim_min_by_key_asserts(impl):
    assert impl.min_by_key("a", [{"a": 1, "b": 2}, {"a": 2}]) == {"a": 1, "b": 2}
    assert impl.min_by_key("a", [{"a": 2}, {"a": 1, "b": 2}]) == {"a": 1, "b": 2}
    assert impl.min_by_key("b", [{"a": 1, "b": 2}, {"a": 2}]) == {"a": 2}
    assert impl.min_by_key("a", [{}]) == {}
    assert impl.min_by_key("b", [{"a": -1}, {"b": -1}]) == {"b": -1}
    assert impl.min_by_key("a", []) is None


@pytest.mark.part1
def test_min_returns_the_same_object_and_does_not_mutate(impl):
    recs = [{"a": 1, "b": 2}, {"a": 2}]
    assert impl.min_by_key("a", recs) is recs[0]
    assert recs == [{"a": 1, "b": 2}, {"a": 2}]


@pytest.mark.part1
@pytest.mark.edge
def test_missing_key_is_zero_between_negative_and_positive(impl):
    assert impl.min_by_key("a", [{"a": 1}, {}, {"a": -1}]) == {"a": -1}
    assert impl.min_by_key("a", [{"a": 1}, {}, {"a": 2}]) == {}
    assert impl.min_by_key("a", [{"a": 0}, {}]) == {"a": 0}        # tie -> first
    assert impl.min_by_key("a", [{}, {"a": 0}]) == {}


@pytest.mark.part1
@pytest.mark.edge
def test_ties_return_first_in_input_order(impl):
    recs = [{"a": 5, "id": 1}, {"a": 5, "id": 2}, {"a": 5, "id": 3}]
    assert impl.min_by_key("a", recs) == {"a": 5, "id": 1}


@pytest.mark.part1
def test_part1_stdin_lines(impl):
    assert impl.part1(["MIN a", '{"a": 1, "b": 2}', '{"a": 2}']) == ['{"a": 1, "b": 2}']
    assert impl.part1(["MIN b", '{"a": 1, "b": 2}', '{"a": 2}']) == ['{"a": 2}']
    assert impl.part1(["MIN b", '{"a": -1}', '{"b": -1}']) == ['{"b": -1}']
    assert impl.part1(["MIN a"]) == ["null"]
    assert impl.part1([]) == []


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_verbatim_first_by_key_asserts(impl):
    assert impl.first_by_key("a", "asc", [{"a": 1}]) == {"a": 1}
    assert impl.first_by_key("a", "asc", EX2) in [{"b": 1}, {"b": -2}]
    assert impl.first_by_key("a", "asc", EX2) == EX2[0]          # notebook: first of the tie
    assert impl.first_by_key("a", "desc", EX2) == {"a": 10}
    assert impl.first_by_key("b", "asc", EX2) == {"b": -2}
    assert impl.first_by_key("b", "desc", EX2) == {"b": 1}
    assert impl.first_by_key("a", "desc", EX3) == {"a": 10, "b": -10}


@pytest.mark.part2
@pytest.mark.edge
def test_desc_ties_first_and_missing_key_max(impl):
    assert impl.first_by_key("a", "desc", [{"a": -1}, {}, {"a": -3}]) == {}         # 0 is the max
    assert impl.first_by_key("a", "desc", [{"a": 7, "i": 1}, {"a": 7, "i": 2}]) == {"a": 7, "i": 1}
    assert impl.first_by_key("a", "desc", []) is None
    assert impl.first_by_key("zzz", "desc", [{"a": 1}, {"b": 2}]) == {"a": 1}       # all 0 -> first


@pytest.mark.part2
def test_min_by_key_is_first_by_key_asc(impl):
    rng = random.Random(3)
    recs = [{rng.choice("abc"): rng.randrange(-5, 6)} for _ in range(200)]
    for key in "abc":
        assert impl.min_by_key(key, recs) is impl.first_by_key(key, "asc", recs)


@pytest.mark.part2
@pytest.mark.fmt
def test_part2_stdin_example_and_invalid_direction(impl):
    lines = ["FIRST a asc", "FIRST a desc", "FIRST b asc", "FIRST b desc", '{"b": 1}', '{"b": -2}', '{"a": 10}']
    assert impl.part2(lines) == ['{"b": 1}', '{"a": 10}', '{"b": -2}', '{"b": 1}']
    assert impl.part2(["FIRST a up", '{"a": 1}']) == ["INVALID_DIRECTION"]
    assert impl.part2(["FIRST a desc", "{}", '{"a": 10, "b": -10}', "{}", '{"a": 3, "c": 3}']) == ['{"a": 10, "b": -10}']


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_verbatim_comparator_asserts(impl):
    cmp = impl.Comparator("a", "asc")
    assert cmp.compare({"a": 1}, {"a": 2}) == -1
    assert cmp.compare({"a": 2}, {"a": 1}) == 1
    assert cmp.compare({"a": 1}, {"a": 1}) == 0
    assert impl.RecordComparator is impl.Comparator or impl.RecordComparator("a", "asc").compare({"a": 1}, {"a": 2}) == -1


@pytest.mark.part3
@pytest.mark.edge
def test_comparator_desc_missing_and_antisymmetry(impl):
    d = impl.RecordComparator("a", "desc")
    assert d.compare({"a": 1}, {"a": 2}) == 1
    assert d.compare({"a": 2}, {"a": 1}) == -1
    assert d.compare({}, {"a": -1}) == -1          # 0 > -1 -> comes first in desc
    assert d.compare({}, {}) == 0
    a = impl.RecordComparator("a", "asc")
    for x, y in [({"a": -3}, {}), ({}, {"a": 3}), ({"a": 10**18}, {"a": -(10**18)}), ({"b": 1}, {"c": 1})]:
        assert a.compare(x, y) == -a.compare(y, x)
        assert d.compare(x, y) == -a.compare(x, y)


@pytest.mark.part3
@pytest.mark.edge
def test_invalid_direction_raises_and_functional_flavour(impl):
    with pytest.raises(ValueError):
        impl.RecordComparator("a", "ascending")
    f = impl.make_comparator("a", "asc")
    assert f({"a": 1}, {"a": 2}) == -1


@pytest.mark.part3
def test_part3_stdin_compare_first_two_records(impl):
    assert impl.part3(["COMPARE a asc", '{"a": 1}', '{"a": 2}']) == ["-1"]
    assert impl.part3(["COMPARE a asc", '{"a": 2}', '{"a": 1}']) == ["1"]
    assert impl.part3(["COMPARE a desc", '{"a": 1}', '{"a": 1}', '{"a": 99}']) == ["0"]
    assert impl.part3(["COMPARE a asc", '{"a": 1}']) == []          # fewer than two records: no answer


# ---------------------------------------------------------------- Part 4
@pytest.mark.part4
def test_sort_by_example_and_top_k(impl):
    recs = [{"a": 2, "b": 1}, {"a": 1, "b": 3}, {"a": 1, "b": 5}, {"b": 9}]
    assert impl.sort_by([("a", "asc"), ("b", "desc")], recs) == [{"b": 9}, {"a": 1, "b": 5}, {"a": 1, "b": 3}, {"a": 2, "b": 1}]
    assert impl.top_k([("a", "asc"), ("b", "desc")], 2, recs) == [{"b": 9}, {"a": 1, "b": 5}]
    assert impl.top_k([("a", "asc")], 0, recs) == []
    assert impl.top_k([("a", "asc")], 99, recs) == impl.sort_by([("a", "asc")], recs)
    lines = ["SORT a:asc,b:desc", "TOP 2 a:asc,b:desc", '{"a": 2, "b": 1}', '{"a": 1, "b": 3}', '{"a": 1, "b": 5}', '{"b": 9}']
    assert impl.part4(lines) == ['{"b": 9}', '{"a": 1, "b": 5}', '{"a": 1, "b": 3}', '{"a": 2, "b": 1}', '{"b": 9}', '{"a": 1, "b": 5}']


@pytest.mark.part4
@pytest.mark.edge
def test_sort_is_stable_and_chain_only_breaks_ties(impl):
    recs = [{"a": 1, "i": 3}, {"a": 1, "i": 1}, {"a": 0, "i": 2}, {"a": 1, "i": 0}]
    assert impl.sort_by([("a", "asc")], recs) == [{"a": 0, "i": 2}, {"a": 1, "i": 3}, {"a": 1, "i": 1}, {"a": 1, "i": 0}]
    assert impl.sort_by([("a", "desc"), ("i", "asc")], recs) == [{"a": 1, "i": 0}, {"a": 1, "i": 1}, {"a": 1, "i": 3}, {"a": 0, "i": 2}]
    assert impl.sort_by([], recs) == recs                     # no specs: input order
    assert impl.sort_by([("a", "asc")], []) == []
    chain = impl.ChainedComparator([impl.RecordComparator("a", "asc"), impl.RecordComparator("i", "desc")])
    assert chain.compare({"a": 1, "i": 1}, {"a": 1, "i": 2}) == 1
    assert chain.compare({"a": 0, "i": 1}, {"a": 1, "i": 2}) == -1


@pytest.mark.part4
def test_sort_by_first_element_equals_first_by_key(impl):
    rng = random.Random(7)
    recs = [{k: rng.randrange(-3, 4) for k in rng.sample("abc", rng.randrange(0, 4))} for _ in range(300)]
    for key in "abc":
        for d in ("asc", "desc"):
            assert impl.sort_by([(key, d)], recs)[0] is impl.first_by_key(key, d, recs)


# ---------------------------------------------------------------- io / perf
@pytest.mark.part4
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script('PART 1\nMIN b\n{"a": 1, "b": 2}\n{"a": 2}\n')
    assert r.returncode == 0, r.stderr
    assert r.stdout == '{"a": 2}\n'
    r = run_script('PART 3\nCOMPARE a asc\n{"a": 1}\n\n{"a": 2}\n')
    assert r.stdout == "-1\n"
    assert run_script("PART 2\nFIRST a desc\n").stdout == "null\n"


@pytest.mark.part4
@pytest.mark.perf
def test_perf_100k_records_sort_two_keys(run_script):
    rng = random.Random(0)
    lines = ["PART 4", "MIN a", "FIRST b desc", "SORT a:asc,b:desc"]
    for _ in range(100_000):
        rec = {k: rng.randrange(-10**9, 10**9) for k in rng.sample(["a", "b", "c"], rng.randrange(0, 4))}
        lines.append(json.dumps(rec))
    r = run_script("\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == 100_002
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
