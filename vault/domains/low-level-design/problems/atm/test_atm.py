"""ATM 参考解的 pytest 套件：`IMPL=solution` 必须全绿，`IMPL=starter` 必须失败。"""

import importlib
import os
import threading
from datetime import datetime

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

Y = impl.YUAN
CARD = "ICBC-6222-0001"
PIN = "1234"


def clock():
    """固定时钟：流水要带时间戳，而测试不该因为"现在几点"而不同。"""
    return lambda: datetime(2025, 3, 1, 9, 0)


# --------------------------------------------------------------------------
# `BankNetwork` 的另外两个实现，整个写在测试里。
# 它们就是第 4 关的证据：换一张别家银行的卡、或者换一条会失败的网络，`ATM`、`Cassette`、
# 选钞、流水、对账**一行都不用改**——被替换的只是构造时传进去的那个对象。


class Interchange:
    """跨行转接网络：按卡号前缀路由到成员行，并收一笔跨行手续费。

    路由键藏在认证返回的账户标识里（`"CMB:77"`），ATM 每次原样递回来即可，它完全不需要
    知道世界上有几家银行。
    """

    def __init__(self, members, fee=2 * Y):
        self._members = dict(members)
        self.fee = fee

    def _route(self, account_id):
        bank_id, _, local = account_id.partition(":")
        return self._members[bank_id], local

    def authenticate(self, card_number, pin):
        for bank_id in sorted(self._members, key=len, reverse=True):
            if card_number.startswith(bank_id):
                return f"{bank_id}:{self._members[bank_id].authenticate(card_number, pin)}"
        raise impl.WrongPinError(0)   # 不认识的前缀，和密码错一样不给任何额外信息

    def balance(self, account_id):
        bank, local = self._route(account_id)
        return bank.balance(local)

    def withdraw(self, account_id, amount, ref):
        bank, local = self._route(account_id)
        return bank.withdraw(local, amount + self.fee, ref)

    def deposit(self, account_id, amount, ref):
        bank, local = self._route(account_id)
        return bank.deposit(local, amount, ref)

    def reverse(self, account_id, amount, ref):
        """冲正连手续费一起退：这笔取款没有发生，跨行费自然也不该收。"""
        bank, local = self._route(account_id)
        return bank.reverse(local, amount + self.fee, ref)


class UnreachableBank:
    """认证正常、扣账永远失败的网络，用来验"远端拒绝时本地回滚干净"。"""

    def __init__(self, bank):
        self._bank = bank

    def authenticate(self, card_number, pin):
        return self._bank.authenticate(card_number, pin)

    def balance(self, account_id):
        return self._bank.balance(account_id)

    def withdraw(self, account_id, amount, ref):
        raise impl.ATMError("bank unreachable")

    def deposit(self, account_id, amount, ref):
        return self._bank.deposit(account_id, amount, ref)

    def reverse(self, account_id, amount, ref):
        return self._bank.reverse(account_id, amount, ref)


# --------------------------------------------------------------------------


def make_bank(balance=3000 * Y, bank_id="ICBC"):
    bank = impl.LocalBank(bank_id)
    bank.open_account("1001", balance=balance)
    bank.issue_card(CARD, "1001", PIN)
    return bank


def make_atm(bank=None, cash=None, **kwargs):
    bank = bank or make_bank()
    counts = cash if cash is not None else {impl.Note.HUNDRED: 10, impl.Note.FIFTY: 4,
                                            impl.Note.TWENTY: 5, impl.Note.TEN: 5}
    return impl.ATM(bank, impl.Cassette(counts), clock=clock(), **kwargs), bank


def signed_in(atm):
    atm.insert_card(CARD)
    atm.enter_pin(PIN)
    return atm


# ---- 第 1 关：会话状态机 --------------------------------------------------


def test_the_happy_path_walks_every_state_in_order():
    atm, _ = make_atm()
    assert atm.state is impl.SessionState.IDLE
    assert atm.insert_card(CARD) is impl.SessionState.CARD_INSERTED
    assert atm.enter_pin(PIN) is impl.SessionState.AUTHENTICATED
    atm.withdraw(300 * Y)
    assert atm.state is impl.SessionState.DISPENSING
    atm.collect_cash()
    assert atm.state is impl.SessionState.AUTHENTICATED
    assert atm.eject_card() is impl.SessionState.IDLE
    assert [e.kind for e in atm.journal()] == [impl.TxKind.WITHDRAWAL]


def test_every_state_action_pair_outside_the_table_is_illegal():
    """穷举 4 × 7 个"状态 × 用户动作"组合：授权表之外的每一个都必须被拒绝。"""
    calls = {
        impl.Action.INSERT_CARD: lambda a: a.insert_card(CARD),
        impl.Action.ENTER_PIN: lambda a: a.enter_pin(PIN),
        impl.Action.BALANCE: lambda a: a.balance(),
        impl.Action.DEPOSIT: lambda a: a.deposit({impl.Note.HUNDRED: 1}),
        impl.Action.WITHDRAW: lambda a: a.withdraw(100 * Y),
        impl.Action.COLLECT_CASH: lambda a: a.collect_cash(),
        impl.Action.EJECT: lambda a: a.eject_card(),
    }
    setups = {
        impl.SessionState.IDLE: lambda a: None,
        impl.SessionState.CARD_INSERTED: lambda a: a.insert_card(CARD),
        impl.SessionState.AUTHENTICATED: lambda a: signed_in(a),
        impl.SessionState.DISPENSING: lambda a: (signed_in(a), a.withdraw(100 * Y)),
    }
    checked = 0
    for state, setup in setups.items():
        for action, call in calls.items():
            if (state, action) in impl.TRANSITIONS:
                continue
            atm, _ = make_atm()
            setup(atm)
            assert atm.state is state
            with pytest.raises(impl.IllegalActionError):
                call(atm)
            assert atm.state is state       # 被拒绝的动作不改变状态
            checked += 1
    legal = sum(1 for s in setups for a in calls if (s, a) in impl.TRANSITIONS)
    assert checked == len(setups) * len(calls) - legal == 20


def test_ejecting_the_card_while_cash_is_on_the_tray_is_refused():
    atm, _ = make_atm()
    signed_in(atm).withdraw(100 * Y)
    with pytest.raises(impl.IllegalActionError):
        atm.eject_card()
    assert atm.state is impl.SessionState.DISPENSING
    assert atm.cash_up().on_tray == 100 * Y      # 钱还在口上，所以卡不能先走


def test_a_wrong_pin_leaves_the_session_where_it_was_and_counts_down():
    atm, _ = make_atm()
    atm.insert_card(CARD)
    with pytest.raises(impl.WrongPinError) as first:
        atm.enter_pin("0000")
    assert first.value.remaining == 2
    assert atm.state is impl.SessionState.CARD_INSERTED
    atm.enter_pin(PIN)                       # 第二次输对了，同一张卡照常放行
    assert atm.state is impl.SessionState.AUTHENTICATED


def test_three_wrong_pins_retain_the_card_and_void_it_at_the_bank():
    atm, _ = make_atm()
    atm.insert_card(CARD)
    for _ in range(2):
        with pytest.raises(impl.WrongPinError):
            atm.enter_pin("0000")
    with pytest.raises(impl.CardRetainedError):
        atm.enter_pin("0000")
    assert atm.state is impl.SessionState.IDLE          # 卡被机器留下，会话结束
    kinds = [e.kind for e in atm.journal()]
    assert kinds.count(impl.TxKind.PIN_FAILURE) == 3
    assert impl.TxKind.CARD_RETAINED in kinds
    atm.insert_card(CARD)                                # 换一张新会话也救不了
    with pytest.raises(impl.CardRetainedError):
        atm.enter_pin(PIN)


def test_the_pin_attempt_counter_belongs_to_the_bank_not_to_one_machine():
    """在三台不同的 ATM 上各错一次，仍然是三次错——计数归发卡行。"""
    bank = make_bank()
    machines = [make_atm(bank=bank)[0] for _ in range(3)]
    for atm in machines[:2]:
        atm.insert_card(CARD)
        with pytest.raises(impl.WrongPinError):
            atm.enter_pin("0000")
    machines[2].insert_card(CARD)
    with pytest.raises(impl.CardRetainedError):
        machines[2].enter_pin("0000")


def test_an_unknown_card_a_wrong_pin_and_a_void_card_are_indistinguishable():
    """否则插一张卡试一次密码就能问出"这张卡存不存在"，机器成了账号枚举器。"""
    unknown_atm, _ = make_atm()
    unknown_atm.insert_card("NO-SUCH-CARD")
    with pytest.raises(impl.WrongPinError) as unknown:
        unknown_atm.enter_pin(PIN)

    wrong_atm, bank = make_atm()
    wrong_atm.insert_card(CARD)
    with pytest.raises(impl.WrongPinError) as wrong:
        wrong_atm.enter_pin("0000")
    assert str(unknown.value) == str(wrong.value)
    assert unknown.value.remaining == wrong.value.remaining

    for _ in range(2):                       # 把这张卡作废掉
        with pytest.raises(impl.ATMError):
            wrong_atm.enter_pin("0000")
    with pytest.raises(impl.WrongPinError) as voided:
        bank.authenticate(CARD, PIN)         # 作废的卡报的还是同一个错
    assert voided.value.remaining == 0


# ---- 第 2 关：取款与选钞 --------------------------------------------------


def test_withdrawal_takes_notes_out_of_the_cassettes_it_actually_holds():
    cash = {impl.Note.HUNDRED: 2, impl.Note.FIFTY: 2, impl.Note.TWENTY: 3}
    atm, bank = make_atm(cash=cash)
    before_notes = impl.Cassette(cash).note_count
    plan = signed_in(atm).withdraw(270 * Y)
    assert sum(int(n) * c for n, c in plan.items()) == 270 * Y
    after = atm.cassette_counts()
    for note, count in plan.items():
        assert after.get(note, 0) == cash[note] - count
    assert impl.Cassette(dict(after)).note_count == before_notes - sum(plan.values())
    assert dict(atm.tray_counts()) == dict(plan)     # 钞票在出钞口上等着
    assert bank.account("1001").balance == 3000 * Y - 270 * Y


def test_the_selector_hands_back_the_fewest_notes_it_can():
    atm, _ = make_atm(cash={impl.Note.HUNDRED: 3, impl.Note.FIFTY: 6, impl.Note.TWENTY: 10})
    plan = signed_in(atm).withdraw(300 * Y)
    assert plan == {impl.Note.HUNDRED: 3}


def test_an_amount_the_notes_cannot_express_is_refused_before_anything_moves():
    atm, bank = make_atm()
    before = dict(atm.cassette_counts())
    with pytest.raises(impl.AmountNotDispensableError) as exc:
        signed_in(atm).withdraw(135 * Y)          # 不是 10 元的整数倍
    assert exc.value.reason is impl.DispenseFailure.NOT_REPRESENTABLE
    assert dict(atm.cassette_counts()) == before
    assert bank.account("1001").balance == 3000 * Y
    assert atm.state is impl.SessionState.AUTHENTICATED


def test_an_amount_the_cassettes_cannot_make_is_a_different_failure():
    atm, bank = make_atm(cash={impl.Note.HUNDRED: 5})
    with pytest.raises(impl.AmountNotDispensableError) as exc:
        signed_in(atm).withdraw(250 * Y)
    assert exc.value.reason is impl.DispenseFailure.NOT_IN_STOCK
    assert bank.account("1001").balance == 3000 * Y


def test_an_amount_needing_more_notes_than_the_feeder_moves_is_refused():
    atm, _ = make_atm(cash={impl.Note.TEN: 80})
    with pytest.raises(impl.AmountNotDispensableError) as exc:
        signed_in(atm).withdraw(500 * Y)          # 50 张，超过一次送钞上限
    assert exc.value.reason is impl.DispenseFailure.TOO_MANY_NOTES


def test_greedy_reports_a_makeable_amount_as_unmakeable_and_the_dp_does_not():
    """钞箱里有 1×100、1×50、4×20，取 80 元：贪心先拿走 50 就再也凑不出，DP 拿四张 20。"""
    def greedy_notes(amount, available):
        plan, remaining = {}, amount
        for note in sorted(available, reverse=True):
            take = min(remaining // int(note), available[note])
            if take:
                plan[note] = take
                remaining -= int(note) * take
        return plan if remaining == 0 else None

    cash = {impl.Note.HUNDRED: 1, impl.Note.FIFTY: 1, impl.Note.TWENTY: 4}
    assert greedy_notes(80 * Y, cash) is None
    assert impl.fewest_notes(80 * Y, cash) == {impl.Note.TWENTY: 4}
    lazy, _ = make_atm(cash=cash, selector=greedy_notes)
    with pytest.raises(impl.AmountNotDispensableError):
        signed_in(lazy).withdraw(80 * Y)
    careful, _ = make_atm(cash=cash)
    assert signed_in(careful).withdraw(80 * Y) == {impl.Note.TWENTY: 4}


def test_a_declined_debit_puts_the_reserved_notes_back_into_the_cassettes():
    """余额不足时，留好的钞票必须原样回到钞箱——否则机器每被拒一次就少一沓钱。"""
    atm, bank = make_atm(bank=make_bank(balance=100 * Y))
    before = dict(atm.cassette_counts())
    with pytest.raises(impl.InsufficientFundsError):
        signed_in(atm).withdraw(300 * Y)
    assert dict(atm.cassette_counts()) == before
    assert bank.account("1001").balance == 100 * Y
    assert dict(atm.tray_counts()) == {}
    assert atm.cash_up().balanced
    assert [e.status for e in atm.journal()] == [impl.TxStatus.DECLINED]


def test_a_network_that_never_answers_also_leaves_the_cassettes_untouched():
    """第二个 `BankNetwork` 实现：远端失败时本地必须回滚得同样干净。"""
    bank = make_bank()
    atm = impl.ATM(UnreachableBank(bank), impl.Cassette({impl.Note.HUNDRED: 5}), clock=clock())
    before = dict(atm.cassette_counts())
    with pytest.raises(impl.ATMError):
        signed_in(atm).withdraw(300 * Y)
    assert dict(atm.cassette_counts()) == before
    assert bank.account("1001").balance == 3000 * Y
    assert atm.cash_up().balanced


def test_a_denomination_that_runs_out_disappears_from_the_cassette_table():
    atm, _ = make_atm(cash={impl.Note.HUNDRED: 1, impl.Note.FIFTY: 2})
    signed_in(atm).withdraw(100 * Y)
    assert impl.Note.HUNDRED not in atm.cassette_counts()
    assert dict(atm.cassette_counts()) == {impl.Note.FIFTY: 2}


def test_the_machine_never_hands_out_its_own_containers():
    atm, _ = make_atm()
    counts = atm.cassette_counts()
    with pytest.raises(TypeError):
        counts[impl.Note.HUNDRED] = 999


# ---- 第 3 关：存款、查询、流水与冲正 ----------------------------------------


def test_deposited_notes_go_to_the_deposit_bin_and_never_back_into_the_cassettes():
    atm, _ = make_atm()
    before = dict(atm.cassette_counts())
    new_balance = signed_in(atm).deposit({impl.Note.HUNDRED: 3})
    assert new_balance == 3300 * Y
    assert dict(atm.cassette_counts()) == before
    report = atm.cash_up()
    assert report.deposited == 300 * Y and report.balanced


def test_the_journal_records_every_transaction_with_a_masked_card_and_a_reference():
    atm, _ = make_atm()
    signed_in(atm)
    atm.balance()
    atm.withdraw(200 * Y)
    atm.collect_cash()
    atm.deposit({impl.Note.FIFTY: 1})
    entries = atm.journal()
    assert [e.kind for e in entries] == [impl.TxKind.BALANCE, impl.TxKind.WITHDRAWAL,
                                         impl.TxKind.DEPOSIT]
    assert all(e.card_tail == CARD[-4:] and len(e.card_tail) == 4 for e in entries)
    assert len({e.ref for e in entries}) == 3


def test_uncollected_cash_is_retracted_into_the_reject_bin_and_reversed_at_the_bank():
    atm, bank = make_atm()
    signed_in(atm).withdraw(300 * Y)
    assert bank.account("1001").balance == 2700 * Y
    assert atm.cash_up().on_tray == 300 * Y
    retracted = atm.retract_uncollected()
    assert sum(int(n) * c for n, c in retracted.items()) == 300 * Y
    assert bank.account("1001").balance == 3000 * Y          # 冲正把钱退回去了
    report = atm.cash_up()
    assert report.in_reject_bin == 300 * Y and report.on_tray == 0 and report.balanced
    assert dict(atm.tray_counts()) == {}
    reversal = [e for e in atm.journal() if e.kind is impl.TxKind.REVERSAL]
    assert len(reversal) == 1 and reversal[0].status is impl.TxStatus.REVERSED
    original = [e for e in atm.journal() if e.kind is impl.TxKind.WITHDRAWAL][0]
    assert original.status is impl.TxStatus.OK               # 原记录永远不改
    assert reversal[0].ref == original.ref


def test_retracted_notes_never_go_back_into_the_dispensable_cassettes():
    atm, _ = make_atm(cash={impl.Note.HUNDRED: 3})
    signed_in(atm).withdraw(300 * Y)
    atm.retract_uncollected()
    assert dict(atm.cassette_counts()) == {}                 # 收回的钞票不再出钞
    with pytest.raises(impl.AmountNotDispensableError):
        atm.withdraw(100 * Y)


def test_cash_is_conserved_across_a_long_mixed_session():
    atm, _ = make_atm()
    signed_in(atm)
    atm.withdraw(300 * Y)
    atm.collect_cash()
    atm.deposit({impl.Note.HUNDRED: 2})
    atm.withdraw(120 * Y)
    atm.retract_uncollected()
    atm.eject_card()
    report = atm.cash_up()
    assert report.balanced
    assert report.collected == 300 * Y and report.in_reject_bin == 120 * Y


# ---- 第 4 关：跨行网络与并发 ------------------------------------------------


def test_a_second_banks_card_works_through_the_interchange_without_touching_the_atm():
    home = make_bank(bank_id="ICBC")
    other = impl.LocalBank("CMB")
    other.open_account("77", balance=1000 * Y)
    other.issue_card("CMB-4001", "77", "9999")
    atm = impl.ATM(Interchange({"ICBC": home, "CMB": other}, fee=2 * Y),
                   impl.Cassette({impl.Note.HUNDRED: 20}), clock=clock())
    atm.insert_card("CMB-4001")
    atm.enter_pin("9999")
    assert atm.balance() == 1000 * Y
    plan = atm.withdraw(500 * Y)
    atm.collect_cash()
    assert sum(int(n) * c for n, c in plan.items()) == 500 * Y   # 客户拿到 500
    assert other.account("77").balance == 1000 * Y - 502 * Y     # 账上少 500 + 手续费
    atm.eject_card()
    assert home.account("1001").balance == 3000 * Y              # 另一家银行毫发无损


def test_a_reversal_across_the_interchange_refunds_the_fee_too():
    """这笔取款没有发生，跨行费自然也不该收——策略要被钉住，不能只写在注释里。"""
    other = impl.LocalBank("CMB")
    other.open_account("77", balance=1000 * Y)
    other.issue_card("CMB-4001", "77", "9999")
    atm = impl.ATM(Interchange({"CMB": other}, fee=2 * Y),
                   impl.Cassette({impl.Note.HUNDRED: 20}), clock=clock())
    atm.insert_card("CMB-4001")
    atm.enter_pin("9999")
    atm.withdraw(500 * Y)
    assert other.account("77").balance == 498 * Y
    atm.retract_uncollected()
    assert other.account("77").balance == 1000 * Y               # 本金和手续费一起退回
    assert atm.cash_up().balanced


def test_concurrent_withdrawals_on_two_machines_never_oversell_one_account():
    """两台机器同时对同一个账户取款：余额不会变负，出钞总额和扣账总额永远对得上。"""
    bank = make_bank(balance=500 * Y)
    machines = [make_atm(bank=bank, cash={impl.Note.HUNDRED: 10})[0] for _ in range(2)]
    barrier = threading.Barrier(len(machines))
    dispensed, errors, guard = [], [], threading.Lock()

    def run(atm):
        signed_in(atm)
        barrier.wait()
        try:
            plan = atm.withdraw(400 * Y)
            atm.collect_cash()
        except impl.ATMError as exc:
            with guard:
                errors.append(exc)
            return
        with guard:
            dispensed.append(sum(int(n) * c for n, c in plan.items()))

    threads = [threading.Thread(target=run, args=(atm,)) for atm in machines]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(dispensed) == 1 and len(errors) == 1      # 只有一个人取得到
    assert bank.account("1001").balance == 500 * Y - sum(dispensed)
    assert all(atm.cash_up().balanced for atm in machines)
