"""ATM 取款机——会话状态机、钞票选取，以及"账户余额"和"钞箱存量"两个权威之间的对账。

核心思路：会话合法性是一张 `dict[(状态, 动作), 新状态]` 的授权表，非法动作按名字拒绝；
PIN 失败计数归发卡行（换一台机器接着错，还是同一个计数），吞卡归机器（塑料在机器手里）。
取款跨两个权威，没有原子性可言，于是顺序定死为"先从钞箱抽出钞票 → 再请银行扣账 → 最后
交到出钞口"：失败时回滚的永远是**本地**那一半，远端那一半只能用一笔冲正（reversal）抵消，
并落在只增不改的流水里。钞票守恒（钞箱＋出钞口＋回收箱＋已取走＝装钞总额）由 `cash_up()`
随时可验——这条不变式才是这台机器"没吞钱"的证据。
"""

from __future__ import annotations

import math
import threading
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, IntEnum
from types import MappingProxyType
from typing import Protocol

YUAN = 100  # 金额一律用整数分；面额、余额都是分


class Note(IntEnum):
    """机器支持的钞票面额（单位：分）。枚举值就是面值，可以直接参与算术。"""

    TEN = 10 * YUAN
    TWENTY = 20 * YUAN
    FIFTY = 50 * YUAN
    HUNDRED = 100 * YUAN


# 面额的最大公约数：不是它整数倍的金额，**无论钞箱装多满**都吐不出来。
NOTE_STEP = math.gcd(*(int(n) for n in Note))
# 送钞机构一次能送出的张数上限，真实机器在 30～60 张之间。
MAX_NOTES_PER_DISPENSE = 40


class SessionState(Enum):
    """一次会话所处的阶段。只有四个，但它是这台机器的安全边界。"""

    IDLE = "idle"
    CARD_INSERTED = "card_inserted"
    AUTHENTICATED = "authenticated"
    DISPENSING = "dispensing"


class Action(Enum):
    """会话里可能发生的动作。带 `_` 前缀的是机器自己触发的，不对外暴露成方法。"""

    INSERT_CARD = "insert_card"
    ENTER_PIN = "enter_pin"
    PIN_REJECTED = "_pin_rejected"
    RETAIN_CARD = "_retain_card"
    BALANCE = "balance"
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    COLLECT_CASH = "collect_cash"
    EJECT = "eject_card"


# 授权表：会话状态机的全部合法转移。表里没有的组合一律非法，于是"没插卡就取款""没输密码
# 就查余额""出钞过程中退卡"由同一份数据统一拒绝，而且能被一个穷举测试盖满。
TRANSITIONS: dict[tuple[SessionState, Action], SessionState] = {
    (SessionState.IDLE, Action.INSERT_CARD): SessionState.CARD_INSERTED,
    (SessionState.CARD_INSERTED, Action.ENTER_PIN): SessionState.AUTHENTICATED,
    (SessionState.CARD_INSERTED, Action.PIN_REJECTED): SessionState.CARD_INSERTED,
    (SessionState.CARD_INSERTED, Action.RETAIN_CARD): SessionState.IDLE,
    (SessionState.CARD_INSERTED, Action.EJECT): SessionState.IDLE,
    (SessionState.AUTHENTICATED, Action.BALANCE): SessionState.AUTHENTICATED,
    (SessionState.AUTHENTICATED, Action.DEPOSIT): SessionState.AUTHENTICATED,
    (SessionState.AUTHENTICATED, Action.WITHDRAW): SessionState.DISPENSING,
    (SessionState.AUTHENTICATED, Action.EJECT): SessionState.IDLE,
    (SessionState.DISPENSING, Action.COLLECT_CASH): SessionState.AUTHENTICATED,
}


class ATMError(Exception):
    """本设计全部失败路径的公共基类。"""


class IllegalActionError(ATMError):
    """这个动作在当前会话状态下不合法（授权表里没有这一项）。"""


class WrongPinError(ATMError):
    """密码错误。

    卡不存在、卡已被冻结，报的也是它，连消息都一样——否则这台机器就成了账号枚举器。
    `remaining` 是这张卡还剩几次机会；为 0 表示卡已经作废，机器应当把它留下。
    """

    def __init__(self, remaining: int) -> None:
        super().__init__(f"wrong PIN, {remaining} attempt(s) left")
        self.remaining = remaining


class CardRetainedError(ATMError):
    """卡被机器吞掉了（连续三次密码错误，或插入了一张已作废的卡）。"""


class InvalidAmountError(ATMError):
    """金额不是正数，或者钞票张数为负。"""


class InsufficientFundsError(ATMError):
    """账户余额不足。这条不变式归账户所有，ATM 只能听银行的回答。"""


class DispenseFailure(Enum):
    """"取不出来"的三种理由。分清楚它们，屏幕才说得出下一步该怎么办。"""

    NOT_REPRESENTABLE = "amount is not a multiple of the smallest note"
    NOT_IN_STOCK = "the cassettes cannot make this amount"
    TOO_MANY_NOTES = "the amount needs more notes than the feeder can move"


class AmountNotDispensableError(ATMError):
    """这笔金额吐不出来。`reason` 说明是哪一种，账户和钞箱都没有被动过。"""

    def __init__(self, amount: int, reason: DispenseFailure) -> None:
        super().__init__(f"cannot dispense {amount}: {reason.value}")
        self.amount = amount
        self.reason = reason


class TxKind(Enum):
    """流水的种类。"""

    WITHDRAWAL = "withdrawal"
    DEPOSIT = "deposit"
    BALANCE = "balance"
    REVERSAL = "reversal"
    PIN_FAILURE = "pin_failure"
    CARD_RETAINED = "card_retained"


class TxStatus(Enum):
    """流水的结局。`REVERSED` 是一条**新增**的冲正记录，原记录永远不改。"""

    OK = "ok"
    DECLINED = "declined"
    REVERSED = "reversed"


@dataclass(frozen=True, slots=True)
class JournalEntry:
    """一条流水：一次动作发生过什么。不可变、只增不改。

    它自带读它的人需要的全部字段，因此对账、打凭条、集中监控都不必回头去读机器的内部
    容器。卡号只留后四位：流水会被导出、被打印，不该带着完整卡号到处跑。
    """

    ref: str
    at: datetime
    kind: TxKind
    status: TxStatus
    amount: int
    card_tail: str
    detail: str = ""


@dataclass(frozen=True, slots=True)
class Reconciliation:
    """一次对账（cash-up）的结果：机器该有多少钞票、实际有多少。"""

    loaded: int
    in_cassette: int
    on_tray: int
    in_reject_bin: int
    collected: int
    deposited: int

    @property
    def balanced(self) -> bool:
        """钞票守恒：装进来的钱要么还在机器里，要么被客户拿走了，不会凭空消失。"""
        return self.loaded == self.in_cassette + self.on_tray + self.in_reject_bin + self.collected


class Cassette:
    """一组钞箱：每种面额各有多少张。出钞口、回收箱、存钞箱都是它的不同角色。

    不变式：张数降到 0 的面额会被从字典里删掉。这不是洁癖——选钞算法遍历的就是这张表，
    留一条"20 元：0 张"会让它把一种其实没有的钞票算进可用集合，于是给出一个兑不出来的
    方案，而这种错往往要等到送钞那一刻才暴露。
    """

    def __init__(self, counts: Mapping[Note, int] | None = None) -> None:
        self._counts: dict[Note, int] = {n: c for n, c in (counts or {}).items() if c > 0}

    def counts(self) -> Mapping[Note, int]:
        """一份只读快照；钞箱从不把自己的字典交出去。"""
        return MappingProxyType(dict(self._counts))

    @property
    def total(self) -> int:
        """箱内金额合计（分）。"""
        return sum(int(note) * c for note, c in self._counts.items())

    @property
    def note_count(self) -> int:
        """箱内张数。

        它是一个只读的计数，所以测试可以断言"钞箱少了正好这么多张"，而不必去读内部字典。
        对账时"金额对得上、张数对不上"意味着某处把面额记错了。
        """
        return sum(self._counts.values())

    def load(self, counts: Mapping[Note, int]) -> None:
        """装钞，也用于把留好的钞票原样放回。"""
        for note, c in counts.items():
            if c < 0:
                raise InvalidAmountError(f"cannot load {c} × {note.name}")
            if c:
                self._counts[note] = self._counts.get(note, 0) + c

    def take(self, plan: Mapping[Note, int]) -> None:
        """按方案取走钞票：先整体校验再整体扣减，取空的面额立刻从字典里消失。"""
        for note, c in plan.items():
            if self._counts.get(note, 0) < c:
                raise AmountNotDispensableError(
                    sum(int(n) * k for n, k in plan.items()), DispenseFailure.NOT_IN_STOCK)
        for note, c in plan.items():
            if not c:
                continue
            self._counts[note] -= c
            if self._counts[note] == 0:
                del self._counts[note]


# 选钞策略：给金额和一份"可用钞票"计数，给出一种凑法或者 `None`。纯函数，构造时注入。
NoteSelector = Callable[[int, Mapping[Note, int]], "dict[Note, int] | None"]


def fewest_notes(amount: int, available: Mapping[Note, int]) -> dict[Note, int] | None:
    """有界背包 DP：在库存允许的所有凑法里选张数最少的一种，没有凑法就返回 `None`。

    张数最少不是审美：送钞机构一次能送的张数有硬上限，张数少还意味着卡钞概率低、清点快。
    规模是"几种面额 × 几百个格子"，这点代价完全付得起，换来的是绝不误报"取不出"——
    那等于把一次本可以成交的取款拒掉。
    """
    if amount == 0:
        return {}
    step = math.gcd(*(int(n) for n in available)) if available else 0
    if step == 0 or amount % step:
        return None
    notes = sorted(available, reverse=True)
    cells = amount // step
    # best[i][v]：只用前 i 种面额凑出 v*step 所需的最少张数，`None` 表示凑不出。
    best: list[list[int | None]] = [[None] * (cells + 1) for _ in range(len(notes) + 1)]
    best[0][0] = 0
    for i, note in enumerate(notes, start=1):
        unit, row, prev = int(note) // step, best[i], best[i - 1]
        for v in range(cells + 1):
            row[v] = prev[v]
            for used in range(1, available[note] + 1):
                if used * unit > v:
                    break
                head = prev[v - used * unit]
                if head is not None and (row[v] is None or head + used < row[v]):
                    row[v] = head + used
    if best[len(notes)][cells] is None:
        return None
    plan: dict[Note, int] = {}
    v = cells
    for i in range(len(notes), 0, -1):  # 回溯：逐层问"这一种面额到底用了几张"
        note, unit = notes[i - 1], int(notes[i - 1]) // step
        for used in range(available[note] + 1):
            head = best[i - 1][v - used * unit] if used * unit <= v else None
            if head is not None and head + used == best[i][v]:
                if used:
                    plan[note] = used
                v -= used * unit
                break
    return plan


@dataclass(slots=True)
class Account:
    """一个账户：余额，以及守着余额的那把锁。这条不变式归它所有，谁也替不了它。

    不变式：余额不为负。检查和扣减必须在同一把锁里做完——"先查后扣"分成两步就会被两个
    线程同时通过，这正是 GIL 保护不了的那类竞态。
    """

    account_id: str
    balance: int = 0
    lock: threading.Lock = field(default_factory=threading.Lock, repr=False, compare=False)

    def debit(self, amount: int) -> int:
        """扣款。不变式过了才动余额，否则一分不动。返回扣后余额。"""
        with self.lock:
            if amount > self.balance:
                raise InsufficientFundsError(f"balance {self.balance} < {amount}")
            self.balance -= amount
            return self.balance

    def credit(self, amount: int) -> int:
        """贷记：存款走它，冲正也走它。

        在账户这一层，冲正就是一次普通的贷记；让它成为"冲正"的是流水里那条引用原 `ref`
        的记录，以及它必须经由银行的 `reverse` 入口——ATM 没有别的路可以把钱加回去。
        """
        with self.lock:
            self.balance += amount
            return self.balance


class BankNetwork(Protocol):
    """ATM 能向"网络另一端"提出的全部问题，也是这台机器唯一的对外接缝。

    它把"余额归银行"从一句口号变成结构：这里**没有** `get_account()`，所以 ATM 永远拿不到
    账户对象，也就永远改不了任何人的余额，连写错的机会都没有。换一家银行、换一张跨行转接
    网络、换一个会超时的桩，都只是换一个满足这个协议的对象，机器本身一行不改。
    """

    def authenticate(self, card_number: str, pin: str) -> str:
        """验密码，通过则返回一个带路由信息的账户标识。"""

    def balance(self, account_id: str) -> int: ...

    def withdraw(self, account_id: str, amount: int, ref: str) -> int:
        """扣账成功返回扣后余额；失败抛异常，且保证远端一分未动。"""

    def deposit(self, account_id: str, amount: int, ref: str) -> int: ...

    def reverse(self, account_id: str, amount: int, ref: str) -> int:
        """冲正 `ref` 那笔取款。这是银行的补偿动作，不是 ATM 自己把钱加回去。"""


class LocalBank:
    """发卡行：管账户、管卡、管密码错误次数。

    密码错误计数放在银行而不是机器里，理由很直白：在三台不同的 ATM 上各错一次，仍然是
    三次错。机器能做的只是把塑料留下，让卡作废是银行的事。
    """

    def __init__(self, bank_id: str = "BANK", max_pin_attempts: int = 3) -> None:
        self.bank_id = bank_id
        self._max_attempts = max_pin_attempts
        self._accounts: dict[str, Account] = {}
        self._cards: dict[str, tuple[str, str]] = {}  # 卡号 -> (账户号, 密码)
        self._failed: dict[str, int] = {}
        self._blocked: set[str] = set()
        self._lock = threading.Lock()

    def open_account(self, account_id: str, balance: int = 0) -> Account:
        account = Account(account_id, balance=balance)
        self._accounts[account_id] = account
        return account

    def issue_card(self, card_number: str, account_id: str, pin: str) -> None:
        self._cards[card_number] = (account_id, pin)

    def account(self, account_id: str) -> Account:
        """给测试和柜面用的直查；ATM 走不到这里，`BankNetwork` 协议里没有它。"""
        return self._accounts[account_id]

    def authenticate(self, card_number: str, pin: str) -> str:
        """卡不存在、密码错、卡已作废，三种情形走同一条分支、抛同一个异常。"""
        with self._lock:
            record = self._cards.get(card_number)
            if card_number in self._blocked or record is None or record[1] != pin:
                if card_number in self._blocked:
                    raise WrongPinError(0)
                failed = self._failed.get(card_number, 0) + 1
                remaining = max(0, self._max_attempts - failed)
                if remaining == 0:
                    # 作废之后计数就没有意义了：再来的请求在上面那一行就被挡住。
                    self._blocked.add(card_number)
                    self._failed.pop(card_number, None)
                else:
                    self._failed[card_number] = failed
                raise WrongPinError(remaining)
            self._failed.pop(card_number, None)
            return record[0]

    def balance(self, account_id: str) -> int:
        return self._accounts[account_id].balance

    def withdraw(self, account_id: str, amount: int, ref: str) -> int:
        return self._accounts[account_id].debit(amount)

    def deposit(self, account_id: str, amount: int, ref: str) -> int:
        return self._accounts[account_id].credit(amount)

    def reverse(self, account_id: str, amount: int, ref: str) -> int:
        return self._accounts[account_id].credit(amount)


class ATM:
    """一台取款机：会话状态机、钞箱、流水，以及一条通往银行的网络。

    不变式：
    1. 任意时刻最多一个会话；退卡或吞卡后卡号、账户标识立刻清空。
    2. 钞票守恒：装钞总额 = 钞箱 + 出钞口 + 回收箱 + 客户已取走，`cash_up()` 随时可验。
    3. 取款失败时回滚本地那一半（留好的钞票原样放回钞箱），远端那一半发一笔冲正；
       两者都在流水里留痕，流水只增不改。
    4. 一把粗锁保护"查状态 → 查守卫 → 改状态"；一台机器只有一个出钞口，本就没有并行度
       可榨，细化锁只换来死锁风险。
    """

    def __init__(self, network: BankNetwork, cassette: Cassette, *,
                 selector: NoteSelector = fewest_notes,
                 clock: Callable[[], datetime] = datetime.now,
                 machine_id: str = "ATM-01") -> None:
        self._network = network
        self._cassette = cassette
        self._selector = selector
        self._clock = clock
        self._machine_id = machine_id
        self._tray = Cassette()          # 出钞口：已交付、客户还没拿走
        self._reject_bin = Cassette()    # 回收箱：客户没拿走被收回的钞票，永不再出
        self._deposit_bin = Cassette()   # 存钞箱：客户存进来的钞票，也永不再出
        self._loaded = cassette.total
        self._collected = 0
        self._deposited = 0
        self._state = SessionState.IDLE
        self._card: str | None = None
        self._account_id: str | None = None
        self._pending: tuple[str, int] | None = None  # 出钞口上那笔钱的 (流水号, 金额)
        self._seq = 0
        self._journal: list[JournalEntry] = []
        self._lock = threading.RLock()

    # ---- 只读视图：一律交出快照或计数，从不把内部容器交出去 ----

    @property
    def state(self) -> SessionState:
        return self._state

    def cassette_counts(self) -> Mapping[Note, int]:
        with self._lock:
            return self._cassette.counts()

    def tray_counts(self) -> Mapping[Note, int]:
        """出钞口上正等着客户拿走的钞票。取款和收回都靠它才能被独立地断言。"""
        with self._lock:
            return self._tray.counts()

    def journal(self) -> tuple[JournalEntry, ...]:
        with self._lock:
            return tuple(self._journal)

    def cash_up(self) -> Reconciliation:
        """对账：把机器里现在的钱和装钞总额摆在一起。`balanced` 为假就该停机查。"""
        with self._lock:
            return Reconciliation(loaded=self._loaded, in_cassette=self._cassette.total,
                                  on_tray=self._tray.total, in_reject_bin=self._reject_bin.total,
                                  collected=self._collected, deposited=self._deposited)

    # ---- 第 1 关：会话状态机 ----

    def insert_card(self, card_number: str) -> SessionState:
        """插卡。

        **这里什么都不验证**：卡认不认识要等密码来了才知道，否则插一张卡就能试出它存不存在，
        机器成了账号枚举器。
        """
        with self._lock:
            nxt = self._next(Action.INSERT_CARD)
            self._card = card_number
            self._state = nxt
            return self._state

    def enter_pin(self, pin: str) -> SessionState:
        """输密码。错了留在原状态（还有机会），最后一次错由银行作废、由机器吞卡。"""
        with self._lock:
            self._next(Action.ENTER_PIN)
            assert self._card is not None
            try:
                self._account_id = self._network.authenticate(self._card, pin)
            except WrongPinError as exc:
                self._log(TxKind.PIN_FAILURE, 0, TxStatus.DECLINED,
                          detail=f"remaining={exc.remaining}")
                if exc.remaining > 0:
                    self._state = self._next(Action.PIN_REJECTED)
                    raise
                self._retain_card("no attempts left")
                raise CardRetainedError("card retained: no attempts left") from exc
            self._state = SessionState.AUTHENTICATED
            return self._state

    def eject_card(self) -> SessionState:
        """退卡，会话结束。出钞过程中不允许——钱还在口上，卡不能先走。"""
        with self._lock:
            nxt = self._next(Action.EJECT)
            self._card = self._account_id = None
            self._state = nxt
            return self._state

    # ---- 第 2 关：取款 ----

    def withdraw(self, amount: int) -> Mapping[Note, int]:
        """取款：先留钞、再扣账、最后把钞票放到出钞口，返回这次送出的面额组合。

        顺序是这道题的题眼。留钞（把钞票从钞箱里抽出来）放在扣账之前，是因为钞箱是本地的、
        回滚干净；扣账放在交钞之前，是因为钞票一旦离开机器就再也收不回来。中间任何一步
        失败，回滚的都是本地那一半。
        """
        with self._lock:
            nxt = self._next(Action.WITHDRAW)
            assert self._account_id is not None
            if amount <= 0:
                raise InvalidAmountError(f"amount must be positive, got {amount}")
            plan = self._plan(amount)      # 三种"取不出"都在这里报错，此刻钞箱没动
            self._cassette.take(plan)      # 留钞：抽出来之后没人能再把它取走
            ref = self._new_ref()
            try:
                self._network.withdraw(self._account_id, amount, ref)
            except ATMError:
                self._cassette.load(plan)  # 远端一分没动，本地原样放回
                self._log(TxKind.WITHDRAWAL, amount, TxStatus.DECLINED, ref)
                raise
            self._tray.load(plan)
            self._pending = (ref, amount)
            self._log(TxKind.WITHDRAWAL, amount, TxStatus.OK, ref)
            self._state = nxt
            return MappingProxyType(dict(plan))

    def collect_cash(self) -> Mapping[Note, int]:
        """客户取走现金，会话回到菜单。"""
        with self._lock:
            nxt = self._next(Action.COLLECT_CASH)
            taken = dict(self._tray.counts())
            self._tray.take(taken)
            self._collected += sum(int(n) * c for n, c in taken.items())
            self._pending = None
            self._state = nxt
            return MappingProxyType(taken)

    def retract_uncollected(self) -> Mapping[Note, int]:
        """超时无人取走：钞票收进回收箱，并向银行发一笔冲正把钱退回账户。

        收进回收箱而不是放回钞箱，是真实机器的做法——被退回的钞票来路已经不确定，再吐给
        下一位客户就把一次纠纷变成两次。这也是"冲正"这条路径唯一的实现出口。
        """
        with self._lock:
            if self._state is not SessionState.DISPENSING or self._pending is None:
                raise IllegalActionError("nothing to retract")
            ref, amount = self._pending
            taken = dict(self._tray.counts())
            self._tray.take(taken)
            self._reject_bin.load(taken)
            assert self._account_id is not None
            self._network.reverse(self._account_id, amount, ref)
            self._log(TxKind.REVERSAL, amount, TxStatus.REVERSED, ref,
                      detail="uncollected cash retracted")
            self._pending = None
            self._state = self._next(Action.COLLECT_CASH)
            return MappingProxyType(taken)

    # ---- 第 3 关：查询与存款 ----

    def balance(self) -> int:
        """查余额。余额永远从网络问来，机器自己不缓存——它不是余额的权威。"""
        with self._lock:
            nxt = self._next(Action.BALANCE)
            assert self._account_id is not None
            current = self._network.balance(self._account_id)
            self._log(TxKind.BALANCE, 0, TxStatus.OK)
            self._state = nxt
            return current

    def deposit(self, notes: Mapping[Note, int]) -> int:
        """存款：钞票进存钞箱（未验真的钞票不能再吐给下一个人），账户入账，返回新余额。"""
        with self._lock:
            nxt = self._next(Action.DEPOSIT)
            assert self._account_id is not None
            amount = sum(int(n) * c for n, c in notes.items())
            if amount <= 0:
                raise InvalidAmountError("deposit must contain at least one note")
            ref = self._new_ref()
            self._deposit_bin.load(notes)
            self._deposited += amount
            new_balance = self._network.deposit(self._account_id, amount, ref)
            self._log(TxKind.DEPOSIT, amount, TxStatus.OK, ref)
            self._state = nxt
            return new_balance

    # ---- 内部 ----

    def _plan(self, amount: int) -> dict[Note, int]:
        """选钞，并把"取不出"分成三种可执行的理由。此刻钞箱一张钞票都没动。"""
        if amount % NOTE_STEP:
            raise AmountNotDispensableError(amount, DispenseFailure.NOT_REPRESENTABLE)
        plan = self._selector(amount, self._cassette.counts())
        if plan is None:
            raise AmountNotDispensableError(amount, DispenseFailure.NOT_IN_STOCK)
        if sum(plan.values()) > MAX_NOTES_PER_DISPENSE:
            raise AmountNotDispensableError(amount, DispenseFailure.TOO_MANY_NOTES)
        return plan

    def _retain_card(self, why: str) -> None:
        """吞卡：先写流水（那时卡号还在），再清空会话。"""
        self._log(TxKind.CARD_RETAINED, 0, TxStatus.DECLINED, detail=why)
        self._card = self._account_id = None
        self._state = self._next(Action.RETAIN_CARD)

    def _next(self, action: Action) -> SessionState:
        """查授权表。表里没有就是非法动作，报错里带上当前状态——客户屏幕和运维日志都靠它。"""
        nxt = TRANSITIONS.get((self._state, action))
        if nxt is None:
            raise IllegalActionError(f"cannot {action.value} while {self._state.value}")
        return nxt

    def _new_ref(self) -> str:
        self._seq += 1
        return f"{self._machine_id}-{self._seq:04d}"

    def _log(self, kind: TxKind, amount: int, status: TxStatus,
             ref: str | None = None, detail: str = "") -> JournalEntry:
        entry = JournalEntry(ref=ref or self._new_ref(), at=self._clock(), kind=kind,
                             status=status, amount=amount,
                             card_tail=(self._card or "****")[-4:], detail=detail)
        self._journal.append(entry)
        return entry


if __name__ == "__main__":
    bank = LocalBank("ICBC")
    bank.open_account("1001", balance=3000 * YUAN)
    bank.issue_card("ICBC-6222-0001", "1001", "1234")
    atm = ATM(bank, Cassette({Note.HUNDRED: 10, Note.FIFTY: 4, Note.TWENTY: 5, Note.TEN: 5}))
    atm.insert_card("ICBC-6222-0001")
    print("认证后:", atm.enter_pin("1234").value)
    print("余额:", atm.balance() / YUAN, "元")
    print("取 780 元:", {n.name: c for n, c in atm.withdraw(780 * YUAN).items()})
    atm.collect_cash()
    print("退卡后:", atm.eject_card().value, "; 对账:", atm.cash_up().balanced)
    for entry in atm.journal():
        print(f"  [journal] {entry.ref} {entry.kind.value} {entry.amount} {entry.status.value}")
