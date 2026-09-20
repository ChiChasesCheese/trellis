"""图书馆管理（Library Management）——练习骨架。公开 API 与 `solution.py` 完全一致，方法体留空。

做法：把每个 `raise NotImplementedError` 换成你自己的实现，然后在仓库根目录跑
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/library -q`。
内部表示随你换，但公开的类名、方法签名和只读属性（`queued_count`、`shelf_size`、`copy_count`）
要保留——测试只看这些。
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


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


class MediaKind(Enum):
    """介质类型。"""

    BOOK = "book"
    DVD = "dvd"
    MAGAZINE = "magazine"


class MemberType(Enum):
    """读者类型。"""

    STUDENT = "student"
    STAFF = "staff"
    PUBLIC = "public"


@dataclass(frozen=True, slots=True)
class Title:
    """一个书目：一部作品的著录记录，不是架上任何一本实体书。"""

    id: str
    name: str
    kind: MediaKind = MediaKind.BOOK
    creator: str = ""
    code: str = ""


@dataclass(frozen=True, slots=True)
class Copy:
    """一个馆藏副本：贴着条码的那一本实体书。"""

    barcode: str
    title_id: str


@dataclass(frozen=True, slots=True)
class Member:
    """一位读者。"""

    id: str
    name: str
    type: MemberType = MemberType.PUBLIC


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
    """按 (读者类型, 介质) 查政策，查不到就退回更粗的一档。"""

    default: LoanPolicy = LoanPolicy()
    overrides: Mapping[tuple[MemberType | None, MediaKind | None], LoanPolicy] = field(
        default_factory=dict)

    def resolve(self, member_type: MemberType, kind: MediaKind) -> LoanPolicy:
        """从最具体到最粗，第一个命中的就是答案。"""
        raise NotImplementedError


Clock = Callable[[], datetime]


@dataclass(slots=True)
class Loan:
    """一次外借。罚金按当前时刻算出来，不存字段。"""

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
        raise NotImplementedError

    def days_overdue(self, now: datetime) -> int:
        """逾期几天——不足一天按一天算，没逾期就是 0。"""
        raise NotImplementedError

    def fine_at(self, now: datetime, policy: LoanPolicy) -> int:
        """到此刻为止的罚金（分）。"""
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class HoldEntry:
    """取书架上的一条：这本副本给谁留着、留到什么时候。"""

    member_id: str
    title_id: str
    expires_at: datetime


class HoldRegistry:
    """按书目排的先来先到预约队列，以及取书架。两个容器都必须会缩。"""

    def __init__(self) -> None:
        raise NotImplementedError

    @property
    def queued_count(self) -> int:
        """当前还有多少条排队中的预约。"""
        raise NotImplementedError

    @property
    def shelf_size(self) -> int:
        """取书架上当前留着几本。"""
        raise NotImplementedError

    def queue_length(self, title_id: str) -> int:
        """这个书目排着几个人。"""
        raise NotImplementedError

    def position(self, member_id: str, title_id: str) -> int:
        """这位读者排在第几位（从 1 起），没排就是 0。"""
        raise NotImplementedError

    def queued_titles(self) -> tuple[str, ...]:
        """还有人排队的书目，一份快照。"""
        raise NotImplementedError

    def enqueue(self, member_id: str, title_id: str) -> int:
        """排到队尾，返回位次。"""
        raise NotImplementedError

    def pop(self, title_id: str) -> str | None:
        """取出队首；队列空了就把键删掉。"""
        raise NotImplementedError

    def cancel(self, member_id: str, title_id: str) -> bool:
        """把这位读者从队列里删掉。"""
        raise NotImplementedError

    def place_on_shelf(self, barcode: str, entry: HoldEntry) -> None:
        """把一本副本留到取书架上。"""
        raise NotImplementedError

    def shelved_for(self, member_id: str, title_id: str) -> str | None:
        """取书架上有没有给这位读者留的这个书目的副本。"""
        raise NotImplementedError

    def take_off_shelf(self, barcode: str) -> HoldEntry | None:
        """把一本副本从取书架上摘下来。"""
        raise NotImplementedError

    def shelved_barcodes(self) -> frozenset[str]:
        """取书架上所有条码的快照。"""
        raise NotImplementedError

    def entry_for(self, barcode: str) -> HoldEntry | None:
        """这本副本此刻被留给了谁。"""
        raise NotImplementedError

    def expire(self, now: datetime) -> tuple[str, ...]:
        """清掉过期的取书架条目，返回被释放的条码。"""
        raise NotImplementedError


class Catalog:
    """馆藏目录：书目、副本，以及"这个书目有哪些副本"。"""

    def __init__(self) -> None:
        raise NotImplementedError

    @property
    def copy_count(self) -> int:
        """全馆副本数。"""
        raise NotImplementedError

    def add_title(self, title: Title) -> None:
        """登记一个书目。"""
        raise NotImplementedError

    def add_copy(self, barcode: str, title_id: str) -> Copy:
        """给一个书目添一本实体副本。"""
        raise NotImplementedError

    def title(self, title_id: str) -> Title:
        """按 id 取书目。"""
        raise NotImplementedError

    def copy(self, barcode: str) -> Copy:
        """按条码取副本。"""
        raise NotImplementedError

    def barcodes_of(self, title_id: str) -> tuple[str, ...]:
        """这个书目的全部副本条码，一份快照。"""
        raise NotImplementedError

    def search(self, query: str) -> tuple[Title, ...]:
        """按书名或作者做子串匹配，按 id 排序。刻意保持朴素。"""
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class ReturnReceipt:
    """一次还书发生了什么。"""

    barcode: str
    days_overdue: int
    fine: int
    held_for: str | None


class Library:
    """流通台：借、还、续借、预约，以及"谁拿到哪一本"的唯一裁决者。"""

    def __init__(self, catalog: Catalog, clock: Clock,
                 policies: PolicyTable = PolicyTable()) -> None:
        raise NotImplementedError

    def add_member(self, member: Member) -> None:
        """登记一位读者。"""
        raise NotImplementedError

    @property
    def queued_count(self) -> int:
        """全馆排队中的预约条数。"""
        raise NotImplementedError

    @property
    def shelf_size(self) -> int:
        """取书架上留着的副本数。"""
        raise NotImplementedError

    def queue_position(self, member_id: str, title_id: str) -> int:
        """这位读者在这个书目的队列里排第几。"""
        raise NotImplementedError

    def loans_of(self, member_id: str) -> tuple[Loan, ...]:
        """这位读者名下未归还的借阅，一份快照。"""
        raise NotImplementedError

    def availability(self, title_id: str) -> int:
        """这个书目此刻有几本可以直接借走。"""
        raise NotImplementedError

    def fines_owed(self, member_id: str) -> int:
        """这位读者此刻欠的罚金（分）。"""
        raise NotImplementedError

    def borrow(self, member_id: str, title_id: str) -> Loan:
        """借书。"""
        raise NotImplementedError

    def return_copy(self, barcode: str) -> ReturnReceipt:
        """还书。"""
        raise NotImplementedError

    def renew(self, loan_id: str) -> Loan:
        """续借。"""
        raise NotImplementedError

    def place_hold(self, member_id: str, title_id: str) -> int:
        """预约。"""
        raise NotImplementedError

    def cancel_hold(self, member_id: str, title_id: str) -> bool:
        """取消预约。"""
        raise NotImplementedError
