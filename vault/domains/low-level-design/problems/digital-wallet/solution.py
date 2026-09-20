"""数字钱包（Digital Wallet）——双分录账本、余额缓存核对与幂等转账的参考实现。

五行设计：钱是整数最小货币单位；充值、提现、转账全部收敛成同一个私有原语 `_move`，
差别只是端点之一是不是保留的 `EXTERNAL` 系统账户；每次移动在账本里追加恰好两条相加为零
的分录，账户余额只是这份账本的缓存投影，`reconcile` 用账本重新推导出真值去核对缓存；
两个账户各自一把锁，`_move` 永远按账户 id 的稳定顺序取锁而不是按参数（from, to）的顺序，
这是防止两个方向的并发转账互相等死的唯一原因；幂等靠同一把锁的互斥性天然获得——同一个
`client_key` 的重试必然锁住同一对账户，不需要另一层去重机制。
"""

from __future__ import annotations

import itertools
import threading
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime


class WalletError(Exception):
    """本设计里所有失败路径的公共基类。"""


class UnknownAccountError(WalletError):
    """引用了一个不存在的账户，或者试图直接操作保留的系统账户。"""


class InvalidAmountError(WalletError):
    """金额不是正数。"""


class InsufficientFundsError(WalletError):
    """账户余额不足以覆盖这笔转出，操作被整体拒绝，两边余额都不变。

    带着 `shortfall`（还差多少）而不是只带一句话：调用方经常需要在界面上直接提示
    "还差 12.30 元"，不该为了这一个数字去重新解析异常消息。
    """

    def __init__(self, account_id: str, available: int, requested: int) -> None:
        super().__init__(f"账户 {account_id} 余额 {available} 不足以转出 {requested}")
        self.account_id = account_id
        self.shortfall = requested - available


class SameAccountTransferError(WalletError):
    """转账的转入转出是同一个账户。"""


class IdempotencyConflictError(WalletError):
    """同一个 `client_key` 被用在了两笔参数不同的移动上——这是调用方的 bug：幂等键
    应该唯一标识"这一次业务意图"，被挪去标识另一笔转账时，绝不能被静默地当成重试放过。
    """


class LedgerIntegrityError(WalletError):
    """一次记账的两条分录没有相加为零——账本自己的不变式被破坏，属于内部缺陷。"""


EXTERNAL_ACCOUNT_ID = "EXTERNAL"


@dataclass(slots=True)
class Account:
    """一个账户：缓存余额，加一把保护它的独立锁。

    余额是**缓存值**（第 2 关的设计决策），每次改动都在持有这把锁的临界区里同步更新；
    唯一真源是 `Ledger`，`Wallet.reconcile` 负责用账本重新推导出的值去核对这份缓存。
    锁挂在账户自己身上，因为一次转账要按账户 id 的稳定顺序同时拿两个账户的锁。

    `reserved` 只在 `EXTERNAL` 这一个账户上是 `True`：它允许余额为负（钱从系统外部
    进入的方式），并且默认不能被公开方法的调用方直接指定为转账的任意一端。这是整个
    钱包里唯一一处需要知道"谁是保留账户"的地方——`_move` 只读这一个字段，不再单独
    判断账户 id 是不是等于 `EXTERNAL_ACCOUNT_ID` 这个字符串。
    """

    id: str
    balance: int = 0
    reserved: bool = False
    lock: threading.Lock = field(default_factory=threading.Lock, repr=False, compare=False)


@dataclass(frozen=True, slots=True)
class LedgerEntry:
    """一条记账分录：某个账户在某次移动里变化了多少。

    一次移动恒定追加两条分录，`delta` 相加为零——这就是"每一笔移动都是两条分录"在代码里
    的样子。正数是入账、负数是出账，不再另设一个 DEBIT/CREDIT 的 `kind` 字段：符号已经
    完整表达了方向，多一个字段只会多出"符号和字段互相矛盾"这一种新的 bug（见题解"常见错误"）。
    """

    id: str
    transfer_id: str
    account_id: str
    delta: int
    memo: str
    at: datetime


class Ledger:
    """“钱从哪笔移动来”的唯一真源：一张只增不减的分录表，每次移动追加恰好两条、`delta`
    相加为零的分录。它不认识锁、不认识账户对象，只认识账户 id 和数字——这是它能被单独
    测试、也能被单独断言"全局相加为零"的原因。
    """

    def __init__(self) -> None:
        self._entries: list[LedgerEntry] = []
        self._by_account: dict[str, list[LedgerEntry]] = {}
        self._by_transfer: dict[str, list[LedgerEntry]] = {}
        self._ids = (f"L{n}" for n in itertools.count(1))

    @property
    def entry_count(self) -> int:
        """账本里一共有多少条分录；只增不减，是审计追溯要求的（不像幂等缓存那样需要收口）。
        `_by_account`、`_by_transfer` 两份索引和它一起增长，理由相同：它们是账本的一部分，
        不是可以随时丢弃重建的缓存。
        """
        return len(self._entries)

    def record_pair(self, transfer_id: str, debit: tuple[str, int], credit: tuple[str, int],
                     memo: str, at: datetime) -> tuple[LedgerEntry, LedgerEntry]:
        """追加一次移动的两条分录；两者的 `delta` 之和必须为零，否则是内部缺陷。"""
        (debit_account, debit_delta), (credit_account, credit_delta) = debit, credit
        if debit_delta + credit_delta != 0:
            raise LedgerIntegrityError(
                f"分录不平：{debit_delta} + {credit_delta} != 0")
        entries = (
            LedgerEntry(next(self._ids), transfer_id, debit_account, debit_delta, memo, at),
            LedgerEntry(next(self._ids), transfer_id, credit_account, credit_delta, memo, at),
        )
        for entry in entries:
            self._entries.append(entry)
            self._by_account.setdefault(entry.account_id, []).append(entry)
        self._by_transfer[transfer_id] = list(entries)
        return entries

    def derived_balance(self, account_id: str) -> int:
        """从分录重新推导出这个账户的余额——账本作为真源，独立于任何缓存。"""
        return sum(e.delta for e in self._by_account.get(account_id, ()))

    def total_delta(self) -> int:
        """全账本所有分录相加。每一笔移动都成对写入、两条相加为零，所以这个数恒为零；
        它是"移动是否真的都成对落账"的回归检验，而不是一句自然成立就不必测的话。
        """
        return sum(e.delta for e in self._entries)

    def count_for(self, account_id: str) -> int:
        """这个账户一共有多少条分录——分页 UI 用它算总页数。"""
        return len(self._by_account.get(account_id, ()))

    def page(self, account_id: str, offset: int, limit: int) -> tuple[LedgerEntry, ...]:
        """这个账户的一页交易记录，最新的排最前。加分页不需要改这个类之外的任何一行——
        `_by_account` 这份索引从第 2 关起就存在，分页只是对已有数据换一种读法。
        """
        entries = self._by_account.get(account_id, [])
        ordered = tuple(reversed(entries))
        return ordered[offset:offset + limit]

    def entries_for_transfer(self, transfer_id: str) -> tuple[LedgerEntry, LedgerEntry]:
        """一次移动落账的那两条分录——查证"每笔移动确实是两条分录"时，这是可以直接
        拿出来看的证据，而不是一句停留在文档里的承诺。
        """
        entries = self._by_transfer.get(transfer_id, [])
        if len(entries) != 2:
            raise LedgerIntegrityError(f"未知的移动：{transfer_id}")
        return entries[0], entries[1]


@dataclass(frozen=True, slots=True)
class TransferReceipt:
    """一次移动（充值/提现/转账）的回执；幂等重试返回的就是这同一个对象。"""

    transfer_id: str
    from_account: str
    to_account: str
    amount: int
    at: datetime
    client_key: str | None


class Wallet:
    """充值、提现、转账、查余额、查流水的唯一入口。

    三个看起来不同的操作在底层收敛成同一个私有原语 `_move`：充值是 `EXTERNAL → 账户`，
    提现是 `账户 → EXTERNAL`，转账是两个真实账户之间；`EXTERNAL` 是一个保留账户
    （`Account.reserved`），代表"系统外部"，允许余额为负——这正是钱从外部进入这个封闭
    系统的方式。`_move` 默认拒绝把保留账户当成调用方传入的任意一端，`top_up`/
    `withdraw`/开户入金三处内部调用显式选择放开这条限制，见 `_move` 的说明。
    """

    def __init__(self, clock: Callable[[], datetime]) -> None:
        self._clock = clock
        self._accounts: dict[str, Account] = {
            EXTERNAL_ACCOUNT_ID: Account(EXTERNAL_ACCOUNT_ID, reserved=True)}
        self._registry_lock = threading.Lock()
        self._ledger = Ledger()
        self._idempotency: dict[str, TransferReceipt] = {}
        self._idempotency_lock = threading.Lock()
        self._ids = (f"T{n}" for n in itertools.count(1))

    def open_account(self, account_id: str, opening_balance: int = 0) -> None:
        """开一个新账户，可带一笔起始余额——起始余额同样是一笔"外部注入"，走的是
        `_move`，纳入同一本账，不给自己开特权后门。
        """
        if opening_balance < 0:
            raise InvalidAmountError("开户余额不能为负")
        with self._registry_lock:
            if account_id in self._accounts:
                raise WalletError(f"账户已存在：{account_id}")
            self._accounts[account_id] = Account(account_id)
        if opening_balance:
            self._move(EXTERNAL_ACCOUNT_ID, account_id, opening_balance, "开户入金", None,
                       allow_reserved=True)

    def _account(self, account_id: str) -> Account:
        account = self._accounts.get(account_id)
        if account is None:
            raise UnknownAccountError(f"未知账户：{account_id}")
        return account

    def _move(self, from_id: str, to_id: str, amount: int, memo: str,
              client_key: str | None, *, allow_reserved: bool = False) -> TransferReceipt:
        """所有资金移动的唯一入口：校验 → 按稳定顺序加锁 → 幂等检查 → 记账 → 改缓存。

        锁按账户 id 的字典序取，不按参数 `(from_id, to_id)` 的顺序取：否则 A 转 B 的线程
        先锁 A 再锁 B，B 转 A 的线程先锁 B 再锁 A，两个方向同时发生就是经典的环形等待
        死锁。稳定顺序下，两个方向的转账永远以同一个次序竞争同一把锁，只会互相排队，
        不会互相等待。

        `allow_reserved` 默认 `False`：只要有一端是保留账户（`Account.reserved`），
        直接拒绝。只有 `top_up`/`withdraw`/开户入金这三处内部调用传 `allow_reserved=
        True`——它们的保留账户那一端是方法内部写死的常量，不是调用方传进来的字符串。
        这样任何以后新增的公开方法，只要复用 `_move` 而不主动传这个参数，默认就是安全
        的：不会因为"忘了另外挡一下 `EXTERNAL`"而意外放开一个可以凭空转账的后门——
        安全的做法是默认值本身就安全，而不是要求每个调用方都记得加一次检查。
        """
        if amount <= 0:
            raise InvalidAmountError(f"金额必须为正：{amount}")
        if from_id == to_id:
            raise SameAccountTransferError("转账双方不能是同一个账户")
        a, b = self._account(from_id), self._account(to_id)
        if not allow_reserved and (a.reserved or b.reserved):
            raise UnknownAccountError(f"{EXTERNAL_ACCOUNT_ID}：保留账户，不能作为转账的任意一端")
        lo, hi = (a, b) if a.id < b.id else (b, a)
        with lo.lock, hi.lock:
            if client_key is not None:
                with self._idempotency_lock:
                    cached = self._idempotency.get(client_key)
                if cached is not None:
                    if (cached.from_account, cached.to_account, cached.amount) != (from_id, to_id, amount):
                        raise IdempotencyConflictError(
                            f"client_key {client_key!r} 已经用于另一笔不同的移动")
                    return cached
            if not a.reserved and a.balance < amount:
                raise InsufficientFundsError(from_id, a.balance, amount)
            transfer_id = next(self._ids)
            at = self._clock()
            self._ledger.record_pair(transfer_id, (from_id, -amount), (to_id, amount), memo, at)
            a.balance -= amount
            b.balance += amount
            receipt = TransferReceipt(transfer_id, from_id, to_id, amount, at, client_key)
            if client_key is not None:
                with self._idempotency_lock:
                    self._idempotency[client_key] = receipt
            return receipt

    def top_up(self, account_id: str, amount: int, client_key: str | None = None) -> TransferReceipt:
        """充值：`EXTERNAL → account_id`。"""
        return self._move(EXTERNAL_ACCOUNT_ID, account_id, amount, "充值", client_key,
                          allow_reserved=True)

    def withdraw(self, account_id: str, amount: int, client_key: str | None = None) -> TransferReceipt:
        """提现：`account_id → EXTERNAL`。"""
        return self._move(account_id, EXTERNAL_ACCOUNT_ID, amount, "提现", client_key,
                          allow_reserved=True)

    def transfer(self, from_id: str, to_id: str, amount: int,
                 client_key: str | None = None) -> TransferReceipt:
        """两个真实账户之间转账；任何一端是保留的 `EXTERNAL` 账户都拒绝——那是内部
        用来给充值/提现建模的记账对手方，不是一个用户可以转钱进出的普通账户。这里不用
        再自己判断 `from_id`/`to_id` 是不是 `EXTERNAL_ACCOUNT_ID`：`_move` 在
        `allow_reserved` 取默认值 `False` 时已经统一挡住了，见该方法的说明。
        """
        return self._move(from_id, to_id, amount, "转账", client_key)

    def balance(self, account_id: str) -> int:
        """当前缓存余额；持锁读，避免读到改到一半的账户。"""
        account = self._account(account_id)
        with account.lock:
            return account.balance

    def history(self, account_id: str, offset: int = 0, limit: int = 20) -> tuple[LedgerEntry, ...]:
        """这个账户的一页交易记录，最新的排最前。"""
        self._account(account_id)
        return self._ledger.page(account_id, offset, limit)

    def history_count(self, account_id: str) -> int:
        """这个账户一共有多少条流水——分页 UI 用它算总页数。"""
        self._account(account_id)
        return self._ledger.count_for(account_id)

    def transfer_entries(self, transfer_id: str) -> tuple[LedgerEntry, LedgerEntry]:
        """一次移动（充值/提现/转账）落账的那两条分录。"""
        return self._ledger.entries_for_transfer(transfer_id)

    def derived_balance(self, account_id: str) -> int:
        """从账本重新推导出的余额，不经过缓存——核对缓存是否漂移时用它做基准。"""
        self._account(account_id)
        return self._ledger.derived_balance(account_id)

    @property
    def ledger_size(self) -> int:
        """账本里一共有多少条分录；只增不减。"""
        return self._ledger.entry_count

    def ledger_total(self) -> int:
        """全账本所有分录相加，恒为零——每一笔移动都成对落账这条不变式的直接证据。"""
        return self._ledger.total_delta()

    def reconcile(self, account_id: str) -> bool:
        """核对缓存余额与账本推导值：一致则什么都不做，不一致就用账本的值纠正缓存，
        返回这次核对是否真的发生了纠正。这是"缓存并定期核对"这条设计承诺的落点——
        账本永远是被信任的一方，缓存只是它的一个投影，漂移了就被它覆盖。
        """
        account = self._account(account_id)
        derived = self._ledger.derived_balance(account_id)
        with account.lock:
            if account.balance == derived:
                return False
            account.balance = derived
            return True

    def purge_idempotency_before(self, cutoff: datetime) -> int:
        """清掉发生在 `cutoff` 之前的幂等回执，返回清掉的条数。没有这一步，`_idempotency`
        会随着客户端重试的笔数无限增长——这是这个设计里必须有出口的那个容器（账本本身
        是审计流水，故意不清，见 `Ledger.entry_count` 的说明）。
        """
        with self._idempotency_lock:
            gone = [k for k, r in self._idempotency.items() if r.at < cutoff]
            for key in gone:
                del self._idempotency[key]
        return len(gone)


if __name__ == "__main__":
    from datetime import UTC

    now = datetime(2026, 1, 1, 9, 0, tzinfo=UTC)
    wallet = Wallet(clock=lambda: now)
    wallet.open_account("alice", opening_balance=5000)
    wallet.open_account("bob")

    wallet.top_up("bob", 2000)
    receipt = wallet.transfer("alice", "bob", 1500, client_key="req-1")
    again = wallet.transfer("alice", "bob", 1500, client_key="req-1")
    assert receipt == again, "同一个 client_key 的重试不应该再转一次"

    print("alice:", wallet.balance("alice"), "bob:", wallet.balance("bob"))
    print("alice reconcile:", wallet.reconcile("alice"))
    print("bob 最近流水:", wallet.history("bob", limit=5))
    print("这笔转账的两条分录:", wallet.transfer_entries(receipt.transfer_id))
    print("账本总和:", wallet.ledger_total(), "分录条数:", wallet.ledger_size)
