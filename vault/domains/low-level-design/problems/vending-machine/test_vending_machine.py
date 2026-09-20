"""自动售货机参考解的 pytest 套件：`IMPL=solution` 必须全绿，`IMPL=starter` 必须失败。"""

import importlib
import os
import threading

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


def make_machine(stock=None, bank=None, change_maker=None):
    slots = stock or {"A1": impl.Slot(impl.Item("可乐", 75), 2),
                      "A2": impl.Slot(impl.Item("薯片", 120), 1)}
    coins = bank if bank is not None else {impl.Coin.QUARTER: 4, impl.Coin.DIME: 4,
                                           impl.Coin.NICKEL: 4}
    kwargs = {} if change_maker is None else {"change_maker": change_maker}
    return impl.VendingMachine(slots=slots, bank=impl.CoinBank(coins), **kwargs)


def buy(machine, code, coins):
    for coin in coins:
        machine.insert_coin(coin)
    machine.select(code)
    item = machine.dispense()
    return item, machine.collect_change()


# ---- 第 1 关：购买流程的状态机 ----------------------------------------------


def test_the_happy_path_walks_every_state_in_order():
    machine = make_machine()
    seen = []
    machine.subscribe(lambda e: seen.append((e.before, e.after)))
    item, change = buy(machine, "A1", [impl.Coin.DOLLAR])
    assert item.name == "可乐"
    assert sum(int(c) for c in change) == 25
    assert seen == [(impl.State.IDLE, impl.State.COIN_INSERTED),
                    (impl.State.COIN_INSERTED, impl.State.DISPENSING),
                    (impl.State.DISPENSING, impl.State.RETURNING_CHANGE),
                    (impl.State.RETURNING_CHANGE, impl.State.IDLE)]
    assert machine.state is impl.State.IDLE


def test_selecting_without_paying_is_rejected_by_the_transition_table():
    machine = make_machine()
    with pytest.raises(impl.IllegalTransitionError):
        machine.select("A1")
    assert machine.state is impl.State.IDLE


def test_inserting_money_after_dispensing_started_is_rejected():
    machine = make_machine()
    machine.insert_coin(impl.Coin.DOLLAR)
    machine.select("A1")
    assert machine.state is impl.State.DISPENSING
    with pytest.raises(impl.IllegalTransitionError):
        machine.insert_coin(impl.Coin.QUARTER)


def test_refund_is_refused_once_the_item_is_on_its_way():
    machine = make_machine()
    machine.insert_coin(impl.Coin.DOLLAR)
    machine.select("A1")
    with pytest.raises(impl.IllegalTransitionError):
        machine.refund()


def test_every_state_event_pair_outside_the_table_is_illegal():
    """穷举 4 × 5 个组合：转移表之外的每一个都必须被拒绝。这是把表做成数据的直接收益。"""
    calls = {
        impl.Event.PAY: lambda m: m.insert_coin(impl.Coin.NICKEL),
        impl.Event.SELECT: lambda m: m.select("A1"),
        impl.Event.DISPENSE: lambda m: m.dispense(),
        impl.Event.COLLECT: lambda m: m.collect_change(),
        impl.Event.REFUND: lambda m: m.refund(),
    }
    setups = {
        impl.State.IDLE: lambda m: None,
        impl.State.COIN_INSERTED: lambda m: m.insert_coin(impl.Coin.DOLLAR),
        impl.State.DISPENSING: lambda m: (m.insert_coin(impl.Coin.DOLLAR), m.select("A1")),
        impl.State.RETURNING_CHANGE: lambda m: (m.insert_coin(impl.Coin.DOLLAR),
                                                m.select("A1"), m.dispense()),
    }
    checked = 0
    for state, setup in setups.items():
        for event, call in calls.items():
            if (state, event) in impl.TRANSITIONS:
                continue
            machine = make_machine()
            setup(machine)
            assert machine.state is state
            with pytest.raises(impl.IllegalTransitionError):
                call(machine)
            checked += 1
    assert checked == len(setups) * len(calls) - len(impl.TRANSITIONS)


def test_the_prompt_says_what_the_machine_is_waiting_for():
    machine = make_machine()
    idle_prompt = machine.prompt
    machine.insert_coin(impl.Coin.QUARTER)
    assert machine.prompt != idle_prompt
    machine.refund()
    assert machine.prompt == idle_prompt


def test_refund_returns_exactly_the_coins_that_went_in():
    machine = make_machine()
    for coin in (impl.Coin.QUARTER, impl.Coin.DIME, impl.Coin.NICKEL):
        machine.insert_coin(coin)
    assert machine.balance == 40
    assert sorted(machine.refund()) == sorted([impl.Coin.QUARTER, impl.Coin.DIME, impl.Coin.NICKEL])
    assert machine.balance == 0
    assert machine.state is impl.State.IDLE
    assert machine.bank_counts()[impl.Coin.QUARTER] == 4  # 退掉的钱没有进过币箱


# ---- 第 2 关：库存、币箱与失败路径 ------------------------------------------


def test_an_unknown_slot_leaves_the_money_where_it_was():
    machine = make_machine()
    machine.insert_coin(impl.Coin.DOLLAR)
    with pytest.raises(impl.InvalidSelectionError):
        machine.select("Z9")
    assert machine.state is impl.State.COIN_INSERTED and machine.balance == 100


def test_a_sold_out_slot_fails_without_touching_stock_or_bank():
    machine = make_machine(stock={"A1": impl.Slot(impl.Item("可乐", 75), 0)})
    machine.insert_coin(impl.Coin.DOLLAR)
    bank_before = dict(machine.bank_counts())
    with pytest.raises(impl.OutOfStockError):
        machine.select("A1")
    assert machine.stock()["A1"] == 0
    assert dict(machine.bank_counts()) == bank_before
    assert machine.balance == 100


def test_too_little_money_is_a_guard_not_an_illegal_transition():
    machine = make_machine()
    machine.insert_coin(impl.Coin.QUARTER)
    with pytest.raises(impl.InsufficientFundsError):
        machine.select("A1")
    assert machine.state is impl.State.COIN_INSERTED
    machine.insert_coin(impl.Coin.DOLLAR)  # 补钱之后同一次选择就能成功
    assert machine.select("A1").name == "可乐"


def test_the_machine_refuses_the_sale_rather_than_half_completing_it():
    """找不开零钱时：货不能出、库存和币箱一动不动、钱还在买家名下。"""
    machine = make_machine(bank={})  # 币箱空的
    machine.insert_coin(impl.Coin.DOLLAR)
    with pytest.raises(impl.CannotMakeChangeError):
        machine.select("A1")
    assert machine.state is impl.State.COIN_INSERTED
    assert machine.stock()["A1"] == 2
    assert dict(machine.bank_counts()) == {}
    assert sorted(machine.refund()) == [impl.Coin.DOLLAR]


def test_exact_money_still_works_when_the_bank_cannot_make_change():
    machine = make_machine(bank={})
    for coin in (impl.Coin.QUARTER, impl.Coin.QUARTER, impl.Coin.QUARTER):
        machine.insert_coin(coin)
    assert machine.select("A1").name == "可乐"
    machine.dispense()
    assert machine.collect_change() == ()
    assert machine.bank_counts()[impl.Coin.QUARTER] == 3


def test_change_may_be_paid_out_of_the_coins_just_inserted():
    machine = make_machine(stock={"A1": impl.Slot(impl.Item("可乐", 75), 1)}, bank={})
    for _ in range(5):
        machine.insert_coin(impl.Coin.QUARTER)  # 125 买 75，应找 50，而币箱是空的
    machine.select("A1")
    machine.dispense()
    assert sum(int(c) for c in machine.collect_change()) == 50


def test_stock_drops_by_exactly_one_and_the_slot_can_sell_out():
    machine = make_machine(stock={"A1": impl.Slot(impl.Item("可乐", 75), 1)}, bank={})
    buy(machine, "A1", [impl.Coin.QUARTER] * 3)
    assert machine.stock()["A1"] == 0
    machine.insert_coin(impl.Coin.QUARTER)
    machine.insert_coin(impl.Coin.QUARTER)
    machine.insert_coin(impl.Coin.QUARTER)
    with pytest.raises(impl.OutOfStockError):
        machine.select("A1")


def test_the_bank_drops_a_denomination_when_its_count_reaches_zero():
    """取空的面额必须从币箱字典里消失，否则找零算法会去试一种其实没有的硬币。"""
    bank = impl.CoinBank({impl.Coin.QUARTER: 1, impl.Coin.DIME: 2})
    bank.take([impl.Coin.QUARTER])
    assert impl.Coin.QUARTER not in bank.counts()
    assert bank.total == 20


def test_the_bank_snapshot_cannot_be_used_to_mutate_the_bank():
    machine = make_machine()
    counts = machine.bank_counts()
    with pytest.raises(TypeError):
        counts[impl.Coin.DOLLAR] = 99  # type: ignore[index]
    assert impl.Coin.DOLLAR not in machine.bank_counts()


# ---- 第 3 关：找零算法 ------------------------------------------------------


def test_greedy_fails_on_a_bank_where_an_exact_solution_exists():
    """币箱里只有 25 分和 10 分时，找 30 分：贪心先拿 25 就死了，DP 用三个 10 分解决。"""
    available = {impl.Coin.QUARTER: 2, impl.Coin.DIME: 5}
    assert impl.greedy_change(30, available) is None
    plan = impl.exact_change(30, available)
    assert plan is not None and sum(int(c) for c in plan) == 30
    assert set(plan) == {impl.Coin.DIME}


def test_both_makers_agree_on_an_ordinary_case():
    available = {impl.Coin.QUARTER: 4, impl.Coin.DIME: 4, impl.Coin.NICKEL: 4}
    for maker in (impl.greedy_change, impl.exact_change):
        plan = maker(40, available)
        assert plan is not None and sum(int(c) for c in plan) == 40


def test_change_makers_report_failure_instead_of_over_paying():
    available = {impl.Coin.QUARTER: 1}
    assert impl.greedy_change(30, available) is None
    assert impl.exact_change(30, available) is None


def test_the_change_maker_is_pluggable_and_changes_the_outcome():
    """同一台机器换一个找零算法，结果从"拒单"变成"成交"——这就是可替换点存在的证据。"""
    bank = {impl.Coin.QUARTER: 2, impl.Coin.DIME: 5}  # 没有 5 分硬币
    greedy = make_machine(stock={"A1": impl.Slot(impl.Item("可乐", 70), 1)},
                          bank=dict(bank), change_maker=impl.greedy_change)
    greedy.insert_coin(impl.Coin.DOLLAR)  # 100 买 70，应找 30
    with pytest.raises(impl.CannotMakeChangeError):
        greedy.select("A1")

    smart = make_machine(stock={"A1": impl.Slot(impl.Item("可乐", 70), 1)},
                         bank=dict(bank), change_maker=impl.exact_change)
    smart.insert_coin(impl.Coin.DOLLAR)
    smart.select("A1")
    smart.dispense()
    assert sum(int(c) for c in smart.collect_change()) == 30


# ---- 第 4 关：补货、管理动作与第二种支付方式 --------------------------------


def test_restocking_is_refused_in_the_middle_of_a_transaction():
    machine = make_machine(stock={"A1": impl.Slot(impl.Item("可乐", 75), 0)})
    machine.insert_coin(impl.Coin.QUARTER)
    with pytest.raises(impl.IllegalTransitionError):
        machine.restock("A1", 5)
    machine.refund()
    machine.restock("A1", 5)
    assert machine.stock()["A1"] == 5


def test_loading_coins_makes_a_previously_impossible_sale_possible():
    machine = make_machine(bank={})
    machine.insert_coin(impl.Coin.DOLLAR)
    with pytest.raises(impl.CannotMakeChangeError):
        machine.select("A1")
    machine.refund()
    machine.load_coins({impl.Coin.QUARTER: 2})
    item, change = buy(machine, "A1", [impl.Coin.DOLLAR])
    assert item.name == "可乐" and sum(int(c) for c in change) == 25


def test_a_card_payment_uses_the_very_same_state_machine():
    machine = make_machine(bank={})
    machine.swipe_card("card-1", authorized=200)
    assert machine.state is impl.State.COIN_INSERTED
    machine.select("A2")
    assert machine.dispense().name == "薯片"
    assert machine.collect_change() == ()  # 刷卡不用硬币找零，所以空币箱也能成交
    assert machine.state is impl.State.IDLE


def test_a_card_tender_captures_only_the_price_and_voids_on_refund():
    tender = impl.CardTender(card_id="card-1", authorized=200)
    bank = impl.CoinBank({})
    tender.settle(bank, 120)
    assert tender.captured == 120 and bank.total == 0
    other = impl.CardTender(card_id="card-2", authorized=200)
    assert other.release() == () and other.voided is True


def test_coins_and_a_card_cannot_be_mixed_in_one_transaction():
    machine = make_machine()
    machine.insert_coin(impl.Coin.QUARTER)
    with pytest.raises(impl.IllegalTransitionError):
        machine.swipe_card("card-1", authorized=200)


def test_concurrent_buyers_never_oversell_a_single_item():
    """八个线程同时抢最后一件：恰好一个人买到，其余全部被状态机或库存守卫挡下。"""
    machine = make_machine(stock={"A1": impl.Slot(impl.Item("可乐", 75), 1)}, bank={})
    barrier = threading.Barrier(8)
    bought: list[str] = []
    lock = threading.Lock()

    def attempt() -> None:
        barrier.wait()
        try:
            for _ in range(3):
                machine.insert_coin(impl.Coin.QUARTER)
            machine.select("A1")
            item = machine.dispense()
            machine.collect_change()
        except impl.VendingMachineError:
            return
        with lock:
            bought.append(item.name)

    threads = [threading.Thread(target=attempt) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(bought) <= 1
    assert machine.stock()["A1"] == (0 if bought else 1)
