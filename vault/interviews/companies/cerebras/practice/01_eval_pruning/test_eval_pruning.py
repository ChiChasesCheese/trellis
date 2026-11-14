from __future__ import annotations

from pathlib import Path

import pytest

DATA = Path(__file__).resolve().parent / "data"


def write_csv(tmp_path, text: str, name: str = "bench.csv") -> Path:
    p = tmp_path / name
    p.write_text(text.strip() + "\n")
    return p


@pytest.fixture(scope="module")
def code(impl):
    return impl.load_bench(DATA / "code_bench.csv")


@pytest.fixture(scope="module")
def longctx(impl):
    return impl.load_bench(DATA / "longctx_bench.csv")


def tiny(impl):
    # 6 samples, 3 models; easy: s0 s1 s2, hard: s3 s4 s5
    return impl.Bench(
        "tiny", [f"s{i}" for i in range(6)], ["easy"] * 3 + ["hard"] * 3,
        {"a": [1, 1, 1, 1, 1, 0], "b": [1, 1, 0, 1, 0, 0], "c": [1, 0, 0, 0, 0, 0]},
    )


# ---------------------------------------------------------------- Part 1


@pytest.mark.part1
def test_load_reads_every_model_column(code, longctx):
    assert len(code) == 300 and len(longctx) == 100
    assert code.models == ["model_a", "model_b", "model_c", "model_d"]
    assert set(code.difficulty) == {"easy", "medium", "hard"}
    assert all(v in (0.0, 1.0) for v in code.scores["model_a"])
    assert all(0.0 <= v <= 1.0 for m in longctx.models for v in longctx.scores[m])


@pytest.mark.part1
def test_new_model_column_needs_no_code(impl, tmp_path):
    p = write_csv(tmp_path, """
sample_id,difficulty,m1,m2,model_new
x1,easy,1,0,1
x2,hard,0,0,0.5
""")
    b = impl.load_bench(p)
    assert b.models == ["m1", "m2", "model_new"]
    assert impl.model_means(b) == {"m1": 0.5, "m2": 0.0, "model_new": 0.75}


@pytest.mark.part1
def test_model_means_on_subset(impl):
    b = tiny(impl)
    assert impl.model_means(b) == pytest.approx({"a": 5 / 6, "b": 3 / 6, "c": 1 / 6})
    assert impl.model_means(b, [0, 5]) == pytest.approx({"a": 0.5, "b": 0.5, "c": 0.5})
    assert impl.model_means(b, [1, 2], models=["a"]) == {"a": 1.0}


@pytest.mark.part1
def test_kendall_tau_basic(impl):
    full = {"a": 0.9, "b": 0.5, "c": 0.1}
    assert impl.kendall_tau(full, {"a": 0.8, "b": 0.6, "c": 0.2}) == pytest.approx(1.0)
    assert impl.kendall_tau(full, {"a": 0.1, "b": 0.5, "c": 0.9}) == pytest.approx(-1.0)
    # one of three pairs swapped: (2 - 1) / 3
    assert impl.kendall_tau(full, {"a": 0.4, "b": 0.5, "c": 0.1}) == pytest.approx(1 / 3)


@pytest.mark.part1
def test_kendall_tau_ties(impl):
    full = {"a": 0.5, "b": 0.5, "c": 0.1}
    assert impl.kendall_tau(full, dict(full)) == pytest.approx(1.0)  # a tie in both rankings agrees
    # (a,b) tie only on one side -> 0; (a,c) and (b,c) agree -> 2/3
    assert impl.kendall_tau(full, {"a": 0.6, "b": 0.5, "c": 0.1}) == pytest.approx(2 / 3)


@pytest.mark.part1
def test_verdict_threshold_is_inclusive(impl):
    assert impl.verdicts({"a": 0.5, "b": 0.4999, "c": 0.9}, 0.5) == {"a": True, "b": False, "c": True}


# ---------------------------------------------------------------- Part 2


@pytest.mark.part2
def test_item_stats(impl):
    p, d = impl.item_stats(tiny(impl), ["a", "b", "c"])
    assert p == pytest.approx([1, 2 / 3, 1 / 3, 2 / 3, 1 / 3, 0])
    assert d[0] == pytest.approx(0.0) and d[5] == pytest.approx(0.0)
    assert d[1] == pytest.approx(0.4714, abs=1e-4)


@pytest.mark.part2
def test_allocate_is_proportional_and_sums_to_k(impl):
    q = impl.allocate({"easy": 50, "medium": 30, "hard": 20}, 10)
    assert q == {"easy": 5, "medium": 3, "hard": 2}
    q = impl.allocate({"easy": 1, "medium": 1, "hard": 1}, 2)
    assert sum(q.values()) == 2 and max(q.values()) == 1
    assert impl.allocate({"easy": 3, "hard": 1}, 99) == {"easy": 3, "hard": 1}


@pytest.mark.part2
def test_select_subset_shape(impl, code):
    for k in (1, 10, 77, 300):
        idx = impl.select_subset(code, k)
        assert idx == sorted(set(idx)) and len(idx) == k
        assert all(0 <= i < len(code) for i in idx)
    assert len(impl.select_subset(code, 1000)) == len(code)


@pytest.mark.part2
def test_select_subset_keeps_strata_proportions(impl, code):
    k = 60
    idx = impl.select_subset(code, k)
    for tag in ("easy", "medium", "hard"):
        share_full = code.difficulty.count(tag) / len(code)
        got = sum(code.difficulty[i] == tag for i in idx)
        assert abs(got - share_full * k) <= 1


@pytest.mark.part2
def test_select_subset_spreads_difficulty(impl, code):
    # evenly spaced along hard -> easy: the subset's mean difficulty stays near the full set's
    p, _ = impl.item_stats(code, code.models)
    idx = impl.select_subset(code, 60)
    assert abs(sum(p[i] for i in idx) / len(idx) - sum(p) / len(p)) < 0.03


@pytest.mark.part2
def test_select_subset_reads_only_given_models(impl, code):
    a = impl.select_subset(code, 50, ["model_a", "model_b", "model_c"])
    wild = impl.Bench(code.name, code.sample_ids, code.difficulty,
                      {**code.scores, "model_d": [1.0 - v for v in code.scores["model_d"]]})
    assert impl.select_subset(wild, 50, ["model_a", "model_b", "model_c"]) == a


# ---------------------------------------------------------------- Part 3


@pytest.mark.part3
def test_full_set_is_a_perfect_subset(impl, code):
    r = impl.evaluate_subset(code, list(range(len(code))), 0.5)
    assert r.ok and r.size == 300 and r.n_full == 300
    assert r.tau == pytest.approx(1.0) and r.verdict_agreement == 1.0 and r.max_gap == pytest.approx(0.0)


@pytest.mark.part3
def test_evaluate_subset_flags_a_flipped_verdict(impl):
    b = tiny(impl)
    r = impl.evaluate_subset(b, [0, 1, 2], 0.6, max_gap=1.0)  # only easy samples: b jumps from 0.5 to 0.67
    assert r.verdict_agreement == pytest.approx(2 / 3) and not r.ok


@pytest.mark.part3
@pytest.mark.parametrize("name,threshold", [("code_bench", 0.5), ("longctx_bench", 0.55)])
def test_smallest_subset_passes_and_is_small(impl, name, threshold):
    b = impl.load_bench(DATA / f"{name}.csv")
    r = impl.smallest_subset(b, threshold)
    assert r.ok and r.tau == pytest.approx(1.0) and r.verdict_agreement == 1.0 and r.max_gap <= 0.05 + 1e-9
    assert r.size <= 0.5 * len(b), "a pruning method should cut at least half of this benchmark"
    assert len(r.indices) == r.size


@pytest.mark.part3
def test_smallest_subset_is_stable_from_there_up(impl, longctx):
    r = impl.smallest_subset(longctx, 0.55)
    assert not impl.evaluate_subset(longctx, impl.select_subset(longctx, r.size - 1), 0.55).ok
    for k in range(r.size, len(longctx) + 1):
        assert impl.evaluate_subset(longctx, impl.select_subset(longctx, k), 0.55).ok


# ---------------------------------------------------------------- Part 4


@pytest.mark.part4
def test_lomo_one_row_per_model(impl, longctx):
    rows = impl.leave_one_model_out(longctx, 0.55)
    assert [h.held_out for h in rows] == longctx.models
    for h in rows:
        assert 0 < h.size <= len(longctx) and len(h.indices) == h.size
        assert -1.0 <= h.tau_all <= 1.0 and h.gap >= 0


@pytest.mark.part4
def test_lomo_never_looks_at_the_held_out_model(impl, longctx):
    before = {h.held_out: h.indices for h in impl.leave_one_model_out(longctx, 0.55)}
    wild = impl.Bench(longctx.name, longctx.sample_ids, longctx.difficulty,
                      {**longctx.scores, "model_c": [1.0 - v for v in longctx.scores["model_c"]]})
    after = {h.held_out: h.indices for h in impl.leave_one_model_out(wild, 0.55)}
    assert after["model_c"] == before["model_c"]


@pytest.mark.part4
def test_lomo_held_out_numbers(impl, longctx):
    full = impl.model_means(longctx)
    for h in impl.leave_one_model_out(longctx, 0.55):
        sub = impl.model_means(longctx, h.indices)
        assert h.gap == pytest.approx(abs(full[h.held_out] - sub[h.held_out]))
        assert h.verdict_kept == ((full[h.held_out] >= 0.55) == (sub[h.held_out] >= 0.55))


# ---------------------------------------------------------------- edge cases


@pytest.mark.edge
@pytest.mark.parametrize("cell", ["1.5", "-0.1", "abc", "", "nan"])
def test_bad_score_rejected(impl, tmp_path, cell):
    p = write_csv(tmp_path, f"sample_id,difficulty,m1,m2\nx1,easy,1,{cell}\n")
    with pytest.raises(ValueError):
        impl.load_bench(p)


@pytest.mark.edge
def test_missing_metadata_column(impl, tmp_path):
    with pytest.raises(ValueError):
        impl.load_bench(write_csv(tmp_path, "sample_id,m1,m2\nx1,1,0\n"))


@pytest.mark.edge
def test_empty_and_duplicate(impl, tmp_path):
    with pytest.raises(ValueError):
        impl.load_bench(write_csv(tmp_path, "sample_id,difficulty,m1,m2"))
    with pytest.raises(ValueError):
        impl.load_bench(write_csv(tmp_path, "sample_id,difficulty,m1,m2\nx1,easy,1,0\nx1,hard,0,0\n"))


@pytest.mark.edge
def test_kendall_needs_two_models(impl):
    with pytest.raises(ValueError):
        impl.kendall_tau({"a": 0.5}, {"a": 0.4})


@pytest.mark.edge
def test_select_rejects_non_positive_k(impl, code):
    with pytest.raises(ValueError):
        impl.select_subset(code, 0)


@pytest.mark.edge
def test_lomo_needs_three_models(impl):
    b = impl.Bench("two", ["s0", "s1"], ["easy", "hard"], {"a": [1, 0], "b": [0, 0]})
    with pytest.raises(ValueError):
        impl.leave_one_model_out(b, 0.5)


@pytest.mark.edge
def test_single_stratum_and_all_equal_scores(impl):
    b = impl.Bench("flat", [f"s{i}" for i in range(8)], ["medium"] * 8,
                   {"a": [1] * 8, "b": [1] * 8, "c": [0] * 8})
    r = impl.smallest_subset(b, 0.5)
    assert r.ok and r.size == 1  # nothing to separate: any one sample keeps ranking and verdicts
