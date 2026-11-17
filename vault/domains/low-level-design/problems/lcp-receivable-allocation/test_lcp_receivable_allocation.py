import importlib
import os
import random
from dataclasses import astuple
from fractions import Fraction

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))
Transaction, Receivable, Contract = impl.Transaction, impl.Receivable, impl.Contract
register, allocate = impl.register_receivables, impl.allocate_receivables

DATE = "2026-12-05"


def tx(customer, merchant, date, card, amount):
    return Transaction(customer_id=customer, merchant_id=merchant, payout_date=date, card_type=card, amount=amount)


def rec(merchant="Grocer", card="Visa", date=DATE, amount=1203):
    return Receivable(merchant_id=merchant, card_type=card, payout_date=date, amount=amount)


def con(cid, kind, value, merchant="Grocer", card="Visa", date=DATE):
    return Contract(contract_id=cid, merchant_id=merchant, payout_date=date, card_type=card, kind=kind, value=value)


def rows(result):
    """行按 (id, 卡类型, 日期, 金额) 排序，返回顺序不限。"""
    assert all(isinstance(r.amount, int) and not isinstance(r.amount, bool) for r in result)
    return sorted(astuple(r) for r in result)


def split(rows_):
    return {r[0]: r[3] for r in rows_}


# ---- 带数字的完整例子 ----

def test_worked_aggregation_across_customers():
    result = register([
        tx("P1", "Bakery", "2026-12-01", "Visa", 175),
        tx("P2", "Bakery", "2026-12-01", "Visa", 225),
        tx("P3", "Florist", "2026-12-02", "MasterCard", 90),
    ])
    assert rows(result) == [("Bakery", "Visa", "2026-12-01", 400), ("Florist", "MasterCard", "2026-12-02", 90)]


def test_worked_card_types_stay_separate():
    result = register([tx("P4", "Garage", "2026-12-03", "Visa", 35), tx("P5", "Garage", "2026-12-03", "MasterCard", 65)])
    assert rows(result) == [("Garage", "MasterCard", "2026-12-03", 65), ("Garage", "Visa", "2026-12-03", 35)]


def test_worked_partial_fixed_leaves_merchant_remainder():
    result = allocate([rec("Kiosk", date="2026-12-04", amount=800)], [con("Split1", "fixed", 250, "Kiosk", date="2026-12-04")])
    assert rows(result) == [("Kiosk", "Visa", "2026-12-04", 550), ("Split1", "Visa", "2026-12-04", 250)]


def test_worked_mixed_percentage_uses_original_amount():
    result = allocate([rec()], [con("Split2", "fixed", 350), con("Split3", "percentage", 1500)])
    assert rows(result) == [("Grocer", "Visa", DATE, 673), ("Split2", "Visa", DATE, 350), ("Split3", "Visa", DATE, 180)]


def test_worked_later_fixed_takes_what_is_left_and_merchant_row_is_zero():
    contracts = [con("Split2", "fixed", 350), con("Split3", "percentage", 1500), con("Split4", "fixed", 900)]
    assert split(rows(allocate([rec()], contracts))) == {"Split2": 350, "Split3": 180, "Split4": 673, "Grocer": 0}


# ---- 汇总 ----

def test_aggregation_key_is_exact_and_case_sensitive():
    result = register([
        tx("U1", "Bakery", "2026-12-01", "Visa", 10),
        tx("U1", "Bakery", "2026-12-01", "visa", 20),  # 卡类型大小写不同
        tx("U1", "shopA", "2026-12-01", "Visa", 30),  # 商户大小写不同
        tx("U1", "Bakery", "2026-12-02", "Visa", 40),  # 日期不同
    ])
    assert sorted(r.amount for r in result) == [10, 20, 30, 40]


def test_duplicate_rows_count_separately_and_customer_is_ignored():
    same = tx("U1", "Bakery", "2026-12-01", "Visa", 100)
    result = register([same, same, tx("U9", "Bakery", "2026-12-01", "Visa", 100)])
    assert rows(result) == [("Bakery", "Visa", "2026-12-01", 300)]


def test_empty_inputs():
    assert register([]) == []
    assert allocate([], []) == []
    assert allocate([], [con("Split1", "fixed", 5)]) == []


def test_aggregation_at_the_documented_bounds():
    big = [tx(f"U{i}", "Bakery", DATE, "Visa", 100_000) for i in range(10_000)]
    assert rows(register(big)) == [("Bakery", "Visa", DATE, 1_000_000_000)]


def test_first_seen_order_is_kept():
    result = register([tx("U", "B", DATE, "Visa", 1), tx("U", "A", DATE, "Visa", 1), tx("U", "B", DATE, "Visa", 1)])
    assert [r.merchant_id for r in result] == ["B", "A"]


# ---- 分账 ----

def test_percentage_is_of_original_not_of_remaining():
    # 原始 1203、先分走 350：按原始算 15% 是 180，按剩余 853 算只有 127
    result = split(rows(allocate([rec()], [con("F", "fixed", 350), con("P", "percentage", 1500)])))
    assert result["P"] == 180 and result["P"] != 853 * 1500 // 10_000


def test_percentage_is_floored_with_integer_arithmetic():
    # 50 分的 58% 是 29；先算 5800/10000 得到 0.58 再乘 50 会得到 28.999999999999996，取整成 28
    assert split(rows(allocate([rec(amount=50)], [con("P", "percentage", 5800)]))) == {"P": 29, "Grocer": 21}
    assert split(rows(allocate([rec(amount=1)], [con("P", "percentage", 9999)]))) == {"Grocer": 1}  # 向下取整为 0，不出行


def test_contract_rows_only_when_positive_merchant_row_always():
    contracts = [con("Z1", "fixed", 0), con("Z2", "percentage", 0), con("Z3", "percentage", 1)]  # 1 基点 * 1203 = 0.1203 -> 0
    assert rows(allocate([rec()], contracts)) == [("Grocer", "Visa", DATE, 1203)]


def test_full_assignment_leaves_a_zero_merchant_row():
    assert rows(allocate([rec(amount=700)], [con("F", "fixed", 700)])) == [("F", "Visa", DATE, 700), ("Grocer", "Visa", DATE, 0)]
    assert rows(allocate([rec(amount=700)], [con("P", "percentage", 10_000)])) == [("Grocer", "Visa", DATE, 0), ("P", "Visa", DATE, 700)]


def test_zero_amount_receivable_still_gets_its_merchant_row():
    assert rows(allocate([rec(amount=0)], [con("F", "fixed", 10)])) == [("Grocer", "Visa", DATE, 0)]


def test_contract_order_decides_who_gets_the_scarce_money():
    receivable = [rec(amount=1000)]
    first = split(rows(allocate(receivable, [con("A", "fixed", 700), con("B", "fixed", 700)])))
    second = split(rows(allocate(receivable, [con("B", "fixed", 700), con("A", "fixed", 700)])))
    assert first == {"A": 700, "B": 300, "Grocer": 0}
    assert second == {"B": 700, "A": 300, "Grocer": 0}


def test_exhausted_funds_give_later_contracts_no_row():
    contracts = [con("A", "percentage", 6000), con("B", "percentage", 6000), con("C", "fixed", 1)]
    assert split(rows(allocate([rec(amount=1000)], contracts))) == {"A": 600, "B": 400, "Grocer": 0}


def test_contracts_with_unmatched_key_are_ignored():
    contracts = [
        con("X1", "fixed", 100, merchant="Other"),
        con("X2", "fixed", 100, card="visa"),
        con("X3", "fixed", 100, date="2026-12-06"),
        con("Hit", "fixed", 100),
    ]
    assert split(rows(allocate([rec()], contracts))) == {"Hit": 100, "Grocer": 1103}


def test_each_key_is_allocated_independently():
    receivables = [rec(card="Visa", amount=1000), rec(card="MasterCard", amount=200)]
    contracts = [con("A", "fixed", 500, card="Visa"), con("B", "fixed", 500, card="MasterCard")]
    result = rows(allocate(receivables, contracts))
    assert result == [("A", "Visa", DATE, 500), ("B", "MasterCard", DATE, 200),
                      ("Grocer", "MasterCard", DATE, 0), ("Grocer", "Visa", DATE, 500)]


def test_same_merchant_contracts_are_not_merged():
    result = allocate([rec()], [con("A", "fixed", 100), con("B", "fixed", 100)])
    assert sorted(r.id for r in result) == ["A", "B", "Grocer"]


def test_empty_contracts_return_every_merchant_row():
    receivables = [rec("Bakery", amount=5), rec("Florist", amount=0)]
    assert rows(allocate(receivables, [])) == [("Bakery", "Visa", DATE, 5), ("Florist", "Visa", DATE, 0)]


def test_extreme_amounts_stay_exact():
    top = 1_000_000_000
    result = split(rows(allocate([rec(amount=top)], [con("P", "percentage", 9999), con("Q", "percentage", 10_000)])))
    assert result == {"P": top * 9999 // 10_000, "Q": top - top * 9999 // 10_000, "Grocer": 0}
    assert top * 9999 // 10_000 == 999_900_000


# ---- 输入不被修改、结果互相独立 ----

def test_inputs_are_not_changed_and_calls_are_independent():
    transactions = [tx("U2", "B", DATE, "Visa", 5), tx("U1", "A", DATE, "Visa", 7), tx("U3", "B", DATE, "Visa", 1)]
    contracts = [con("Z", "fixed", 3, merchant="B"), con("Y", "percentage", 5000, merchant="B"), con("W", "fixed", 1, merchant="A")]
    before_t, before_c = list(transactions), list(contracts)
    first = register(transactions)
    receivables_before = list(first)
    again = register(transactions)
    assert first == again and first is not again
    out1 = allocate(first, contracts)
    out2 = allocate(first, contracts)
    assert out1 == out2 and out1 is not out2
    assert transactions == before_t and contracts == before_c and first == receivables_before
    out1.clear()  # 改结果不影响输入和下一次调用
    first.append(rec())
    assert allocate(again, contracts) == out2


def test_contract_list_is_read_in_one_pass():
    class Counting(list):
        passes = 0

        def __iter__(self):
            type(self).passes += 1
            return super().__iter__()

    receivables = [rec(merchant=f"M{i}", amount=10) for i in range(50)]
    contracts = Counting(con(f"C{i}", "fixed", 1, merchant=f"M{i}") for i in range(50))
    result = allocate(receivables, contracts)
    assert len(result) == 100
    assert Counting.passes <= 2  # 每笔应收款重新扫一遍合约会是 50 遍


# ---- 与独立实现对拍：守恒与逐行核对 ----

def oracle(receivables, contracts):
    """用 Fraction 逐步模拟，写法与解答完全不同。"""
    out = {}
    for r in receivables:
        left = r.amount
        for c in contracts:
            if (c.merchant_id, c.card_type, c.payout_date) != (r.merchant_id, r.card_type, r.payout_date):
                continue
            want = c.value if c.kind == "fixed" else int(Fraction(r.amount * c.value, 10_000) // 1)
            got = min(want, left)
            left -= got
            if got > 0:
                out[(c.contract_id, r.card_type, r.payout_date)] = got
        out[(r.merchant_id, r.card_type, r.payout_date)] = left
    return out


@pytest.mark.parametrize("seed", range(40))
def test_random_cases_match_the_oracle_and_conserve_money(seed):
    rng = random.Random(seed)
    merchants, cards, dates = ["A", "B", "C"], ["Visa", "visa", "MC"], ["2026-12-01", "2026-12-02"]
    transactions = [
        tx(f"U{rng.randrange(5)}", rng.choice(merchants), rng.choice(dates), rng.choice(cards), rng.randint(1, 10**9 // 50))
        for _ in range(rng.randint(0, 40))
    ]
    receivables = register(transactions)
    contracts = [
        con(f"K{i}", rng.choice(["fixed", "percentage"]), 0, rng.choice(merchants), rng.choice(cards), rng.choice(dates))
        for i in range(rng.randint(0, 25))
    ]
    contracts = [
        Contract(c.contract_id, c.merchant_id, c.payout_date, c.card_type, c.kind,
                 rng.randint(0, 10_000) if c.kind == "percentage" else rng.randint(0, 3 * 10**7))
        for c in contracts
    ]
    result = allocate(receivables, contracts)
    expected = oracle(receivables, contracts)
    assert {(r.id, r.card_type, r.payout_date): r.amount for r in result} == expected
    assert len(result) == len(expected)  # 没有重复行
    assert sum(r.amount for r in result) == sum(r.amount for r in receivables)
    assert all(r.amount >= 0 for r in result)
    ids = {r.id for r in result}
    assert {r.merchant_id for r in receivables} <= ids  # 每笔应收款都有商户行


def test_ten_thousand_by_ten_thousand_is_exact():
    receivables = [rec(merchant=f"M{i}", amount=1_000 + i) for i in range(10_000)]
    contracts = [con(f"C{i}", "percentage", 2500 + i % 7, merchant=f"M{i}") for i in range(10_000)]
    result = allocate(receivables, contracts)
    assert len(result) == 20_000
    assert sum(r.amount for r in result) == sum(r.amount for r in receivables)
    assert {(r.id, r.card_type, r.payout_date): r.amount for r in result} == oracle(receivables, contracts)


# ---- 解答自己的安全设计（starter 没有这些名字时跳过）----

needs_funds = pytest.mark.skipif(not hasattr(impl, "Funds"), reason="the learner's design may differ")


@needs_funds
def test_funds_never_creates_money():
    funds = impl.Funds.of(100)
    assert funds.take(60) == 60 and funds.take(60) == 40 and funds.take(1) == 0
    assert funds.remaining == 0 and funds.original == 100
    with pytest.raises(ValueError):
        impl.Funds.of(100).take(-1)


@needs_funds
def test_duplicate_receivable_keys_and_unknown_kinds_are_refused():
    with pytest.raises(ValueError):
        allocate([rec(), rec()], [con("A", "fixed", 1)])
    with pytest.raises(ValueError):
        allocate([rec()], [con("A", "ratio", 1)])


@needs_funds
def test_funds_constructor_refuses_a_broken_state():
    with pytest.raises(ValueError):
        impl.Funds(original=10, remaining=11)
    with pytest.raises(ValueError):
        impl.Funds(original=10, remaining=-1)


needs_csv = pytest.mark.skipif(not hasattr(impl, "settle_csv"), reason="CSV helpers are optional")


@needs_csv
def test_csv_round_trip_with_the_worked_example():
    transactions = "customer_id,merchant_id,payout_date,card_type,amount\nP6,Grocer,2026-12-05,Visa,700\nP7,Grocer,2026-12-05,Visa,503\n"
    contracts = ("contract_id,merchant_id,payout_date,card_type,kind,value\n"
                 "Split2,Grocer,2026-12-05,Visa,fixed,350\nSplit3,Grocer,2026-12-05,Visa,percentage,1500\n")
    text = impl.settle_csv(transactions, contracts)
    lines = text.splitlines()
    assert lines[0] == "id,card_type,payout_date,amount" and text.endswith("\n")
    assert sorted(lines[1:]) == ["Grocer,Visa,2026-12-05,673", "Split2,Visa,2026-12-05,350", "Split3,Visa,2026-12-05,180"]


@needs_csv
def test_payout_totals_add_up_across_keys():
    receivables = [rec(card="Visa", amount=1000), rec(card="MasterCard", amount=200)]
    contracts = [con("A", "fixed", 100, card="Visa"), con("A2", "fixed", 100, card="MasterCard")]
    totals = impl.payout_totals(allocate(receivables, contracts))
    assert totals == {"A": 100, "A2": 100, "Grocer": 1000}
    assert sum(totals.values()) == 1200
