"""银行账户系统（Bank Account System）——分关递进机考题的参考实现。

五行设计：没有任何"当前余额"字段，`EventLog` 是只增不减的事件表，余额、排行都是对它的
一次归约（reduce）；没有 `self._clock`——这个系统没有后台线程，每次调用显式传入时间戳，
"到期的定时支付"只在下一次任意调用发生时才被结算，这正是"一切由传入的时间戳驱动"的字面
实现；账户 id 一旦创建永不复用，合并只是把一个 id 从"活跃"挪到"不再接受新操作"，它自己
的历史原样留在日志里，历史时点查询因此不需要任何特殊代码；账户 id 之间没有互相持有的
引用，合并、排行、结算都通过 `account_id: str` 这一个共同的键联系在一起。
"""

from __future__ import annotations

import heapq
import itertools
from dataclasses import dataclass
from enum import Enum


class BankError(Exception):
    """本设计里所有失败路径的公共基类。"""


class UnknownAccountError(BankError):
    """账户不存在，或者曾经存在但已经被合并掉、不再接受新操作。"""


class DuplicateAccountError(BankError):
    """这个账户 id 曾经被用过（哪怕现在已经合并掉了），不能再开一个同名账户。"""


class InvalidAmountError(BankError):
    """金额不是正数。"""


class SameAccountError(BankError):
    """转账或合并的两个账户 id 其实是同一个。"""


class InsufficientFundsError(BankError):
    """余额不足以覆盖这笔转出或定时支付。"""

    def __init__(self, account_id: str, available: int, requested: int) -> None:
        super().__init__(f"账户 {account_id} 余额 {available} 不足以支付 {requested}")
        self.account_id = account_id
        self.shortfall = requested - available


class UnknownPaymentError(BankError):
    """定时支付 id 不存在。"""


class InvalidPaymentStateError(BankError):
    """这笔定时支付已经结算或已经取消，不能再取消一次。"""


class NonMonotonicTimestampError(BankError):
    """这次调用的时间戳比上一次调用还早——这套系统假设调用方按时间顺序发起请求。"""


class EventKind(Enum):
    """一条事件描述的是哪一类资金变化；`top_spenders` 只统计 `TRANSFER_OUT`，其余
    种类只参与余额归约——这是"排行只算转账支出"这条产品假设在代码里的落点，改成也算
    定时支付的支出时，只需要在 `top_spenders` 的过滤条件里加一个种类。
    """

    OPENED = "opened"
    DEPOSIT = "deposit"
    TRANSFER_OUT = "transfer_out"
    TRANSFER_IN = "transfer_in"
    PAYMENT_OUT = "payment_out"
    PAYMENT_REFUND = "payment_refund"
    CASHBACK_IN = "cashback_in"
    MERGE_IN = "merge_in"


class PaymentStatus(Enum):
    IN_PROGRESS = "in_progress"
    CASHBACK_RECEIVED = "cashback_received"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class Event:
    """一条不可变的账户历史记录：`account_id` 在时间戳 `at` 变化了 `delta`（带符号，
    正数入账、负数出账）。它是这个设计里唯一的真源，`Bank` 自己不缓存任何余额。
    """

    seq: int
    kind: EventKind
    account_id: str
    at: int
    delta: int


@dataclass(slots=True)
class Payment:
    """一笔定时支付：立即扣款，`matures_at` 时刻返现。`account_id` 是**可变**的——
    如果这笔支付所属的账户在返现到账之前被合并掉，它会被改指到合并后存活的账户，
    这就是"定时支付随账户一起合并"的全部实现。
    """

    id: str
    account_id: str
    amount: int
    scheduled_at: int
    matures_at: int
    status: PaymentStatus = PaymentStatus.IN_PROGRESS


class EventLog:
    """账户历史的唯一真源：一张按账户 id 分组、只增不减的事件表。它不知道"合并"、
    "定时支付"这些业务概念，只知道"某个 id 在某个时间点变化了多少"——`balance` 和
    `outgoing_total` 都只是对这份历史做一次带时间上限的归约。一个账户被合并掉之后，
    只是不再有新事件写进它自己的这一份历史，历史本身永远留着，这正是"合并后的 id
    依然能回答历史时点的余额查询"不需要任何专门代码的原因。
    """

    def __init__(self) -> None:
        self._events: dict[str, list[Event]] = {}
        self._seq = itertools.count(1)

    def append(self, account_id: str, kind: EventKind, at: int, delta: int) -> Event:
        event = Event(next(self._seq), kind, account_id, at, delta)
        self._events.setdefault(account_id, []).append(event)
        return event

    def balance(self, account_id: str, at: int) -> int:
        """`account_id` 在时间戳 `at` 那一刻的余额：账户从未开户、或者查询的时刻
        早于开户时刻，历史里没有任何一条落在范围内的事件，归约的结果自然是 0——
        不需要单独判断"这个时刻账户还不存在"。
        """
        return sum(e.delta for e in self._events.get(account_id, ()) if e.at <= at)

    def outgoing_total(self, account_id: str, at: int) -> int:
        """`account_id` 在时间戳 `at` 之前转出去过多少钱——`top_spenders` 排行用的
        正是这个数。
        """
        return sum(-e.delta for e in self._events.get(account_id, ())
                    if e.at <= at and e.kind is EventKind.TRANSFER_OUT)

    def entries(self, account_id: str) -> tuple[Event, ...]:
        """`account_id` 的完整历史快照——按追加顺序，不把内部列表本身交出去。"""
        return tuple(self._events.get(account_id, ()))


class Bank:
    """开户、存款、转账、按支出排行、定时支付带返现、合并账户的唯一入口。

    没有任何"当前余额"字段——每一次余额、排行查询都是对 `EventLog` 的一次归约；也没有
    `self._clock`：这个系统完全没有后台线程或墙上时钟，"现在几点"由调用方在每一次调用
    里显式传入，"到期"只在下一次任意调用发生时才会被观察到并处理——这是"驱动一切的是
    传进来的时间戳"这条要求最直接的样子，测试也因此从不需要 `sleep`。
    """

    def __init__(self, cashback_rate: float = 0.02) -> None:
        self._log = EventLog()
        self._known_ids: set[str] = set()
        self._active: set[str] = set()
        self._payments: dict[str, Payment] = {}
        self._due: list[tuple[int, int, str]] = []
        self._payment_ids = (f"PAY{n}" for n in itertools.count(1))
        self._cashback_rate = cashback_rate
        self._last_timestamp = 0

    def _settle_due(self, timestamp: int) -> None:
        """结算所有在 `timestamp` 之前到期的定时支付。返现事件记在**真正到期的那一刻**
        `matures_at`，不是这次触发结算的调用的时间戳——不然一次晚到的调用会让返现在
        账本里显得比实际发生得更晚，任何查询"到期和触发之间某一刻"余额的调用都会得到
        错误答案（少算一笔早就该到账的返现）。谁先调用、什么时候调用，不该改变钱真正
        落账的时间点。
        """
        while self._due and self._due[0][0] <= timestamp:
            matures_at, _, payment_id = heapq.heappop(self._due)
            payment = self._payments[payment_id]
            if payment.status is not PaymentStatus.IN_PROGRESS:
                continue  # 已经被取消——堆里这条过期条目直接丢弃，不需要额外清理它
            cashback = round(payment.amount * self._cashback_rate)
            self._log.append(payment.account_id, EventKind.CASHBACK_IN, matures_at, cashback)
            payment.status = PaymentStatus.CASHBACK_RECEIVED

    def _advance(self, timestamp: int) -> None:
        """写操作的第一步：校验这次调用的时间戳没有比上一次写操作倒退，把它记成新的
        "当前时间"，再结算所有到期的定时支付。只读的 `get_balance` 不走这个方法——
        它可以查询任意历史时刻，见该方法的说明。
        """
        if timestamp < self._last_timestamp:
            raise NonMonotonicTimestampError(
                f"时间戳必须不小于上一次调用的时间戳（{self._last_timestamp}），收到 {timestamp}")
        self._last_timestamp = timestamp
        self._settle_due(timestamp)

    def _require_active(self, account_id: str) -> None:
        if account_id not in self._active:
            raise UnknownAccountError(f"账户不存在或已经合并：{account_id}")

    @property
    def payment_count(self) -> int:
        """一共开过多少笔定时支付——包括已经返现、已经取消的，这张表和 `EventLog`
        一样是审计记录，故意不清理。"""
        return len(self._payments)

    @property
    def pending_payment_count(self) -> int:
        """还没有返现也没有被取消的定时支付有多少笔；结算/取消都会让这个数变小，
        是"`_due` 这个堆确实会缩小"这条不变式可以直接断言的证据。"""
        return sum(1 for p in self._payments.values() if p.status is PaymentStatus.IN_PROGRESS)

    def history(self, account_id: str) -> tuple[Event, ...]:
        """这个账户的完整历史，用于查证"每一步都被正确地记进了日志"——测试和面试演示
        都靠这个方法看账本，而不是伸手进 `Bank` 内部拿私有字段。
        """
        if account_id not in self._known_ids:
            raise UnknownAccountError(f"未知账户：{account_id}")
        return self._log.entries(account_id)

    def create_account(self, timestamp: int, account_id: str) -> None:
        """第 1 关：开户。id 一旦用过永不复用，即使对应账户后来被合并掉了。"""
        self._advance(timestamp)
        if account_id in self._known_ids:
            raise DuplicateAccountError(f"账户 id 已经被使用过：{account_id}")
        self._known_ids.add(account_id)
        self._active.add(account_id)
        self._log.append(account_id, EventKind.OPENED, timestamp, 0)

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int:
        """第 1 关：存款，返回存款后的余额。"""
        self._advance(timestamp)
        self._require_active(account_id)
        if amount <= 0:
            raise InvalidAmountError(f"金额必须为正：{amount}")
        self._log.append(account_id, EventKind.DEPOSIT, timestamp, amount)
        return self._log.balance(account_id, timestamp)

    def transfer(self, timestamp: int, source_id: str, target_id: str, amount: int) -> int:
        """第 1 关：转账，返回转出方转账后的余额。"""
        self._advance(timestamp)
        if source_id == target_id:
            raise SameAccountError("转账双方不能是同一个账户")
        self._require_active(source_id)
        self._require_active(target_id)
        if amount <= 0:
            raise InvalidAmountError(f"金额必须为正：{amount}")
        available = self._log.balance(source_id, timestamp)
        if available < amount:
            raise InsufficientFundsError(source_id, available, amount)
        self._log.append(source_id, EventKind.TRANSFER_OUT, timestamp, -amount)
        self._log.append(target_id, EventKind.TRANSFER_IN, timestamp, amount)
        return self._log.balance(source_id, timestamp)

    def get_balance(self, timestamp: int, account_id: str) -> int:
        """查询某个账户在 `timestamp` 那一刻的余额；被合并掉的 id 同样可以查——它的
        历史没有被删除，只是不会再增长。这是一次纯读取，`timestamp` 可以是**任意**
        历史时刻，不要求不小于上一次调用的时间戳，也不会把它记成新的"当前时间"——这
        正是"合并掉的账户依然能按过去某个时间点回答余额查询"必须成立的地方：如果查
        历史也要满足"只能越查越晚"，就没法在合并之后再回头问合并之前的余额了。它仍然
        会结算截至 `timestamp` 为止到期的定时支付，理由见 `_settle_due`。
        """
        if account_id not in self._known_ids:
            raise UnknownAccountError(f"未知账户：{account_id}")
        self._settle_due(timestamp)
        return self._log.balance(account_id, timestamp)

    def top_spenders(self, timestamp: int, n: int) -> list[tuple[str, int]]:
        """第 2 关：按截至 `timestamp` 的转账支出总额从高到低取前 `n` 个活跃账户，
        支出相同则按账户 id 升序；支出为 0 的账户不上榜。
        """
        self._advance(timestamp)
        totals = ((account_id, self._log.outgoing_total(account_id, timestamp))
                   for account_id in self._active)
        ranked = sorted((t for t in totals if t[1] > 0), key=lambda t: (-t[1], t[0]))
        return ranked[:n]

    def schedule_payment(self, timestamp: int, account_id: str, amount: int,
                          cashback_delay: int) -> str:
        """第 3 关：立即扣款，`cashback_delay` 之后返还 `amount * cashback_rate`
        （四舍五入到整数最小货币单位）。返现不是"到点自动发生"，是**下一次任意调用**
        经过 `_advance` 时被结算——这套系统里唯一会推进"时间"的地方。
        """
        self._advance(timestamp)
        self._require_active(account_id)
        if amount <= 0:
            raise InvalidAmountError(f"金额必须为正：{amount}")
        available = self._log.balance(account_id, timestamp)
        if available < amount:
            raise InsufficientFundsError(account_id, available, amount)
        payment_id = next(self._payment_ids)
        matures_at = timestamp + cashback_delay
        self._payments[payment_id] = Payment(payment_id, account_id, amount, timestamp, matures_at)
        heapq.heappush(self._due, (matures_at, len(self._payments), payment_id))
        self._log.append(account_id, EventKind.PAYMENT_OUT, timestamp, -amount)
        return payment_id

    def cancel_payment(self, timestamp: int, payment_id: str) -> None:
        """第 3 关：取消一笔还没有返现的定时支付，扣掉的本金退回去。"""
        self._advance(timestamp)
        payment = self._payments.get(payment_id)
        if payment is None:
            raise UnknownPaymentError(f"未知的定时支付：{payment_id}")
        if payment.status is not PaymentStatus.IN_PROGRESS:
            raise InvalidPaymentStateError(
                f"支付 {payment_id} 已经是 {payment.status.value}，不能再取消")
        payment.status = PaymentStatus.CANCELLED
        self._log.append(payment.account_id, EventKind.PAYMENT_REFUND, timestamp, payment.amount)

    def payment_status(self, timestamp: int, payment_id: str) -> PaymentStatus:
        self._advance(timestamp)
        payment = self._payments.get(payment_id)
        if payment is None:
            raise UnknownPaymentError(f"未知的定时支付：{payment_id}")
        return payment.status

    def merge_accounts(self, timestamp: int, survivor_id: str, absorbed_id: str) -> None:
        """第 4 关：把 `absorbed_id` 合并进 `survivor_id`。`absorbed_id` 当前的余额
        整笔计入 `survivor_id`，它名下还没有返现的定时支付改由 `survivor_id` 持有；
        `absorbed_id` 从"活跃账户"里移除，但它的历史留在日志里，`get_balance` 依然
        能查——见 `EventLog` 的说明。
        """
        self._advance(timestamp)
        if survivor_id == absorbed_id:
            raise SameAccountError("不能把一个账户合并进它自己")
        self._require_active(survivor_id)
        self._require_active(absorbed_id)
        absorbed_balance = self._log.balance(absorbed_id, timestamp)
        for payment in self._payments.values():
            if payment.account_id == absorbed_id and payment.status is PaymentStatus.IN_PROGRESS:
                payment.account_id = survivor_id
        if absorbed_balance:
            self._log.append(survivor_id, EventKind.MERGE_IN, timestamp, absorbed_balance)
        self._active.discard(absorbed_id)


if __name__ == "__main__":
    bank = Bank(cashback_rate=0.02)
    bank.create_account(0, "alice")
    bank.create_account(0, "bob")
    bank.deposit(10, "alice", 10_000)
    bank.transfer(20, "alice", "bob", 3_000)
    payment_id = bank.schedule_payment(30, "bob", 1_000, cashback_delay=100)

    print("alice:", bank.get_balance(40, "alice"), "bob:", bank.get_balance(40, "bob"))
    print("排行:", bank.top_spenders(40, 5))
    print("返现前状态:", bank.payment_status(40, payment_id))
    bank.merge_accounts(50, "alice", "bob")
    print("合并后 alice:", bank.get_balance(150, "alice"))
    print("合并后返现落到 alice 而不是 bob，状态:", bank.payment_status(150, payment_id))
    print("bob 合并前的历史仍然可查:", bank.get_balance(45, "bob"))
