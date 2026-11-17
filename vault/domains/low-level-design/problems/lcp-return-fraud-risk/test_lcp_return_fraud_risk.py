import copy
import importlib
import itertools
import os
import threading
from decimal import Decimal

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

RATING_POINTS = {1: 40, 2: 30, 3: 20, 4: 10, 5: 0}
KEYS = ("rating", "value_cents", "account_age_days")


def oracle_value(cents):
    return 30 if cents >= 50_000 else 15 if cents >= 10_000 else 0


def oracle_age(days):
    return 25 if days < 30 else 10 if days < 180 else 0


def oracle_decision(score):
    return "reject" if score >= 60 else "manual_review" if score >= 30 else "approve"


def record(rating=3, value_cents=0, account_age_days=0):
    return {"rating": rating, "value_cents": value_cents, "account_age_days": account_age_days}


def assert_invalid(*args):
    with pytest.raises(impl.ServiceError) as caught:
        impl.RiskEngine().evaluate(*args)
    assert (caught.value.status, caught.value.code) == (400, "invalid_input")


# ---- 合同里的两个例子 ----

def test_readme_example_high_risk():
    assert impl.RiskEngine().evaluate(2, 50_000, 5) == {
        "score": 85, "decision": "reject", "components": {"rating": 30, "value": 30, "age": 25}}


def test_readme_example_low_risk():
    assert impl.RiskEngine().evaluate(5, 900, 400) == {
        "score": 0, "decision": "approve", "components": {"rating": 0, "value": 0, "age": 0}}


# ---- 分项：每个下界与下界前一格 ----

@pytest.mark.parametrize("rating", [1, 2, 3, 4, 5])
def test_rating_points_follow_the_table(rating):
    # 金额 0、账龄 365 让另两项都是 0，分项直接露出来
    result = impl.RiskEngine().evaluate(rating, 0, 365)
    assert result["components"] == {"rating": RATING_POINTS[rating], "value": 0, "age": 0}


@pytest.mark.parametrize("cents, points", [
    (0, 0), (1, 0), (9_999, 0), (10_000, 15), (10_001, 15), (49_999, 15), (50_000, 30), (50_001, 30), (10**18, 30)])
def test_value_points_at_every_threshold(cents, points):
    assert impl.RiskEngine().evaluate(5, cents, 365)["components"]["value"] == points


@pytest.mark.parametrize("days, points", [
    (0, 25), (1, 25), (29, 25), (30, 10), (31, 10), (179, 10), (180, 0), (181, 0), (10**9, 0)])
def test_age_points_at_every_threshold(days, points):
    assert impl.RiskEngine().evaluate(5, 0, days)["components"]["age"] == points


# ---- 总分与决定 ----

@pytest.mark.parametrize("args, score, decision", [
    ((3, 0, 100), 30, "manual_review"),        # 总分恰好 30：进入人工复核，不是通过
    ((4, 0, 29), 35, "manual_review"),
    ((4, 0, 180), 10, "approve"),
    ((5, 0, 29), 25, "approve"),              # 比 30 小一档
    ((2, 10_000, 180), 45, "manual_review"),
    ((1, 10_000, 180), 55, "manual_review"),  # 比 60 小一档
    ((3, 10_000, 0), 60, "reject"),           # 总分恰好 60：拒绝
    ((3, 50_000, 180), 50, "manual_review"),
    ((3, 50_000, 30), 60, "reject"),
])
def test_decision_bands_include_their_lower_bound(args, score, decision):
    result = impl.RiskEngine().evaluate(*args)
    assert (result["score"], result["decision"]) == (score, decision)


def test_every_combination_matches_an_independent_oracle():
    engine = impl.RiskEngine()
    cents_grid = [0, 9_999, 10_000, 49_999, 50_000, 10**12]
    days_grid = [0, 29, 30, 179, 180, 10**6]
    for rating, cents, days in itertools.product(RATING_POINTS, cents_grid, days_grid):
        parts = (RATING_POINTS[rating], oracle_value(cents), oracle_age(days))
        expected = {"score": sum(parts), "decision": oracle_decision(sum(parts)),
                    "components": dict(zip(("rating", "value", "age"), parts))}
        assert engine.evaluate(rating, cents, days) == expected, (rating, cents, days)


def test_score_is_the_plain_sum_of_the_three_components():
    result = impl.RiskEngine().evaluate(1, 10**9, 0)
    assert result["score"] == sum(result["components"].values()) == 95


def test_result_shape_and_types_are_exact():
    result = impl.RiskEngine().evaluate(2, 20_000, 40)
    assert set(result) == {"score", "decision", "components"}
    assert set(result["components"]) == {"rating", "value", "age"}
    assert type(result["score"]) is int
    assert all(type(v) is int for v in result["components"].values())
    assert type(result["decision"]) is str


# ---- 校验 ----

@pytest.mark.parametrize("rating", [0, 6, -1, 100, 10**30])
def test_rating_outside_1_to_5_is_rejected(rating):
    assert_invalid(rating, 100, 30)


@pytest.mark.parametrize("bad", [True, False, 3.0, 2.5, "3", "", None, [3], (3,), {"a": 1}, Decimal(3), b"3"])
def test_wrong_types_are_rejected_in_every_position(bad):
    assert_invalid(bad, 100, 30)
    assert_invalid(3, bad, 30)
    assert_invalid(3, 100, bad)


@pytest.mark.parametrize("args", [(3, -1, 30), (3, 100, -1), (3, -10**9, 0), (3, 0, -10**9)])
def test_negative_amounts_and_ages_are_rejected(args):
    assert_invalid(*args)


def test_booleans_are_not_integers_even_though_they_equal_them():
    assert True == 1  # noqa: E712  这正是陷阱：相等，但合同要求拒绝
    assert_invalid(True, 100, 30)
    assert_invalid(3, True, 30)
    assert_invalid(3, 100, False)


def test_huge_integers_are_valid_for_amount_and_age():
    result = impl.RiskEngine().evaluate(5, 10**100, 10**100)
    assert result["components"] == {"rating": 0, "value": 30, "age": 0}


def test_invalid_input_leaves_the_engine_usable():
    engine = impl.RiskEngine()
    with pytest.raises(impl.ServiceError):
        engine.evaluate(0, 0, 0)
    assert engine.evaluate(5, 900, 400)["score"] == 0


# ---- 批量 ----

def test_batch_results_follow_input_order_and_mix_valid_with_invalid():
    engine = impl.RiskEngine()
    records = [record(2, 50_000, 5), {"rating": 9}, record(5, 900, 400), "nope", record(0)]
    out = engine.evaluate_many(records)
    assert [o["error"] for o in out] == [None, "invalid_input", None, "invalid_input", "invalid_input"]
    assert out[0]["result"] == engine.evaluate(2, 50_000, 5)
    assert out[2]["result"] == engine.evaluate(5, 900, 400)
    assert [o["result"] for o in out if o["error"]] == [None, None, None]
    assert all(set(o) == {"result", "error"} for o in out)


def test_batch_invalid_record_carries_the_error_code_not_none():
    assert impl.RiskEngine().evaluate_many([record(0)]) == [{"result": None, "error": "invalid_input"}]


def test_batch_empty_input_returns_an_empty_list():
    assert impl.RiskEngine().evaluate_many([]) == []
    assert impl.RiskEngine().evaluate_many(iter(())) == []


@pytest.mark.parametrize("bad", [
    None, 3, "rating", [3, 100, 30], (3, 100, 30), {"rating": 3},                      # 不是字典，或缺键
    {"rating": 3, "value_cents": 100},
    {"rating": 3, "value_cents": 100, "account_age_days": 30, "note": "x"},           # 多键
    {"rating": 3, "value_cents": 100, "account_age_days": None},                       # 值无效
    {"rating": True, "value_cents": 100, "account_age_days": 30},
    {"rating": 3, "value_cents": 100.0, "account_age_days": 30},
    {"rating": 3, "value_cents": 100, "account_age_days": -1},
    {"rating": 3, "value_cents": 100, "age_days": 30},                                 # 键名不对
])
def test_batch_marks_each_kind_of_bad_record_invalid_and_keeps_going(bad):
    out = impl.RiskEngine().evaluate_many([bad, record(5, 900, 400)])
    assert out[0] == {"result": None, "error": "invalid_input"}
    assert out[1]["error"] is None and out[1]["result"]["score"] == 0


def test_batch_consumes_the_iterable_exactly_once():
    pulled = []

    def source():
        for item in (record(2, 50_000, 5), {"rating": 0}, record(5, 900, 400)):
            pulled.append(item)
            yield item

    out = impl.RiskEngine().evaluate_many(source())
    assert len(pulled) == 3 and len(out) == 3


def test_batch_does_not_swallow_errors_from_the_input_iterator():
    def source():
        yield record(5, 900, 400)
        raise RuntimeError("upstream broke")

    with pytest.raises(RuntimeError, match="upstream broke"):
        impl.RiskEngine().evaluate_many(source())


def test_batch_accepts_any_finite_iterable():
    engine = impl.RiskEngine()
    as_tuple = engine.evaluate_many((record(2, 50_000, 5),))
    as_gen = engine.evaluate_many(r for r in [record(2, 50_000, 5)])
    assert as_tuple == as_gen == [{"result": engine.evaluate(2, 50_000, 5), "error": None}]


# ---- 无状态与互不影响 ----

def test_mutating_a_result_does_not_change_later_results():
    engine = impl.RiskEngine()
    first = engine.evaluate(2, 50_000, 5)
    first["components"]["rating"] = -1
    first["decision"] = "approve"
    first["score"] = 0
    assert engine.evaluate(2, 50_000, 5) == {
        "score": 85, "decision": "reject", "components": {"rating": 30, "value": 30, "age": 25}}


def test_two_results_for_the_same_input_share_no_objects():
    engine = impl.RiskEngine()
    a, b = engine.evaluate(2, 20_000, 40), engine.evaluate(2, 20_000, 40)
    assert a == b and a is not b and a["components"] is not b["components"]


def test_batch_results_share_no_nested_objects_and_do_not_touch_the_input():
    engine = impl.RiskEngine()
    rec = record(2, 20_000, 40)
    snapshot = copy.deepcopy(rec)
    out = engine.evaluate_many([rec, rec])
    assert rec == snapshot and list(rec) == list(KEYS)
    assert out[0]["result"] == out[1]["result"]
    assert out[0]["result"]["components"] is not out[1]["result"]["components"]
    out[0]["result"]["components"]["age"] = 99
    assert out[1]["result"]["components"]["age"] == 10
    assert engine.evaluate_many([rec])[0]["result"]["components"]["age"] == 10


def test_calls_do_not_depend_on_what_ran_before_or_on_the_instance():
    one, two = impl.RiskEngine(), impl.RiskEngine()
    with pytest.raises(impl.ServiceError):
        one.evaluate(0, 0, 0)
    one.evaluate_many([{"rating": 9}, record(2, 50_000, 5)])
    assert one.evaluate(3, 10_000, 0) == two.evaluate(3, 10_000, 0)


def test_concurrent_calls_return_the_same_answers_as_sequential_calls():
    engine = impl.RiskEngine()
    cases = list(itertools.product(RATING_POINTS, [0, 10_000, 50_000], [0, 30, 180]))
    expected = {c: engine.evaluate(*c) for c in cases}
    barrier = threading.Barrier(8)
    failures = []

    def worker():
        barrier.wait()
        for _ in range(50):
            for case in cases:
                got = engine.evaluate(*case)
                if got != expected[case]:
                    failures.append((case, got))
                got["components"]["rating"] = -1  # 改自己的结果，不能影响别的线程

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert failures == []


# ---- 以下只在解答里存在的扩展（策略版本、判定记录）；骨架没有 Policy 就跳过 ----

needs_policy = pytest.mark.skipif(not hasattr(impl, "Policy"), reason="extension: versioned policy")


@needs_policy
def test_a_new_policy_version_changes_decisions_without_touching_the_engine():
    stricter = impl.Policy(
        version="v2",
        rating_points=impl.POLICY_V1.rating_points,
        value=impl.POLICY_V1.value,
        age=impl.POLICY_V1.age,
        decision=impl.Tiers.of((0, "approve"), (25, "manual_review"), (60, "reject")),
    )
    assert impl.RiskEngine().evaluate(5, 0, 29)["decision"] == "approve"
    assert impl.RiskEngine(stricter).evaluate(5, 0, 29)["decision"] == "manual_review"


@needs_policy
def test_assessment_records_inputs_and_policy_version_for_later_explanation():
    assessment = impl.RiskEngine().assess(3, 10_000, 0)
    assert (assessment.policy_version, assessment.score, assessment.decision) == ("v1", 60, "reject")
    assert assessment.explain() == "v1: rating=3→20, value=10000→15, age=0→25; score=60 → reject"


@needs_policy
def test_tiers_reject_a_table_that_does_not_start_at_zero_or_is_unsorted():
    for bounds in [(5, 10), (0, 10, 10), (0, 20, 10)]:
        with pytest.raises(ValueError):
            impl.Tiers(bounds, tuple(range(len(bounds))))
