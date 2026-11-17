"""功能开关与实验分组的测试：覆盖合同每一条，含并发。"""

import copy
import importlib
import os
import threading
from hashlib import sha256

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


def expected_bucket(flag_key: str, user_id: str) -> int:
    """合同里钉死的公式，测试自己再写一遍，不依赖被测代码。"""
    return int(sha256(f"{flag_key}:{user_id}".encode("utf-8")).hexdigest(), 16) % 10000


def expected_variant(variants, rollout, bucket_number):
    upper = 0
    for v in variants:
        if v in rollout:
            upper += rollout[v] * 100
            if bucket_number < upper:
                return v
    raise AssertionError("rollout does not tile the bucket space")


def flag(**overrides):
    config = {
        "key": "search_ranker",
        "enabled": True,
        "variants": ["baseline", "candidate"],
        "default_variant": "baseline",
        "rules": [
            {"conditions": [{"attribute": "region", "op": "in", "value": ["EU", "UK"]},
                            {"attribute": "seats", "op": "gt", "value": 18}],
             "serve": "candidate"},
        ],
        "fallthrough": {"rollout": {"baseline": 80, "candidate": 20}},
    }
    config.update(overrides)
    return config


def rollout_flag(rollout, variants=("baseline", "candidate"), key="search_ranker"):
    return flag(key=key, variants=list(variants), default_variant=variants[0], rules=[],
                fallthrough={"rollout": rollout})


def one_rule_flag(condition, **overrides):
    return flag(rules=[{"conditions": [condition], "serve": "candidate"}], **overrides)


@pytest.fixture()
def svc():
    return impl.FeatureFlagService()


# ---------- 创建、读取、规范化 ----------

def test_create_returns_normalized_config_and_drops_extra_properties(svc):
    config = flag(color="red")
    config["rules"][0]["note"] = "x"
    config["rules"][0]["conditions"][0]["extra"] = 1
    config["fallthrough"]["sticky"] = True
    stored = svc.create_flag(config)
    assert stored == flag()
    assert svc.get_flag("search_ranker") == flag()


def test_rules_and_conditions_default_to_empty_lists(svc):
    config = flag()
    del config["rules"]
    assert svc.create_flag(config)["rules"] == []
    config = flag(key="k2", rules=[{"serve": "candidate"}])
    assert svc.create_flag(config)["rules"] == [{"conditions": [], "serve": "candidate"}]


def test_get_missing_is_none_and_delete_reports_existence(svc):
    assert svc.get_flag("ghost") is None
    svc.create_flag(flag())
    assert svc.delete_flag("search_ranker") is True
    assert svc.delete_flag("search_ranker") is False
    assert svc.get_flag("search_ranker") is None


def test_duplicate_key_conflicts_and_keeps_the_original(svc):
    svc.create_flag(flag())
    with pytest.raises(impl.ConflictError):
        svc.create_flag(flag(enabled=False))
    assert svc.get_flag("search_ranker")["enabled"] is True


def test_list_flags_in_creation_order_and_update_keeps_position(svc):
    for key in ("b", "a", "c"):
        svc.create_flag(flag(key=key))
    svc.update_flag("b", flag(key="b", enabled=False))
    assert [f["key"] for f in svc.list_flags()] == ["b", "a", "c"]
    svc.delete_flag("b")
    svc.create_flag(flag(key="b"))
    assert [f["key"] for f in svc.list_flags()] == ["a", "c", "b"]


def test_errors_share_one_base_class():
    for error in (impl.ValidationError, impl.NotFoundError, impl.ConflictError):
        assert issubclass(error, impl.FeatureFlagError)


# ---------- 校验矩阵 ----------

def _drop(name):
    def mutate(c):
        del c[name]
    return mutate


def _set(name, value):
    def mutate(c):
        c[name] = value
    return mutate


def _set_cond(**fields):
    def mutate(c):
        c["rules"][0]["conditions"][0].update(fields)
    return mutate


BAD_CONFIGS = {
    "key missing": _drop("key"),
    "key empty": _set("key", ""),
    "key bad chars": _set("key", "a b"),
    "key trailing newline": _set("key", "abc\n"),
    "key 65 chars": _set("key", "a" * 65),
    "key not string": _set("key", 7),
    "enabled missing": _drop("enabled"),
    "enabled not bool": _set("enabled", "true"),
    "enabled int": _set("enabled", 1),
    "variants empty": _set("variants", []),
    "variants not list": _set("variants", "baseline"),
    "variants duplicate": _set("variants", ["baseline", "baseline"]),
    "variant empty string": _set("variants", ["baseline", ""]),
    "variant not string": _set("variants", ["baseline", 3]),
    "default missing": _drop("default_variant"),
    "default undeclared": _set("default_variant", "other"),
    "rules not list": _set("rules", {}),
    "rules null": _set("rules", None),
    "rule not object": _set("rules", ["serve"]),
    "conditions not list": lambda c: c["rules"][0].update(conditions={}),
    "serve undeclared": lambda c: c["rules"][0].update(serve="other"),
    "serve missing": lambda c: c["rules"][0].pop("serve"),
    "condition not object": lambda c: c["rules"][0].update(conditions=[5]),
    "attribute empty": _set_cond(attribute=""),
    "attribute not string": _set_cond(attribute=3),
    "unknown op": _set_cond(op="regex"),
    "op missing": lambda c: c["rules"][0]["conditions"][0].pop("op"),
    "in needs list": _set_cond(op="in", value="EU"),
    "not_in needs list": _set_cond(op="not_in", value=5),
    "gt needs number": _set_cond(op="gt", value="18"),
    "gt rejects bool": _set_cond(op="gt", value=True),
    "lt needs number": _set_cond(op="lt", value=None),
    "contains needs string": _set_cond(op="contains", value=3),
    "eq rejects list": _set_cond(op="eq", value=["a"]),
    "eq rejects null": _set_cond(op="eq", value=None),
    "fallthrough missing": _drop("fallthrough"),
    "fallthrough not object": _set("fallthrough", [1]),
    "rollout missing": _set("fallthrough", {}),
    "rollout empty": _set("fallthrough", {"rollout": {}}),
    "rollout key undeclared": _set("fallthrough", {"rollout": {"baseline": 50, "other": 50}}),
    "rollout float weight": _set("fallthrough", {"rollout": {"baseline": 80.0, "candidate": 20}}),
    "rollout bool weight": _set("fallthrough", {"rollout": {"baseline": True, "candidate": 99}}),
    "rollout negative": _set("fallthrough", {"rollout": {"baseline": 110, "candidate": -10}}),
    "rollout sums to 99": _set("fallthrough", {"rollout": {"baseline": 79, "candidate": 20}}),
    "rollout sums to 101": _set("fallthrough", {"rollout": {"baseline": 81, "candidate": 20}}),
}


@pytest.mark.parametrize("name", BAD_CONFIGS)
def test_validation_matrix_create(svc, name):
    config = flag()
    BAD_CONFIGS[name](config)
    with pytest.raises(impl.ValidationError):
        svc.create_flag(config)
    assert svc.list_flags() == []


@pytest.mark.parametrize("config", [None, [], "flag", 5])
def test_config_must_be_an_object(svc, config):
    with pytest.raises(impl.ValidationError):
        svc.create_flag(config)


def test_key_boundaries_are_accepted(svc):
    for key in ("a", "A-z_9", "k" * 64):
        assert svc.create_flag(flag(key=key))["key"] == key


def test_values_at_the_edge_of_the_schema_are_accepted(svc):
    config = flag(
        variants=["baseline", "candidate", "holdout"],
        rules=[{"conditions": [{"attribute": "plan", "op": "eq", "value": True},
                               {"attribute": "n", "op": "lt", "value": 2.5},
                               {"attribute": "tags", "op": "in", "value": []},
                               {"attribute": "email", "op": "contains", "value": ""}],
                "serve": "holdout"}],
        fallthrough={"rollout": {"candidate": 100, "baseline": 0}},
    )
    assert svc.create_flag(config) == config


# ---------- 更新 ----------

def test_update_replaces_the_whole_config(svc):
    svc.create_flag(flag())
    new = flag(enabled=False, rules=[], fallthrough={"rollout": {"candidate": 100}})
    assert svc.update_flag("search_ranker", new) == new
    assert svc.get_flag("search_ranker") == new


def test_update_missing_flag_is_not_found(svc):
    with pytest.raises(impl.NotFoundError):
        svc.update_flag("ghost", flag(key="ghost"))
    assert svc.get_flag("ghost") is None


def test_update_with_a_different_body_key_is_a_validation_error(svc):
    svc.create_flag(flag())
    with pytest.raises(impl.ValidationError):
        svc.update_flag("search_ranker", flag(key="other"))
    assert svc.get_flag("other") is None and svc.get_flag("search_ranker") == flag()


def test_invalid_update_leaves_the_old_config_in_place(svc):
    svc.create_flag(flag())
    bad = flag(fallthrough={"rollout": {"baseline": 60, "candidate": 20}})
    with pytest.raises(impl.ValidationError):
        svc.update_flag("search_ranker", bad)
    assert svc.get_flag("search_ranker") == flag()


def test_update_is_visible_to_the_next_evaluation(svc):
    svc.create_flag(flag())
    attrs = {"region": "EU", "seats": 30}
    assert svc.evaluate("search_ranker", "u1", attrs) == {"value": "candidate", "reason": "RULE_MATCH", "rule_index": 0}
    svc.update_flag("search_ranker", flag(enabled=False))
    assert svc.evaluate("search_ranker", "u1", attrs) == {"value": "baseline", "reason": "DISABLED"}
    svc.update_flag("search_ranker", flag(rules=[]))
    assert svc.evaluate("search_ranker", "u1", attrs)["reason"] == "FALLTHROUGH"


# ---------- 返回值与输入隔离 ----------

def test_mutating_the_input_after_create_does_not_change_the_stored_flag(svc):
    config = flag()
    svc.create_flag(config)
    config["enabled"] = False
    config["variants"].append("extra")
    config["rules"][0]["conditions"][0]["value"].append("BR")
    config["rules"][0]["serve"] = "baseline"
    config["fallthrough"]["rollout"]["baseline"] = 0
    assert svc.get_flag("search_ranker") == flag()
    assert svc.evaluate("search_ranker", "u", {"region": "BR", "seats": 30})["reason"] == "FALLTHROUGH"


def test_mutating_any_returned_value_does_not_change_the_stored_flag(svc):
    created = svc.create_flag(flag())
    created["rules"][0]["conditions"][0]["value"].append("BR")
    created["variants"].clear()
    fetched = svc.get_flag("search_ranker")
    fetched["rules"].clear()
    fetched["fallthrough"]["rollout"]["baseline"] = 0
    listed = svc.list_flags()
    listed[0]["enabled"] = False
    listed.clear()
    updated = svc.update_flag("search_ranker", flag())
    updated["rules"][0]["serve"] = "baseline"
    assert svc.get_flag("search_ranker") == flag()
    assert len(svc.list_flags()) == 1


def test_mutating_an_evaluation_result_does_not_change_later_results(svc):
    svc.create_flag(flag())
    first = svc.evaluate("search_ranker", "u1", {"region": "EU", "seats": 30})
    first["value"] = "baseline"
    first["extra"] = 1
    assert svc.evaluate("search_ranker", "u1", {"region": "EU", "seats": 30}) == {
        "value": "candidate", "reason": "RULE_MATCH", "rule_index": 0}


def test_mutating_attributes_after_evaluate_is_harmless(svc):
    svc.create_flag(flag())
    attributes = {"region": "EU", "seats": 30}
    svc.evaluate("search_ranker", "u1", attributes)
    attributes["region"] = "FR"
    assert svc.get_flag("search_ranker") == flag()


# ---------- 求值：停用、规则 ----------

def test_disabled_flag_serves_default_variant_and_ignores_rules_and_rollout(svc):
    svc.create_flag(flag(enabled=False, default_variant="candidate"))
    assert svc.evaluate("search_ranker", "u1", {"region": "EU", "seats": 30}) == {
        "value": "candidate", "reason": "DISABLED"}


def test_default_variant_is_only_for_disabled_flags(svc):
    svc.create_flag(rollout_flag({"baseline": 0, "candidate": 100}))
    svc.update_flag("search_ranker", flag(default_variant="baseline", rules=[],
                                          fallthrough={"rollout": {"candidate": 100}}))
    assert svc.evaluate("search_ranker", "anyone") == {"value": "candidate", "reason": "FALLTHROUGH"}


def test_first_matching_rule_wins_and_reports_its_index(svc):
    svc.create_flag(flag(
        variants=["off", "on", "beta"], default_variant="off",
        rules=[{"conditions": [{"attribute": "region", "op": "eq", "value": "FR"}], "serve": "on"},
               {"conditions": [{"attribute": "seats", "op": "gt", "value": 18}], "serve": "beta"},
               {"conditions": [], "serve": "off"}],
        fallthrough={"rollout": {"off": 100}}))
    assert svc.evaluate("search_ranker", "u", {"region": "FR", "seats": 40}) == {
        "value": "on", "reason": "RULE_MATCH", "rule_index": 0}
    assert svc.evaluate("search_ranker", "u", {"region": "DE", "seats": 40}) == {
        "value": "beta", "reason": "RULE_MATCH", "rule_index": 1}
    assert svc.evaluate("search_ranker", "u", {"region": "DE", "seats": 10}) == {
        "value": "off", "reason": "RULE_MATCH", "rule_index": 2}


def test_conditions_are_anded_and_all_must_match(svc):
    svc.create_flag(flag())
    for attrs in ({"region": "EU"}, {"seats": 30}, {"region": "FR", "seats": 30}, {"region": "EU", "seats": 18}):
        assert svc.evaluate("search_ranker", "u1", attrs)["reason"] == "FALLTHROUGH"
    assert svc.evaluate("search_ranker", "u1", {"region": "UK", "seats": 19})["reason"] == "RULE_MATCH"


def test_rule_with_no_conditions_matches_everyone(svc):
    svc.create_flag(flag(rules=[{"serve": "candidate"}]))
    assert svc.evaluate("search_ranker", "u1") == {"value": "candidate", "reason": "RULE_MATCH", "rule_index": 0}


# ---------- 操作符 ----------

OPERATOR_CASES = [
    # (op, 配置值, 属性字典, 期望命中)
    ("eq", "EU", {"a": "EU"}, True),
    ("eq", "EU", {"a": "us"}, False),
    ("eq", 5, {"a": 5.0}, True),
    ("eq", 5, {"a": "5"}, False),
    ("eq", True, {"a": True}, True),
    ("eq", True, {"a": 1}, False),
    ("eq", 1, {"a": True}, False),
    ("eq", 10**23, {"a": 1e23}, False),
    ("eq", 1e23, {"a": 10**23}, False),
    ("eq", 10**23, {"a": 10**23}, True),
    ("eq", "x", {}, False),
    ("neq", "EU", {"a": "FR"}, True),
    ("neq", "EU", {"a": "EU"}, False),
    ("neq", 5, {"a": "5"}, True),
    ("neq", True, {"a": 1}, True),
    ("neq", "EU", {}, False),
    ("in", ["EU", "UK"], {"a": "UK"}, True),
    ("in", ["EU", "UK"], {"a": "FR"}, False),
    ("in", [1, 2], {"a": 2.0}, True),
    ("in", [1, 2], {"a": True}, False),
    ("in", [], {"a": "x"}, False),
    ("in", ["x"], {}, False),
    ("not_in", ["EU", "UK"], {"a": "FR"}, True),
    ("not_in", ["EU", "UK"], {"a": "EU"}, False),
    ("not_in", ["EU"], {}, False),
    ("not_in", [], {"a": "x"}, True),
    ("gt", 18, {"a": 19}, True),
    ("gt", 18, {"a": 18}, False),
    ("gt", 18, {"a": 18.5}, True),
    ("gt", 0, {"a": True}, False),
    ("gt", 18, {"a": "30"}, False),
    ("gt", 18, {"a": None}, False),
    ("gt", 18, {}, False),
    ("lt", 18, {"a": 17}, True),
    ("lt", 18, {"a": 18}, False),
    ("lt", 2, {"a": True}, False),
    ("lt", 18, {"a": [1]}, False),
    ("contains", "@corp", {"a": "me@corp.com"}, True),
    ("contains", "@corp", {"a": "me@home.com"}, False),
    ("contains", "", {"a": "anything"}, True),
    ("contains", "1", {"a": 123}, False),
    ("contains", "a", {"a": ["a"]}, False),
    ("contains", "a", {}, False),
]


@pytest.mark.parametrize("op,value,attrs,expected", OPERATOR_CASES)
def test_operator_semantics(svc, op, value, attrs, expected):
    svc.create_flag(one_rule_flag({"attribute": "a", "op": op, "value": value}))
    result = svc.evaluate("search_ranker", "u1", attrs)
    assert (result["reason"] == "RULE_MATCH") is expected


def test_attributes_never_raise_whatever_their_type(svc):
    ops = [("eq", 1), ("neq", 1), ("in", [1]), ("not_in", [1]), ("gt", 1), ("lt", 1), ("contains", "x")]
    svc.create_flag(flag(rules=[{"conditions": [{"attribute": "a", "op": op, "value": v}], "serve": "candidate"}
                                for op, v in ops]))
    for weird in (None, [1, [2]], {"k": {"n": 1}}, "", 0, -1.5, True, float("inf")):
        assert svc.evaluate("search_ranker", "u1", {"a": weird})["value"] in ("baseline", "candidate")


# ---------- 分桶与放量 ----------

def test_worked_examples_from_the_contract(svc):
    assert expected_bucket("search_ranker", "acct-1") == 468
    assert expected_bucket("search_ranker", "acct-42") == 8016
    svc.create_flag(rollout_flag({"baseline": 80, "candidate": 20}))
    assert svc.evaluate("search_ranker", "acct-1") == {"value": "baseline", "reason": "FALLTHROUGH"}
    assert svc.evaluate("search_ranker", "acct-42") == {"value": "candidate", "reason": "FALLTHROUGH"}


def test_bucket_function_matches_the_pinned_formula():
    for key, user in (("search_ranker", "acct-1"), ("other", "名字"), ("k", "a:b")):
        assert impl.bucket(key, user) == expected_bucket(key, user)


# 在 search_ranker 里恰好落在边界上的用户（桶号由测试里的公式核对）
EDGE_USERS = {0: "acct2340", 7999: "acct15988", 8000: "acct390", 9999: "acct663"}


def test_range_boundaries_are_left_closed_right_open(svc):
    for bucket_number, user in EDGE_USERS.items():
        assert expected_bucket("search_ranker", user) == bucket_number
    svc.create_flag(rollout_flag({"baseline": 80, "candidate": 20}))
    got = {b: svc.evaluate("search_ranker", u)["value"] for b, u in EDGE_USERS.items()}
    assert got == {0: "baseline", 7999: "baseline", 8000: "candidate", 9999: "candidate"}


def test_zero_percent_variant_gets_nobody_and_hundred_percent_gets_everybody(svc):
    svc.create_flag(rollout_flag({"baseline": 100, "candidate": 0}))
    assert {svc.evaluate("search_ranker", f"u{i}")["value"] for i in range(300)} == {"baseline"}
    svc.update_flag("search_ranker", rollout_flag({"candidate": 100}))
    assert {svc.evaluate("search_ranker", f"u{i}")["value"] for i in range(300)} == {"candidate"}


def test_ranges_follow_the_variants_order_not_the_rollout_key_order(svc):
    variants = ["a", "b", "c"]
    rollout = {"c": 10, "a": 50, "b": 40}  # 键顺序故意与 variants 不同
    svc.create_flag(rollout_flag(rollout, variants))
    for i in range(1500):
        user = f"user-{i}"
        want = expected_variant(variants, rollout, expected_bucket("search_ranker", user))
        assert svc.evaluate("search_ranker", user)["value"] == want


def test_assignment_is_deterministic_across_calls_and_instances():
    first, second = impl.FeatureFlagService(), impl.FeatureFlagService()
    for s in (first, second):
        s.create_flag(rollout_flag({"baseline": 50, "candidate": 50}))
    users = [f"user-{i}" for i in range(200)]
    run1 = [first.evaluate("search_ranker", u) for u in users]
    assert run1 == [first.evaluate("search_ranker", u) for u in users]
    assert run1 == [second.evaluate("search_ranker", u) for u in users]


def test_growing_a_rollout_keeps_every_user_already_assigned(svc):
    users = [f"u{i}" for i in range(3000)]
    svc.create_flag(rollout_flag({"baseline": 80, "candidate": 20}))
    before = {u: svc.evaluate("search_ranker", u)["value"] for u in users}
    svc.update_flag("search_ranker", rollout_flag({"baseline": 70, "candidate": 30}))
    after = {u: svc.evaluate("search_ranker", u)["value"] for u in users}
    assert all(after[u] == "candidate" for u in users if before[u] == "candidate")
    moved = [u for u in users if before[u] != after[u]]
    assert moved and all(7000 <= expected_bucket("search_ranker", u) < 8000 for u in moved)
    assert len(moved) == sum(1 for u in users if 7000 <= expected_bucket("search_ranker", u) < 8000)


def test_assignment_depends_on_the_flag_key(svc):
    svc.create_flag(rollout_flag({"baseline": 50, "candidate": 50}, key="flag_one"))
    svc.create_flag(rollout_flag({"baseline": 50, "candidate": 50}, key="flag_two"))
    users = [f"u{i}" for i in range(500)]
    one = [svc.evaluate("flag_one", u)["value"] for u in users]
    two = [svc.evaluate("flag_two", u)["value"] for u in users]
    assert one != two


def test_rollout_share_is_close_to_the_configured_percentage(svc):
    svc.create_flag(rollout_flag({"baseline": 80, "candidate": 20}))
    n = 10000
    treated = sum(svc.evaluate("search_ranker", f"u{i}")["value"] == "candidate" for i in range(n))
    sigma = (n * 0.2 * 0.8) ** 0.5  # 二项分布标准差，约 40
    assert abs(treated - n * 0.2) <= 5 * sigma


# ---------- 求值的输入与错误 ----------

@pytest.mark.parametrize("user_id", [None, "", 5, ["u"], {"id": 1}])
def test_user_id_must_be_a_non_empty_string(svc, user_id):
    svc.create_flag(flag())
    with pytest.raises(impl.ValidationError):
        svc.evaluate("search_ranker", user_id, {})


@pytest.mark.parametrize("attributes", ["x", [], 5, True])
def test_attributes_must_be_an_object_when_given(svc, attributes):
    svc.create_flag(flag())
    with pytest.raises(impl.ValidationError):
        svc.evaluate("search_ranker", "u1", attributes)


def test_attributes_are_optional(svc):
    svc.create_flag(flag())
    assert svc.evaluate("search_ranker", "u1")["reason"] == "FALLTHROUGH"
    assert svc.evaluate("search_ranker", "u1", None)["reason"] == "FALLTHROUGH"
    assert svc.evaluate("search_ranker", "u1", {})["reason"] == "FALLTHROUGH"


def test_missing_flag_is_not_found_but_bad_input_is_checked_first(svc):
    with pytest.raises(impl.NotFoundError):
        svc.evaluate("ghost", "u1", {})
    with pytest.raises(impl.ValidationError):
        svc.evaluate("ghost", "", {})
    with pytest.raises(impl.ValidationError):
        svc.evaluate("ghost", "u1", "oops")


def test_result_has_rule_index_only_for_rule_matches(svc):
    svc.create_flag(flag())
    matched = svc.evaluate("search_ranker", "u", {"region": "EU", "seats": 20})
    fell = svc.evaluate("search_ranker", "u", {})
    svc.update_flag("search_ranker", flag(enabled=False))
    disabled = svc.evaluate("search_ranker", "u", {})
    assert set(matched) == {"value", "reason", "rule_index"}
    assert set(fell) == {"value", "reason"} and set(disabled) == {"value", "reason"}
    assert fell["value"] in ("baseline", "candidate")


def test_served_value_is_always_a_declared_variant(svc):
    svc.create_flag(flag(variants=["red", "green", "blue"], default_variant="red", rules=[],
                         fallthrough={"rollout": {"green": 30, "blue": 70}}))
    assert {svc.evaluate("search_ranker", f"u{i}")["value"] for i in range(400)} == {"green", "blue"}


# ---------- 并发 ----------

def _run_threads(count, target):
    barrier = threading.Barrier(count, timeout=10)
    errors: list[BaseException] = []
    results: list = []

    def worker(index):
        try:
            barrier.wait()
            results.append(target(index))
        except BaseException as exc:  # noqa: BLE001 - 收集后统一断言
            errors.append(exc)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(count)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=30)
    return results, errors


def test_concurrent_creates_of_one_key_have_exactly_one_winner(svc):
    def create(_):
        try:
            svc.create_flag(flag())
            return "created"
        except impl.ConflictError:
            return "conflict"

    results, errors = _run_threads(32, create)
    assert not errors
    assert results.count("created") == 1 and results.count("conflict") == 31


def test_concurrent_deletes_of_one_key_have_exactly_one_winner(svc):
    svc.create_flag(flag())
    results, errors = _run_threads(32, lambda _: svc.delete_flag("search_ranker"))
    assert not errors and results.count(True) == 1 and results.count(False) == 31


def test_concurrent_creates_of_different_keys_all_land(svc):
    results, errors = _run_threads(40, lambda i: svc.create_flag(flag(key=f"k{i}"))["key"])
    assert not errors and len(results) == 40
    assert sorted(f["key"] for f in svc.list_flags()) == sorted(f"k{i}" for i in range(40))


def test_evaluations_during_updates_only_see_a_whole_version(svc):
    v1 = flag(variants=["x1", "z"], default_variant="z",
              rules=[{"conditions": [], "serve": "x1"}], fallthrough={"rollout": {"z": 100}})
    v2 = flag(variants=["y2", "z"], default_variant="z",
              rules=[{"conditions": [{"attribute": "never", "op": "eq", "value": 1}], "serve": "z"},
                     {"conditions": [], "serve": "y2"}],
              fallthrough={"rollout": {"z": 100}})
    svc.create_flag(v1)
    whole = {("x1", 0), ("y2", 1)}

    def work(index):
        if index == 0:
            for i in range(400):
                svc.update_flag("search_ranker", v2 if i % 2 == 0 else v1)
            return set()
        seen = set()
        for _ in range(600):
            r = svc.evaluate("search_ranker", "u1", {})
            seen.add((r["value"], r["rule_index"]))
            seen_config = svc.get_flag("search_ranker")
            assert seen_config in (v1, v2)
        return seen

    results, errors = _run_threads(7, work)
    assert not errors
    assert set().union(*results) <= whole


def test_evaluate_racing_with_delete_and_recreate_never_crashes(svc):
    svc.create_flag(flag())

    def work(index):
        outcomes = set()
        for i in range(300):
            if index == 0:
                svc.delete_flag("search_ranker")
                try:
                    svc.create_flag(flag())
                except impl.ConflictError:
                    pass
            else:
                try:
                    outcomes.add(svc.evaluate("search_ranker", f"u{i}", {})["reason"])
                except impl.NotFoundError:
                    outcomes.add("missing")
        return outcomes

    results, errors = _run_threads(5, work)
    assert not errors
    assert set().union(*results) <= {"FALLTHROUGH", "missing"}


def test_config_dicts_are_independent_between_threads(svc):
    svc.create_flag(flag())

    def mutate(index):
        for _ in range(200):
            got = svc.get_flag("search_ranker")
            got["rules"][0]["conditions"][0]["value"].append(index)
            got["variants"].append("junk")
        return True

    _, errors = _run_threads(8, mutate)
    assert not errors
    assert svc.get_flag("search_ranker") == flag()
    assert copy.deepcopy(svc.list_flags()) == [flag()]
