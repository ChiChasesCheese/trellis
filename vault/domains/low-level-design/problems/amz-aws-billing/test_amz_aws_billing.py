import importlib
import os
import threading
from datetime import datetime
from decimal import Decimal as D

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

START = datetime(2026, 10, 1)
END = datetime(2026, 11, 1)


def day(n):
    return datetime(2026, 10, n, 12)


def s3_plan():
    # 前 51200 GB 每 GB 0.023，之后 0.022
    return impl.TieredRate((impl.Tier(D("51200"), D("0.023")), impl.Tier(None, D("0.022"))))


def service(*prices):
    book = impl.PriceBook()
    for name, metric, plan in prices:
        book.set_price(name, metric, plan, START)
    return impl.BillingService(book)


def use(uid, svc, metric, qty, at=None):
    return impl.UsageRecord(uid, svc, metric, D(qty), at or day(2))


# ---- 第 1 关：用量 x 费率，按服务汇总 ----

def test_flat_rate_bill_is_quantity_times_rate():
    b = service(("ec2", "hours", impl.FlatRate(D("0.0416"))))
    b.record(use("u1", "ec2", "hours", "730"))
    assert b.invoice(START, END).total == impl.Money(3037)  # 730 x 0.0416 = 30.368


def test_each_service_gets_its_own_line_and_the_total_is_the_sum_of_lines():
    b = service(("ec2", "hours", impl.FlatRate(D("0.0416"))), ("sqs", "requests", impl.FlatRate(D("0.0000004"))))
    b.record(use("u1", "ec2", "hours", "100"))
    b.record(use("u2", "sqs", "requests", "5000000"))
    inv = b.invoice(START, END)
    assert [(l.service, l.amount.cents) for l in inv.lines] == [("ec2", 416), ("sqs", 200)]
    assert inv.total.cents == sum(l.amount.cents for l in inv.lines)


def test_usage_of_one_service_is_summed_before_pricing():
    b = service(("ec2", "hours", impl.FlatRate(D("0.5"))))
    b.record(use("u1", "ec2", "hours", "3"))
    b.record(use("u2", "ec2", "hours", "5", day(9)))
    inv = b.invoice(START, END)
    assert len(inv.lines) == 1 and inv.lines[0].quantity == D("8") and inv.total == impl.Money(400)


def test_empty_period_gives_an_empty_invoice():
    inv = service(("ec2", "hours", impl.FlatRate(D("1")))).invoice(START, END)
    assert inv.lines == () and inv.totals == {}


def test_usage_outside_the_period_is_not_billed():
    b = service(("ec2", "hours", impl.FlatRate(D("1"))))
    b.record(use("u1", "ec2", "hours", "10", datetime(2026, 9, 30, 23)))
    b.record(use("u2", "ec2", "hours", "4", END))
    b.record(use("u3", "ec2", "hours", "1", START))
    assert b.invoice(START, END).total == impl.Money(100)


def test_service_without_a_price_is_rejected_loudly():
    b = service(("ec2", "hours", impl.FlatRate(D("1"))))
    b.record(use("u1", "glacier", "gb", "1"))
    with pytest.raises(impl.UnknownServiceError):
        b.invoice(START, END)


def test_money_rounds_half_up_once_and_refuses_mixed_currencies():
    assert impl.Money.from_decimal(D("30.368")) == impl.Money(3037)
    assert impl.Money.from_decimal(D("0.005")) == impl.Money(1)
    assert str(impl.Money(137120)) == "1371.20 USD" and str(impl.Money(5)) == "0.05 USD"
    with pytest.raises(impl.BillingError):
        impl.Money(1, "USD") + impl.Money(1, "EUR")


def test_negative_usage_is_rejected_and_not_stored():
    b = service(("ec2", "hours", impl.FlatRate(D("1"))))
    with pytest.raises(impl.InvalidUsage):
        b.record(use("u1", "ec2", "hours", "-1"))
    assert b.invoice(START, END).lines == ()


# ---- 第 2 关：阶梯价与免费额度 ----

def test_tiers_are_marginal_not_whole():
    # 102400 GB = 51200 x 0.023 + 51200 x 0.022 = 1177.60 + 1126.40
    assert s3_plan().charge(D("102400")) == D("2304.000")
    assert s3_plan().charge(D("51200")) == D("1177.600")
    assert s3_plan().charge(D("0")) == 0


def test_three_tiers_and_a_quantity_exactly_on_a_boundary():
    plan = impl.TieredRate((impl.Tier(D("10"), D("1")), impl.Tier(D("20"), D("0.5")), impl.Tier(None, D("0.1"))))
    assert plan.charge(D("10")) == D("10")
    assert plan.charge(D("20")) == D("15.0")
    assert plan.charge(D("30")) == D("16.0")


def test_tiers_apply_to_the_monthly_total_not_to_each_record():
    b = service(("s3", "gb-month", s3_plan()))
    b.record(use("u1", "s3", "gb-month", "30000"))
    b.record(use("u2", "s3", "gb-month", "30000", day(9)))
    # 一起算：51200 x 0.023 + 8800 x 0.022 = 1177.60 + 193.60；分开算会得到 2 x 690.00 = 1380.00
    assert b.invoice(START, END).total == impl.Money(137120)


def test_free_tier_is_taken_off_the_monthly_total():
    plan = impl.FreeTierThen(D("1000000"), impl.FlatRate(D("0.0000002")))
    b = service(("lambda", "requests", plan))
    b.record(use("u1", "lambda", "requests", "600000"))
    b.record(use("u2", "lambda", "requests", "1900000", day(8)))
    assert b.invoice(START, END).total == impl.Money(30)  # (2500000 - 1000000) x 0.0000002 = 0.30


def test_usage_inside_the_free_tier_costs_nothing():
    plan = impl.FreeTierThen(D("100"), impl.FlatRate(D("1")))
    b = service(("lambda", "gb-seconds", plan))
    b.record(use("u1", "lambda", "gb-seconds", "100"))
    inv = b.invoice(START, END)
    assert inv.total == impl.Money(0) and len(inv.lines) == 1


def test_plans_nest_a_free_tier_in_front_of_tiers():
    plan = impl.FreeTierThen(D("10"), impl.TieredRate((impl.Tier(D("10"), D("2")), impl.Tier(None, D("1")))))
    assert plan.charge(D("25")) == D("25")  # 超出 15：10 x 2 + 5 x 1


# ---- 第 3 关：重复投递 ----

def test_a_duplicate_delivery_is_ignored_and_counted():
    b = service(("ec2", "hours", impl.FlatRate(D("1"))))
    assert b.record(use("u1", "ec2", "hours", "10")) is True
    assert b.record(use("u1", "ec2", "hours", "10")) is False
    inv = b.invoice(START, END)
    assert inv.total == impl.Money(1000) and inv.duplicates_ignored == 1


def test_same_id_with_different_content_is_an_error_not_a_silent_overwrite():
    b = service(("ec2", "hours", impl.FlatRate(D("1"))))
    b.record(use("u1", "ec2", "hours", "10"))
    with pytest.raises(impl.InvalidUsage):
        b.record(use("u1", "ec2", "hours", "11"))
    assert b.invoice(START, END).total == impl.Money(1000)


def test_invoicing_twice_gives_the_same_bill():
    b = service(("s3", "gb-month", s3_plan()))
    b.record(use("u1", "s3", "gb-month", "60000"))
    assert b.invoice(START, END) == b.invoice(START, END)


def test_concurrent_duplicate_reports_are_counted_once():
    b = service(("ec2", "hours", impl.FlatRate(D("1"))))
    barrier = threading.Barrier(8)
    results = []

    def report():
        barrier.wait()
        results.append(b.record(use("same", "ec2", "hours", "5")))

    threads = [threading.Thread(target=report) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert results.count(True) == 1 and results.count(False) == 7
    assert b.invoice(START, END).total == impl.Money(500)


# ---- 第 4 关：月中调价与多币种 ----

def test_a_mid_month_price_change_prices_each_usage_at_its_own_time():
    b = service(("ec2", "hours", impl.FlatRate(D("1"))))
    b.prices.set_price("ec2", "hours", impl.FlatRate(D("2")), datetime(2026, 10, 16))
    b.record(use("u1", "ec2", "hours", "10", day(10)))
    b.record(use("u2", "ec2", "hours", "10", day(20)))
    inv = b.invoice(START, END)
    assert [(l.quantity, l.amount.cents) for l in inv.lines] == [(D("10"), 1000), (D("10"), 2000)]
    assert inv.total == impl.Money(3000)


def test_a_price_set_late_for_an_earlier_effective_date_still_applies_in_order():
    book = impl.PriceBook()
    book.set_price("ec2", "hours", impl.FlatRate(D("2")), datetime(2026, 10, 16))
    book.set_price("ec2", "hours", impl.FlatRate(D("1")), START)
    assert book.version_at("ec2", "hours", day(10)).plan == impl.FlatRate(D("1"))
    assert book.version_at("ec2", "hours", day(20)).plan == impl.FlatRate(D("2"))
    with pytest.raises(impl.UnknownServiceError):
        book.version_at("ec2", "hours", datetime(2026, 9, 1))


def test_services_priced_in_different_currencies_get_separate_totals():
    book = impl.PriceBook()
    book.set_price("ec2", "hours", impl.FlatRate(D("1")), START, "USD")
    book.set_price("s3-eu", "gb", impl.FlatRate(D("2")), START, "EUR")
    b = impl.BillingService(book)
    b.record(use("u1", "ec2", "hours", "3"))
    b.record(use("u2", "s3-eu", "gb", "4"))
    inv = b.invoice(START, END)
    assert inv.totals == {"USD": impl.Money(300, "USD"), "EUR": impl.Money(800, "EUR")}
    with pytest.raises(impl.BillingError):
        inv.total


def test_ledger_hands_out_a_snapshot():
    b = service(("ec2", "hours", impl.FlatRate(D("1"))))
    b.record(use("u1", "ec2", "hours", "1"))
    snap = b.ledger.between(START, END)
    b.record(use("u2", "ec2", "hours", "1"))
    assert len(snap) == 1 and len(b.ledger.between(START, END)) == 2
