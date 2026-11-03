"""计费 / 计税引擎的测试：`-k part1` 选第 1 关，依此类推。"""

import importlib
import os
import threading

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

T = 5.0


def txn(amount=10000, ts=150, merchant="m1", currency="USD", tid="t1"):
    return impl.Txn(tid, merchant, amount, currency, ts)


def std_rules(fee_bps=290, fixed=30, tax_bps=1000):
    return (impl.PercentPlusFixed("fee", fee_bps, fixed), impl.TaxOnFees("tax", tax_bps))


def engine_with_two_versions():
    e = impl.FeeEngine()
    e.publish("m1", 100, std_rules())
    e.publish("m1", 200, std_rules(fee_bps=250))
    return e


def amounts(lines):
    return [(line.rule_id, line.amount) for line in lines]


# ---- 第 1 关：版本、规则链、取整 -----------------------------------------------


def test_part1_fee_plus_tax_for_the_active_version():
    e = engine_with_two_versions()
    lines = e.quote(txn(10000, ts=150))
    assert amounts(lines) == [("fee", 320), ("tax", 32)]          # 10000 x 2.9% + 30 = 320；税 = 费用的 10%
    assert [(l.kind, l.version) for l in lines] == [("fee", 1), ("tax", 1)]


def test_part1_version_boundaries_use_bisect_right():
    e = engine_with_two_versions()
    assert amounts(e.quote(txn(ts=199))) == [("fee", 320), ("tax", 32)]       # 版本 1
    assert amounts(e.quote(txn(ts=200))) == [("fee", 280), ("tax", 28)]       # 恰好等于生效时间：属于新版本
    assert amounts(e.quote(txn(ts=10 ** 9))) == [("fee", 280), ("tax", 28)]
    assert amounts(e.quote(txn(ts=100))) == [("fee", 320), ("tax", 32)]       # 第一个版本从它的生效时间起算


def test_part1_publish_returns_increasing_version_numbers():
    e = impl.FeeEngine()
    assert e.publish("m1", 100, std_rules()) == 1
    assert e.publish("m1", 200, std_rules()) == 2
    assert e.publish("m2", 5, std_rules()) == 1                   # 版本号按商户独立计


def test_part1_rounding_is_bankers_and_happens_once_per_line():
    e = impl.FeeEngine()
    e.publish("m1", 0, (impl.PercentPlusFixed("fee", 500, 0),))
    # 5% 的 0.5、1.5、2.5、3.5 -> 取偶数：0、2、2、4（四舍五入会得 1、2、3、4）
    assert [e.quote(txn(a, ts=1))[0].amount for a in (10, 30, 50, 70)] == [0, 2, 2, 4]
    e2 = engine_with_two_versions()
    assert amounts(e2.quote(txn(500, ts=150))) == [("fee", 44), ("tax", 4)]    # 费用 44.5 -> 44；税建在已取整的 44 上 -> 4.4 -> 4


def test_part1_tax_is_computed_on_rounded_fee_lines_of_kind_fee_only():
    e = impl.FeeEngine()
    e.publish("m1", 0, (impl.PercentPlusFixed("fee-a", 500, 0), impl.PercentPlusFixed("fee-b", 500, 0),
                        impl.TaxOnFees("tax", 10_000)))
    # 每个 0.5 都取整到 0；若先加后取整会得 1
    assert amounts(e.quote(txn(10, ts=1))) == [("fee-a", 0), ("fee-b", 0), ("tax", 0)]


def test_part1_no_active_version_is_an_error_not_zero():
    e = engine_with_two_versions()
    with pytest.raises(impl.NoActiveRules):
        e.quote(txn(ts=99))
    with pytest.raises(impl.NoActiveRules):
        e.quote(txn(merchant="unknown"))
    assert issubclass(impl.NoActiveRules, LookupError)


def test_part1_publish_must_move_forward_and_failure_changes_nothing():
    e = engine_with_two_versions()
    for ts in (200, 150, 0):
        with pytest.raises(impl.StaleVersion):
            e.publish("m1", ts, std_rules(fee_bps=1))
    assert amounts(e.quote(txn(ts=300))) == [("fee", 280), ("tax", 28)]
    assert e.publish("m1", 201, std_rules()) == 3
    assert issubclass(impl.StaleVersion, ValueError) and issubclass(impl.StaleVersion, impl.BillingError)


def test_part1_merchants_are_independent():
    e = impl.FeeEngine()
    e.publish("m1", 0, std_rules())
    e.publish("m2", 1000, std_rules(fee_bps=100, fixed=0))
    assert amounts(e.quote(txn(10000, ts=500, merchant="m1"))) == [("fee", 320), ("tax", 32)]
    with pytest.raises(impl.NoActiveRules):
        e.quote(txn(10000, ts=500, merchant="m2"))


def test_part1_non_positive_amounts_produce_no_lines():
    e = impl.FeeEngine()
    e.publish("m1", 0, std_rules())
    assert e.quote(txn(0, ts=1)) == ()                               # 费用不适用，于是税也没有可建的基数
    assert e.quote(txn(-500, ts=1)) == ()


def test_part1_quote_is_a_pure_function_of_txn_and_version():
    e = engine_with_two_versions()
    t = txn(12345, ts=150)
    first = e.quote(t)
    e.publish("m1", 300, std_rules(fee_bps=1))                    # 之后发布新版本，不影响历史交易
    assert e.quote(t) == first == e.quote(t)
    assert isinstance(first, tuple)


# ---- 第 2 关：阶梯、封顶与保底 -------------------------------------------------


def test_part2_tiered_charges_each_slice_at_its_own_rate():
    e = impl.FeeEngine()
    e.publish("m1", 0, (impl.Tiered("fee", ((10000, 290), (None, 250))), impl.TaxOnFees("tax", 1000)))
    assert e.quote(txn(5000, ts=1))[0].amount == 145                  # 全在第一档
    assert e.quote(txn(10000, ts=1))[0].amount == 290                 # 正好用满第一档
    assert e.quote(txn(25000, ts=1))[0].amount == 665                 # 290 + 15000 x 2.5%
    assert e.quote(txn(25000, ts=1))[1].amount == 66                  # 税 = 66.5 -> 66（取偶数）


def test_part2_tiered_with_three_tiers_and_fixed_fee():
    r = impl.Tiered("fee", ((1000, 100), (5000, 200), (None, 300)), fixed=10)
    e = impl.FeeEngine()
    e.publish("m1", 0, (r,))
    # 1000 x 1% + 4000 x 2% + 2000 x 3% + 10 = 10 + 80 + 60 + 10
    assert e.quote(txn(7000, ts=1))[0].amount == 160
    assert e.quote(txn(1000, ts=1))[0].amount == 20
    assert e.quote(txn(1001, ts=1))[0].amount == 20                   # 超出 1 分钱 x 2% = 0.02


def test_part2_tiers_are_summed_before_rounding_once():
    e = impl.FeeEngine()
    e.publish("m1", 0, (impl.Tiered("fee", ((1000, 105), (None, 205))),))
    # 10.5 + 2.05 = 12.55 -> 13；若每档各取整会得到 10 + 2 = 12
    assert e.quote(txn(1100, ts=1))[0].amount == 13


@pytest.mark.parametrize("tiers", [
    (), ((1000, 100),), ((None, 100), (None, 200)), ((2000, 100), (1000, 200), (None, 300)),
    ((1000, 100), (1000, 200), (None, 300)),
])
def test_part2_invalid_tier_definitions_are_rejected(tiers):
    with pytest.raises(impl.InvalidRuleSet):
        impl.Tiered("fee", tiers)
    assert issubclass(impl.InvalidRuleSet, ValueError)


def test_part2_bounded_applies_cap_and_floor_to_any_rule():
    base = impl.PercentPlusFixed("pct", 290, 30)
    e = impl.FeeEngine()
    e.publish("m1", 0, (impl.Bounded("fee", base, minimum=50, maximum=500), impl.TaxOnFees("tax", 1000)))
    assert amounts(e.quote(txn(100, ts=1))) == [("fee", 50), ("tax", 5)]          # 32.9 抬到保底 50
    assert amounts(e.quote(txn(10000, ts=1))) == [("fee", 320), ("tax", 32)]      # 区间内不变
    assert amounts(e.quote(txn(100000, ts=1))) == [("fee", 500), ("tax", 50)]     # 2930 压到封顶；税建在封顶后的费用上


def test_part2_bounded_keeps_not_applicable_rules_not_applicable_and_inherits_kind():
    inner = impl.PercentPlusFixed("pct", 290, 30)
    b = impl.Bounded("fee", inner, minimum=50)
    assert b.kind == "fee"
    e = impl.FeeEngine()
    e.publish("m1", 0, (b,))
    assert e.quote(txn(0, ts=1)) == ()                                # 金额为 0：不适用，保底不会硬凑出一行


def test_part2_bounded_composes_with_tiered():
    r = impl.Bounded("fee", impl.Tiered("t", ((10000, 290), (None, 250))), maximum=400)
    e = impl.FeeEngine()
    e.publish("m1", 0, (r,))
    assert e.quote(txn(25000, ts=1))[0].amount == 400                 # 665 压到 400
    assert e.quote(txn(5000, ts=1))[0].amount == 145


# ---- 第 3 关：依赖顺序、按币种的固定费 ------------------------------------------


def test_part3_rules_are_ordered_by_needs_not_by_list_position():
    e = impl.FeeEngine()
    tax = impl.TaxOnFees("tax", 1000, needs=("fee",))
    fee = impl.PercentPlusFixed("fee", 290, 30)
    e.publish("m1", 0, (tax, fee))                                    # 税写在前面，依赖保证费用先算
    assert amounts(e.quote(txn(10000, ts=1))) == [("fee", 320), ("tax", 32)]


def test_part3_ordering_is_stable_when_there_are_no_constraints():
    e = impl.FeeEngine()
    rules = [impl.PercentPlusFixed(n, 100, 0) for n in ("c", "a", "b")]
    e.publish("m1", 0, rules)
    assert [l.rule_id for l in e.quote(txn(10000, ts=1))] == ["c", "a", "b"]
    e2 = impl.FeeEngine()
    e2.publish("m1", 0, [rules[0], impl.PercentPlusFixed("a", 100, 0, needs=("b",)), rules[2]])
    assert [l.rule_id for l in e2.quote(txn(10000, ts=1))] == ["c", "b", "a"]


def test_part3_dependency_chain_and_diamond():
    e = impl.FeeEngine()
    e.publish("m1", 0, [
        impl.PercentPlusFixed("d", 100, 0, needs=("b", "c")),
        impl.PercentPlusFixed("b", 100, 0, needs=("a",)),
        impl.PercentPlusFixed("c", 100, 0, needs=("a",)),
        impl.PercentPlusFixed("a", 100, 0),
    ])
    order = [l.rule_id for l in e.quote(txn(10000, ts=1))]
    assert order[0] == "a" and order[-1] == "d" and set(order) == {"a", "b", "c", "d"}


@pytest.mark.parametrize("rules", [
    [("a", ("b",)), ("b", ("a",))],                                   # 两个互相依赖
    [("a", ("a",))],                                                  # 依赖自己
    [("a", ("b",)), ("b", ("c",)), ("c", ("a",)), ("d", ())],         # 三角环，旁边还有一条正常规则
    [("a", ("ghost",))],                                              # 依赖不存在
    [("a", ()), ("a", ())],                                           # ID 重复
])
def test_part3_bad_rule_sets_are_rejected_at_publish_and_change_nothing(rules):
    e = impl.FeeEngine()
    e.publish("m1", 0, std_rules())
    built = [impl.PercentPlusFixed(rid, 100, 0, needs=needs) for rid, needs in rules]
    with pytest.raises(impl.InvalidRuleSet):
        e.publish("m1", 100, built)
    assert e.publish("m1", 100, std_rules()) == 2                       # 失败的发布没有占用版本号


def test_part3_fixed_fee_per_currency():
    r = impl.PercentPlusFixed("fee", 290, {"USD": 30, "JPY": 5})
    e = impl.FeeEngine()
    e.publish("m1", 0, (r,))
    assert e.quote(txn(10000, ts=1, currency="USD"))[0].amount == 320
    assert e.quote(txn(10000, ts=1, currency="JPY"))[0].amount == 295
    with pytest.raises(impl.MissingCurrency):
        e.quote(txn(10000, ts=1, currency="EUR"))
    assert issubclass(impl.MissingCurrency, LookupError)


def test_part3_per_currency_fixed_fee_works_inside_tiered_too():
    r = impl.Tiered("fee", ((None, 100),), fixed={"USD": 10})
    e = impl.FeeEngine()
    e.publish("m1", 0, (r,))
    assert e.quote(txn(10000, ts=1))[0].amount == 110
    with pytest.raises(impl.MissingCurrency):
        e.quote(txn(10000, ts=1, currency="JPY"))


def test_part3_readers_see_consistent_versions_while_publishing():
    e = impl.FeeEngine()
    e.publish("m1", 0, std_rules())
    baseline = e.quote(txn(10000, ts=5))
    stop = threading.Event()
    errors = []
    barrier = threading.Barrier(5)

    def reader():
        barrier.wait(T)
        while not stop.is_set():
            try:
                if e.quote(txn(10000, ts=5)) != baseline:
                    errors.append("history changed")
            except Exception as exc:  # noqa: BLE001
                errors.append(repr(exc))

    def publisher():
        barrier.wait(T)
        try:
            for i in range(1, 300):
                e.publish("m1", i * 10, std_rules(fee_bps=i))
        finally:
            stop.set()

    threads = [threading.Thread(target=reader, daemon=True) for _ in range(4)] + [threading.Thread(target=publisher, daemon=True)]
    [t.start() for t in threads]
    [t.join(T * 4) for t in threads]
    assert errors == []
    assert amounts(e.quote(txn(10000, ts=10_000))) == [("fee", 329), ("tax", 33)]     # 最新版本：299 bps + 30
    assert e.publish("m1", 10 ** 6, std_rules()) == 301


def test_part3_concurrent_publishes_to_one_merchant_keep_versions_dense_and_increasing():
    e = impl.FeeEngine()
    n = 8
    barrier = threading.Barrier(n)
    versions = []

    def worker(i):
        barrier.wait(T)
        try:
            versions.append(e.publish("m1", 100 + i, std_rules()))
        except impl.StaleVersion:
            pass

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n)]
    [t.start() for t in threads]
    [t.join(T) for t in threads]
    assert sorted(versions) == list(range(1, len(versions) + 1)) and len(versions) >= 1


# ---- 第 4 关（选做）：更正已发布的错误 -----------------------------------------


def test_part4_reprice_returns_only_the_differences_as_adjustment_lines():
    e = impl.FeeEngine()
    e.publish("m1", 0, std_rules(fee_bps=300))                        # 误配成 3.0%
    t = txn(10000, ts=5)
    old = e.quote(t)
    assert amounts(old) == [("fee", 330), ("tax", 33)]
    fixed = e.reprice(t, old, std_rules(fee_bps=290), version=2)
    assert fixed == (impl.Line("fee", "adjustment", 2, -10), impl.Line("tax", "adjustment", 2, -1))
    new_total = sum(l.amount for l in old) + sum(l.amount for l in fixed)
    assert new_total == 320 + 32                                      # 旧各行加调整行 = 正确的总数


def test_part4_reprice_with_no_change_is_empty_and_does_not_touch_the_engine():
    e = impl.FeeEngine()
    e.publish("m1", 0, std_rules())
    t = txn(10000, ts=5)
    old = e.quote(t)
    assert e.reprice(t, old, std_rules(), version=2) == ()
    assert e.quote(t) == old


def test_part4_reprice_handles_rules_added_and_removed():
    e = impl.FeeEngine()
    e.publish("m1", 0, (impl.PercentPlusFixed("fee", 290, 30), impl.PercentPlusFixed("legacy", 100, 0)))
    t = txn(10000, ts=5)
    old = e.quote(t)
    corrected = (impl.PercentPlusFixed("fee", 290, 30), impl.PercentPlusFixed("extra", 50, 0))
    assert e.reprice(t, old, corrected, version=3) == (
        impl.Line("extra", "adjustment", 3, 50), impl.Line("legacy", "adjustment", 3, -100))   # 按 rule_id 排序


def test_part4_reprice_validates_the_corrected_rules():
    e = impl.FeeEngine()
    e.publish("m1", 0, std_rules())
    t = txn(10000, ts=5)
    with pytest.raises(impl.InvalidRuleSet):
        e.reprice(t, e.quote(t), [impl.PercentPlusFixed("a", 100, 0, needs=("zzz",))], version=2)
