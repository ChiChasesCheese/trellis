"""图书馆管理（Library Management）——书目与副本的区分、借还与续借、预约队列、逾期罚金的参考实现。

核心思路：**书目（Title）不是副本（Copy）**——搜索挂在书目上，借还挂在副本上，预约挂在书目上，
这三句话决定了全部数据结构。预约是一条按书目排的先来先到队列；一本书还回来时，队首的人被摘下来，
副本进"取书架"（hold shelf）并带一个到期时刻，逾期不取就下架、这个人**退出队列**。谁能拿到哪一本，
只由 `_sweep` 一个方法决定——归还、过期、新进书、取消预约都只改事实再调它，没有定时器也没有后台
线程。借阅限额、借期、续借次数、罚金费率、留架天数全部来自一张按 (读者类型, 介质) 查的政策表，
加一种读者或一种介质只是加一行。
"""

from __future__ import annotations

import itertools
import math
import threading
from collections import deque
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

# --------------------------------------------------------------------------
# 失败路径。

class LibraryError(Exception):
    """本设计里所有失败路径的公共基类。"""


class UnknownEntityError(LibraryError):
    """书目、副本、读者或借阅记录不存在。"""


class NoCopyAvailableError(LibraryError):
    """这个书目此刻没有可外借的副本。"""


class LoanLimitReachedError(LibraryError):
    """这位读者名下的在借数已达上限。"""


class RenewalRefusedError(LibraryError):
    """这次续借不被允许：有人在排队，或续借次数用尽。"""


class HoldRefusedError(LibraryError):
    """这次预约不被允许：有书可借、或者已经预约过、或者自己正借着。"""


# --------------------------------------------------------------------------
# 书目与副本——这道题的第一条分界线。

class MediaKind(Enum):
    """介质类型。它只影响政策（借期、罚金、留架天数），不影响任何流程。"""

    BOOK = "book"
    DVD = "dvd"
    MAGAZINE = "magazine"


class MemberType(Enum):
    """读者类型。同样只影响政策。"""

    STUDENT = "student"
    STAFF = "staff"
    PUBLIC = "public"


@dataclass(frozen=True, slots=True)
class Title:
    """一个**书目**：一部作品的著录记录，不是架上任何一本实体书。

    `creator` 按介质换角色（图书的作者、DVD 的导演、期刊的出版者），`code` 同理
    （ISBN / 碟片编号 / 刊期号）。这就是为什么不需要 `Book`、`DVD`、`Magazine` 三个子类：
    它们的差别是**字段叫什么**和**按什么政策借**，不是行为不同。一本期刊的每一期是一个独立书目，
    名字相同、`code` 不同。
    """

    id: str
    name: str
    kind: MediaKind = MediaKind.BOOK
    creator: str = ""
    code: str = ""


@dataclass(frozen=True, slots=True)
class Copy:
    """一个**馆藏副本**：贴着条码的那一本实体书。真正被借走、被还回、被放上取书架的是它。

    它凭什么值得是一个独立的类（而不是给书目加一个 `count`）？凭**身份**：同一个书目的两本
    副本一旦有一本丢了、有一本被留给了别人，它们就不再可互换，而罚金、丢失、注销都记在条码上。
    """

    barcode: str
    title_id: str


@dataclass(frozen=True, slots=True)
class Member:
    """一位读者。借阅权限来自 `type`，不来自这个对象上的任何字段。"""

    id: str
    name: str
    type: MemberType = MemberType.PUBLIC


# --------------------------------------------------------------------------
# 政策表：借期、限额、罚金、留架天数。加一种读者或一种介质＝加一行。

@dataclass(frozen=True, slots=True)
class LoanPolicy:
    """一行政策：借几本、借多少天、能续几次、逾期每天罚多少分、预约留架几天。"""

    max_loans: int = 5
    loan_days: int = 14
    max_renewals: int = 2
    fine_per_day: int = 50
    hold_days: int = 3


@dataclass(frozen=True, slots=True)
class PolicyTable:
    """按 (读者类型, 介质) 查政策，查不到就退回更粗的一档，最后退回默认。

    政策是**数据**而不是代码：加一条"教师借 DVD 可以借 7 天"只是往 `overrides` 里加一个键，
    借还流程一行不动。写成 `if member.type is STAFF` 的分支才是真正贵的那种写法。
    """

    default: LoanPolicy = LoanPolicy()
    overrides: Mapping[tuple[MemberType | None, MediaKind | None], LoanPolicy] = field(
        default_factory=dict)

    def resolve(self, member_type: MemberType, kind: MediaKind) -> LoanPolicy:
        """从最具体到最粗，第一个命中的就是答案。"""
        for key in ((member_type, kind), (member_type, None), (None, kind)):
            found = self.overrides.get(key)
            if found is not None:
                return found
        return self.default


# --------------------------------------------------------------------------
# 借阅记录与罚金。

Clock = Callable[[], datetime]


@dataclass(slots=True)
class Loan:
    """一次外借：哪本副本、借给谁、什么时候到期、续过几次、还了没有。

    罚金不是一个存下来的数字，而是**按当前时刻算出来的**：读者还没还书的时候，柜台也要答得出
    "现在欠多少"。存一个 `fine` 字段就只能在还书那一刻更新，之后就过期了。
    """

    id: str
    barcode: str
    title_id: str
    member_id: str
    out_at: datetime
    due_at: datetime
    renewals: int = 0
    returned_at: datetime | None = None

    @property
    def open(self) -> bool:
        """这笔借阅还没还。"""
        return self.returned_at is None

    def days_overdue(self, now: datetime) -> int:
        """逾期几天——不足一天按一天算，没逾期就是 0。"""
        moment = self.returned_at or now
        if moment <= self.due_at:
            return 0
        return max(1, math.ceil((moment - self.due_at).total_seconds() / 86400))

    def fine_at(self, now: datetime, policy: LoanPolicy) -> int:
        """到此刻为止的罚金（分）。"""
        return self.days_overdue(now) * policy.fine_per_day


# --------------------------------------------------------------------------
# HoldRegistry：预约队列 + 取书架。两个都必须会缩。

@dataclass(frozen=True, slots=True)
class HoldEntry:
    """取书架上的一条：这本副本给谁留着、留到什么时候。"""

    member_id: str
    title_id: str
    expires_at: datetime


class HoldRegistry:
    """按书目排的先来先到预约队列，以及"已经留出来等人来取"的取书架。

    不变量：一位读者对同一个书目最多排一次队；队列空了立刻删键，不留空壳；取书架上的条目
    一旦过期就必须被清掉——**过期的预约要离开队列**，否则一本书会被一个再也不来的人永远占着。
    """

    def __init__(self) -> None:
        self._queues: dict[str, deque[str]] = {}
        self._shelf: dict[str, HoldEntry] = {}

    @property
    def queued_count(self) -> int:
        """当前还有多少条排队中的预约——只读计数，验证"队空即删"真的生效。"""
        return sum(len(queue) for queue in self._queues.values())

    @property
    def shelf_size(self) -> int:
        """取书架上当前留着几本。"""
        return len(self._shelf)

    def queue_length(self, title_id: str) -> int:
        """这个书目排着几个人。"""
        return len(self._queues.get(title_id, ()))

    def position(self, member_id: str, title_id: str) -> int:
        """这位读者排在第几位（从 1 起），没排就是 0。"""
        queue = self._queues.get(title_id, deque())
        return queue.index(member_id) + 1 if member_id in queue else 0

    def queued_titles(self) -> tuple[str, ...]:
        """还有人排队的书目，一份快照——遍历时要删键，不能直接迭代内部字典。"""
        return tuple(self._queues)

    def enqueue(self, member_id: str, title_id: str) -> int:
        """排到队尾，返回位次。已经在队里就抛 `HoldRefusedError`。"""
        queue = self._queues.setdefault(title_id, deque())
        if member_id in queue:
            raise HoldRefusedError(f"{member_id} already holds {title_id}")
        queue.append(member_id)
        return len(queue)

    def pop(self, title_id: str) -> str | None:
        """取出队首；队列空了就把键删掉。"""
        queue = self._queues.get(title_id)
        if not queue:
            return None
        member_id = queue.popleft()
        if not queue:
            del self._queues[title_id]
        return member_id

    def cancel(self, member_id: str, title_id: str) -> bool:
        """读者主动取消排队，或者他已经用别的途径借到了。队列空了同样删键。"""
        queue = self._queues.get(title_id)
        if not queue or member_id not in queue:
            return False
        queue.remove(member_id)
        if not queue:
            del self._queues[title_id]
        return True

    def place_on_shelf(self, barcode: str, entry: HoldEntry) -> None:
        """把一本副本留到取书架上。"""
        self._shelf[barcode] = entry

    def shelved_for(self, member_id: str, title_id: str) -> str | None:
        """取书架上有没有给这位读者留的这个书目的副本，有就给条码。"""
        return next((barcode for barcode, entry in self._shelf.items()
                     if entry.member_id == member_id and entry.title_id == title_id), None)

    def take_off_shelf(self, barcode: str) -> HoldEntry | None:
        """把一本副本从取书架上摘下来（被取走，或者被注销）。"""
        return self._shelf.pop(barcode, None)

    def shelved_barcodes(self) -> frozenset[str]:
        """取书架上所有条码的快照。"""
        return frozenset(self._shelf)

    def entry_for(self, barcode: str) -> HoldEntry | None:
        """这本副本此刻被留给了谁。"""
        return self._shelf.get(barcode)

    def expire(self, now: datetime) -> tuple[str, ...]:
        """清掉过期的取书架条目，返回被释放的条码。

        这是取书架唯一的收缩途径。不清的后果很具体：一位读者预约了书、通知也收到了，却再也没来，
        这本副本就永远停在"给他留着"的状态——馆里有书，谁也借不到。**过期即离队**：他不会被放回
        队尾，要书就重新排（要的是"再表达一次意愿"，而不是无限顺延）。
        """
        stale = [barcode for barcode, entry in self._shelf.items() if entry.expires_at <= now]
        for barcode in stale:
            del self._shelf[barcode]
        return tuple(stale)


# --------------------------------------------------------------------------
# Catalog：书目与副本的登记簿，以及一个刻意保持朴素的检索。

class Catalog:
    """馆藏目录：书目、副本，以及"这个书目有哪些副本"。

    不变量：每个副本的 `title_id` 都指向一个存在的书目；副本条码全局唯一。
    """

    def __init__(self) -> None:
        self._titles: dict[str, Title] = {}
        self._copies: dict[str, Copy] = {}
        self._by_title: dict[str, list[str]] = {}

    @property
    def copy_count(self) -> int:
        """全馆副本数。"""
        return len(self._copies)

    def add_title(self, title: Title) -> None:
        """登记一个书目。"""
        self._titles[title.id] = title

    def add_copy(self, barcode: str, title_id: str) -> Copy:
        """给一个书目添一本实体副本。"""
        if title_id not in self._titles:
            raise UnknownEntityError(f"unknown title {title_id!r}")
        copy = Copy(barcode, title_id)
        self._copies[barcode] = copy
        self._by_title.setdefault(title_id, []).append(barcode)
        return copy

    def title(self, title_id: str) -> Title:
        """按 id 取书目。"""
        found = self._titles.get(title_id)
        if found is None:
            raise UnknownEntityError(f"unknown title {title_id!r}")
        return found

    def copy(self, barcode: str) -> Copy:
        """按条码取副本。"""
        found = self._copies.get(barcode)
        if found is None:
            raise UnknownEntityError(f"unknown copy {barcode!r}")
        return found

    def barcodes_of(self, title_id: str) -> tuple[str, ...]:
        """这个书目的全部副本条码，一份快照。"""
        return tuple(self._by_title.get(title_id, ()))

    def search(self, query: str) -> tuple[Title, ...]:
        """按书名或作者做**子串匹配**，按 id 排序。

        刻意保持朴素：这道题考的是借还与预约的建模，检索是送分项。真要上规模，答案是倒排索引
        或者外挂一个搜索引擎，而不是在这里摆一组 `SearchByAuthorStrategy` 子类——那是给一个
        `if` 套四层类。
        """
        needle = query.lower()
        found = [t for t in self._titles.values()
                 if needle in t.name.lower() or needle in t.creator.lower()]
        return tuple(sorted(found, key=lambda t: t.id))


# --------------------------------------------------------------------------
# 还书回执。

@dataclass(frozen=True, slots=True)
class ReturnReceipt:
    """一次还书发生了什么：逾期几天、罚了多少、这本书接着留给了谁。"""

    barcode: str
    days_overdue: int
    fine: int
    held_for: str | None


# --------------------------------------------------------------------------
# Library：流通台。借、还、续借、预约，以及"谁拿到哪一本"的唯一裁决者。

class Library:
    """流通台：把目录、预约队列、借阅记录和政策表绑在一起。

    锁纪律：一把锁保护全部可变状态（借阅表、队列、取书架），所有公开方法都在锁内完成一次
    完整的复合操作。这道题没有第二把锁，所以不存在锁序问题——**该说清楚的是为什么不需要**，
    而不是为了显得高级去拆锁。
    """

    def __init__(self, catalog: Catalog, clock: Clock,
                 policies: PolicyTable = PolicyTable()) -> None:
        self._catalog = catalog
        self._clock = clock
        self._policies = policies
        self._holds = HoldRegistry()
        self._members: dict[str, Member] = {}
        self._loans: dict[str, Loan] = {}
        self._out: dict[str, str] = {}  # 条码 → 未归还的借阅 id
        self._fines: dict[str, int] = {}  # 读者 → 已结清前的累计罚金（分）
        self._lock = threading.Lock()
        self._ids = (f"L{n}" for n in itertools.count(1))

    # ---- 读者与只读视图 --------------------------------------------------

    def add_member(self, member: Member) -> None:
        """登记一位读者。"""
        with self._lock:
            self._members[member.id] = member

    def _member(self, member_id: str) -> Member:
        found = self._members.get(member_id)
        if found is None:
            raise UnknownEntityError(f"unknown member {member_id!r}")
        return found

    @property
    def queued_count(self) -> int:
        """全馆排队中的预约条数（按当前时刻结算过过期条目）。"""
        with self._lock:
            self._sweep(self._clock())
            return self._holds.queued_count

    @property
    def shelf_size(self) -> int:
        """取书架上留着的副本数。

        它也会先跑一次 `_sweep`：惰性过期的代价就是"读"也要把世界推到当前时刻，否则这个数字
        会把一条早该下架的条目报给调用方。宁可让只读属性做这一点工作，也不要引入定时器。
        """
        with self._lock:
            self._sweep(self._clock())
            return self._holds.shelf_size

    def queue_position(self, member_id: str, title_id: str) -> int:
        """这位读者在这个书目的队列里排第几（从 1 起，0 表示没排）。"""
        with self._lock:
            self._sweep(self._clock())
            return self._holds.position(member_id, title_id)

    def loans_of(self, member_id: str) -> tuple[Loan, ...]:
        """这位读者名下未归还的借阅，一份快照。"""
        with self._lock:
            return tuple(l for l in self._loans.values()
                         if l.member_id == member_id and l.open)

    def availability(self, title_id: str) -> int:
        """这个书目此刻有几本可以直接借走（既没外借，也没被留在取书架上）。"""
        with self._lock:
            self._sweep(self._clock())
            return len(self._free_barcodes(title_id))

    def fines_owed(self, member_id: str) -> int:
        """这位读者此刻欠的罚金（分）：已结算的 + 手上逾期书**正在**产生的。"""
        now = self._clock()
        with self._lock:
            accruing = sum(loan.fine_at(now, self._policy_for(loan))
                           for loan in self._loans.values()
                           if loan.member_id == member_id and loan.open)
            return self._fines.get(member_id, 0) + accruing

    # ---- 内部：政策、空闲副本、以及唯一的分配规则 ------------------------

    def _policy_for(self, loan: Loan) -> LoanPolicy:
        return self._policies.resolve(self._member(loan.member_id).type,
                                      self._catalog.title(loan.title_id).kind)

    def _free_barcodes(self, title_id: str) -> tuple[str, ...]:
        """既没被借走、也没被留在取书架上的副本。调用方必须已经持有锁。"""
        shelved = self._holds.shelved_barcodes()
        return tuple(b for b in self._catalog.barcodes_of(title_id)
                     if b not in self._out and b not in shelved)

    def _sweep(self, now: datetime) -> None:
        """惰性清理 + 分配：先让过期的取书架条目下架，再把空闲副本按队列依次留给下一个人。

        **全馆"谁拿到哪一本"只在这里决定。**还书、过期、新进书、取消预约都只是改事实，改完调它。
        这样做的直接好处是不需要定时器、不需要后台线程：没有人查询时，过期与否无人关心；
        任何一次查询或操作都会先把世界推到当前时刻的正确状态。
        """
        self._holds.expire(now)
        for title_id in self._holds.queued_titles():
            while self._holds.queue_length(title_id):
                free = self._free_barcodes(title_id)
                if not free:
                    break
                member_id = self._holds.pop(title_id)
                if member_id is None:
                    break
                policy = self._policies.resolve(self._member(member_id).type,
                                                self._catalog.title(title_id).kind)
                self._holds.place_on_shelf(free[0], HoldEntry(
                    member_id, title_id, now + timedelta(days=policy.hold_days)))

    # ---- 借、还、续借 ----------------------------------------------------

    def borrow(self, member_id: str, title_id: str) -> Loan:
        """借书：优先拿取书架上为你留的那一本，否则拿一本空闲副本。

        借到之后要把自己从这个书目的队列里删掉——不然一个人既借着书又排着队，下一本还回来
        还会再留给他一次。**队列必须在每一条离队的路径上都缩。**
        """
        now = self._clock()
        with self._lock:
            self._sweep(now)
            member = self._member(member_id)
            title = self._catalog.title(title_id)
            policy = self._policies.resolve(member.type, title.kind)
            open_loans = sum(1 for l in self._loans.values()
                             if l.member_id == member_id and l.open)
            if open_loans >= policy.max_loans:
                raise LoanLimitReachedError(
                    f"{member_id} already has {open_loans} item(s), limit {policy.max_loans}")
            barcode = self._holds.shelved_for(member_id, title_id)
            if barcode is not None:
                self._holds.take_off_shelf(barcode)
            else:
                free = self._free_barcodes(title_id)
                if not free:
                    raise NoCopyAvailableError(f"no copy of {title_id!r} is on the shelf")
                barcode = free[0]
            self._holds.cancel(member_id, title_id)
            loan = Loan(id=next(self._ids), barcode=barcode, title_id=title_id,
                        member_id=member_id, out_at=now,
                        due_at=now + timedelta(days=policy.loan_days))
            self._loans[loan.id] = loan
            self._out[barcode] = loan.id
            return loan

    def return_copy(self, barcode: str) -> ReturnReceipt:
        """还书：结算罚金，副本回到馆里，再由 `_sweep` 决定它接着归谁。"""
        now = self._clock()
        with self._lock:
            loan_id = self._out.get(barcode)
            if loan_id is None:
                raise UnknownEntityError(f"copy {barcode!r} is not on loan")
            loan = self._loans[loan_id]
            loan.returned_at = now
            fine = loan.fine_at(now, self._policy_for(loan))
            days = loan.days_overdue(now)
            self._fines[loan.member_id] = self._fines.get(loan.member_id, 0) + fine
            del self._out[barcode]
            self._sweep(now)
            entry = self._holds.entry_for(barcode)
            return ReturnReceipt(barcode, days, fine, entry.member_id if entry else None)

    def renew(self, loan_id: str) -> Loan:
        """续借：有人在排队就拒绝，续借次数用尽也拒绝。新的到期日从今天起算。

        "有人排队就不给续"是这道题里唯一一条真正的业务规则冲突，也是面试官最爱追的点：
        续借是对**已经在手上**的读者的方便，排队是对**还没拿到**的读者的承诺，后者优先。
        """
        now = self._clock()
        with self._lock:
            self._sweep(now)
            loan = self._loans.get(loan_id)
            if loan is None or not loan.open:
                raise UnknownEntityError(f"unknown open loan {loan_id!r}")
            policy = self._policy_for(loan)
            if self._holds.queue_length(loan.title_id):
                raise RenewalRefusedError(
                    f"{loan.title_id} has {self._holds.queue_length(loan.title_id)} hold(s)")
            if loan.renewals >= policy.max_renewals:
                raise RenewalRefusedError(
                    f"loan {loan_id} already renewed {loan.renewals} time(s)")
            loan.renewals += 1
            loan.due_at = max(loan.due_at, now + timedelta(days=policy.loan_days))
            return loan

    # ---- 预约 ------------------------------------------------------------

    def place_hold(self, member_id: str, title_id: str) -> int:
        """预约：有书可借时拒绝（直接去借就是了），否则排到队尾并返回位次。"""
        now = self._clock()
        with self._lock:
            self._sweep(now)
            self._member(member_id)
            self._catalog.title(title_id)
            if self._free_barcodes(title_id):
                raise HoldRefusedError(f"{title_id} has copies on the shelf; just borrow one")
            if self._holds.shelved_for(member_id, title_id) is not None:
                raise HoldRefusedError(f"a copy of {title_id} is already waiting for {member_id}")
            if any(l.member_id == member_id and l.title_id == title_id and l.open
                   for l in self._loans.values()):
                raise HoldRefusedError(f"{member_id} already has a copy of {title_id}")
            return self._holds.enqueue(member_id, title_id)

    def cancel_hold(self, member_id: str, title_id: str) -> bool:
        """取消预约。已经被留到取书架上的那一本也一并释放，交给下一个人。"""
        now = self._clock()
        with self._lock:
            barcode = self._holds.shelved_for(member_id, title_id)
            if barcode is not None:
                self._holds.take_off_shelf(barcode)
            cancelled = self._holds.cancel(member_id, title_id)
            self._sweep(now)
            return cancelled or barcode is not None


if __name__ == "__main__":
    from datetime import UTC

    now = datetime(2026, 9, 1, 10, 0, tzinfo=UTC)
    catalog = Catalog()
    catalog.add_title(Title("T1", "深入理解计算机系统", creator="Bryant", code="9787111544937"))
    catalog.add_copy("B001", "T1")
    catalog.add_title(Title("T2", "沙丘", MediaKind.DVD, creator="Villeneuve"))
    catalog.add_copy("D001", "T2")

    policies = PolicyTable(LoanPolicy(),
                           {(MemberType.STUDENT, None): LoanPolicy(max_loans=2, loan_days=7),
                            (None, MediaKind.DVD): LoanPolicy(loan_days=2, fine_per_day=200,
                                                              hold_days=1)})
    library = Library(catalog, clock=lambda: now, policies=policies)
    library.add_member(Member("M1", "chi", MemberType.STUDENT))
    library.add_member(Member("M2", "lee", MemberType.STAFF))

    loan = library.borrow("M1", "T1")
    print(f"{loan.id} {loan.barcode} 到期 {loan.due_at:%m-%d}，T1 可借 {library.availability('T1')}")
    print("M2 预约 T1，位次", library.place_hold("M2", "T1"), "；续借被拒：", end=" ")
    try:
        library.renew(loan.id)
    except RenewalRefusedError as error:
        print(error)

    now = datetime(2026, 9, 12, 10, 0, tzinfo=UTC)
    receipt = library.return_copy("B001")
    print(f"还书：逾期 {receipt.days_overdue} 天、罚 {receipt.fine} 分、留给 {receipt.held_for}，"
          f"取书架 {library.shelf_size} 本，队列 {library.queued_count} 条")

    now = datetime(2026, 9, 20, 10, 0, tzinfo=UTC)
    print(f"M2 迟迟不来，过期之后：取书架 {library.shelf_size} 本，"
          f"T1 可借 {library.availability('T1')}，M2 欠款 {library.fines_owed('M2')} 分")
