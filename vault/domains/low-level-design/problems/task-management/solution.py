"""任务看板（Trello / Jira）：看板-列-卡片，工作流状态转移，指派/标签/截止日期，活动记录。

设计要点：一列（`BoardList`）本身就是工作流里的一个状态节点，`Workflow` 只管"这一步转移合不
合法"这一件事，不知道卡片、不知道索引；`CardStore` 只管卡片的存储与三类索引（按列排序、按
指派人、按未归档的到期日）的维护，不知道工作流规则；`TaskBoardService` 编排两者，是唯一同时
知道"这次移动合不合法"和"移动之后索引该怎么变"的地方。卡片在列内的顺序用可排序的浮点"秩"
（rank）维护——挪一张卡只改它自己的一个数字，不用移动其它卡；秩间距耗尽时只重排那一列，不碰
其它列。归档一张卡会把它从三类索引里同时摘除，索引因此不会随着历史卡片数量无限增长。
"""

from __future__ import annotations

import itertools
import threading
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from enum import Enum
from typing import Callable

Clock = Callable[[], datetime]


def utc_now() -> datetime:
    """默认时钟。"""
    return datetime.now(timezone.utc)


# --------------------------------------------------------------------------
# 失败路径


class TaskBoardError(Exception):
    """本组件所有失败路径的公共基类。"""


class UnknownBoardError(TaskBoardError, KeyError):
    """看板 id 不存在。"""


class UnknownListError(TaskBoardError, KeyError):
    """列 id 在这块看板上不存在。"""


class UnknownCardError(TaskBoardError, KeyError):
    """卡片 id，或卡片上的某条清单项 id，不存在。"""


class DuplicateListError(TaskBoardError):
    """同一个列 id 在同一块看板上被重复创建。"""


class IllegalTransitionError(TaskBoardError):
    """工作流里没有这条边：从当前列不能直接转移到目标列。"""


class CardArchivedError(TaskBoardError):
    """卡片已归档，不能再移动、指派或改其它字段。"""


# --------------------------------------------------------------------------
# 秩：卡片在列内的顺序，位置用一个可排序的浮点数表达，不用整数下标。


class RankExhaustedError(Exception):
    """相邻两张卡的秩已经挨得太近，浮点精度分不出中点了——调用方应当重排整列。"""


def rank_between(prev_rank: float | None, next_rank: float | None) -> float:
    """算一个夹在 `prev_rank` 和 `next_rank` 之间的秩；两端各自可以是 `None`（列首/列尾）。

    这是"位置怎么存"这道题的核心：整数下标每插入一张卡都要把后面所有卡的下标加一，一次移动是
    O(n)；这里插入或移动只写一张卡自己的浮点数，其它卡一行都不碰，是 O(1)。代价是浮点数的
    精度有限——反复在同一条缝里插入，早晚会碰到两个相邻的秩已经无法再取中点，那时候
    `RankExhaustedError` 提醒调用方对这一列做一次性的整列重排（`CardStore._rebalance`），这个
    重排本身是 O(列长)，但只在这条缝真的被塞满时才发生，不是每次插入都付出的代价。
    """
    if prev_rank is None and next_rank is None:
        return 0.0
    if prev_rank is None:
        return next_rank - 1.0
    if next_rank is None:
        return prev_rank + 1.0
    mid = prev_rank + (next_rank - prev_rank) / 2
    if mid <= prev_rank or mid >= next_rank:
        raise RankExhaustedError("rank gap exhausted")
    return mid


# --------------------------------------------------------------------------
# 活动记录：一份不可变、追加写的事件日志，是"这张卡上发生过什么"的唯一真相来源。


class ActivityType(Enum):
    """一条活动事件的种类；每一种都对应卡片生命周期里的一次可观察动作。"""

    CREATED = "created"
    MOVED = "moved"
    ASSIGNED = "assigned"
    UNASSIGNED = "unassigned"
    LABELED = "labeled"
    UNLABELED = "unlabeled"
    DUE_DATE_SET = "due_date_set"
    DUE_DATE_CLEARED = "due_date_cleared"
    CHECKLIST_ITEM_ADDED = "checklist_item_added"
    CHECKLIST_ITEM_TOGGLED = "checklist_item_toggled"
    ARCHIVED = "archived"


@dataclass(frozen=True, slots=True)
class ActivityEvent:
    """一条活动事件：发生了什么、谁做的、什么时候——一个冻结快照，不是可以回头改写的一行。"""

    event_id: str
    card_id: str
    type: ActivityType
    actor: str
    at: datetime
    detail: str = ""


@dataclass(slots=True)
class ChecklistItem:
    """卡片上清单的一项：文字与完成状态。只在 `Card` 内部被修改，不参与任何索引。"""

    item_id: str
    text: str
    done: bool = False


# --------------------------------------------------------------------------
# 工作流：一块看板自己的状态转移规则。列本身就是状态节点。


class Workflow:
    """看板的工作流：哪些列之间允许直接互转。这是 Jira 风格的图，不是硬编码的三段
    to-do/doing/done——每块看板可以有自己的一套状态和边，甚至允许"打回去"这种反向边。

    这里没有为每个状态各写一个子类去表达"这个状态下能做什么"（教科书里状态模式的常见写法）：
    三个状态之间唯一有实质内容的差异是"允许转到哪些状态"，这是纯数据，不是行为——状态本身不
    会让"移动"这个操作的代码逻辑发生分支。行为差异才值得建类层级；这里只有一张表值得维护。
    """

    def __init__(self, states: Iterable[str] = ()) -> None:
        self._edges: dict[str, set[str]] = {s: set() for s in states}

    def add_state(self, state_id: str) -> None:
        self._edges.setdefault(state_id, set())

    def allow(self, from_state: str, to_state: str) -> None:
        if from_state not in self._edges or to_state not in self._edges:
            raise UnknownListError(f"unknown workflow state {from_state!r} or {to_state!r}")
        self._edges[from_state].add(to_state)

    def can_transition(self, from_state: str, to_state: str) -> bool:
        return from_state == to_state or to_state in self._edges.get(from_state, ())

    def states(self) -> frozenset[str]:
        return frozenset(self._edges)


@dataclass(slots=True)
class BoardList:
    """一块看板上的一列：id 与显示名字。列的先后顺序由 `Board` 维护，不是列自己的事。"""

    id: str
    name: str


class Board:
    """一块看板：列的集合与它们的先后顺序，以及这块看板自己的 `Workflow`。不持有卡片——卡片
    的存储和索引是 `CardStore` 的职责，两者由 `TaskBoardService` 编排到一起。
    """

    def __init__(self, board_id: str, name: str) -> None:
        self.id = board_id
        self.name = name
        self.workflow = Workflow()
        self._lists: dict[str, BoardList] = {}
        self._order: list[str] = []

    def add_list(self, list_id: str, name: str) -> BoardList:
        if list_id in self._lists:
            raise DuplicateListError(f"list {list_id!r} already exists on board {self.id!r}")
        lst = BoardList(list_id, name)
        self._lists[list_id] = lst
        self._order.append(list_id)
        self.workflow.add_state(list_id)
        return lst

    def has_list(self, list_id: str) -> bool:
        return list_id in self._lists

    def list_name(self, list_id: str) -> str:
        try:
            return self._lists[list_id].name
        except KeyError:
            raise UnknownListError(list_id) from None

    def list_ids(self) -> tuple[str, ...]:
        """列的显示顺序快照——调用方不能通过它改写看板的列序。"""
        return tuple(self._order)


# --------------------------------------------------------------------------
# 卡片：数据持有者。列成员、指派、到期日的写入只应经过 `CardStore`，否则三类索引会和卡片
# 自身的字段脱节——这条纪律和餐厅题里"两把锁只有一个方向"一样，靠约定维持、写进文档字符串。


class Card:
    """看板上的一张卡片。清单（checklist）的增删不影响列成员、指派、到期日何何一项索引，因此
    stage 4 加清单这个动作完全不碰 `CardStore` 的任何一行代码——这正是这道题"加一个子功能不动
    移动逻辑"这条验收标准的字面体现。
    """

    def __init__(self, card_id: str, board_id: str, list_id: str, title: str, rank: float) -> None:
        self.id = card_id
        self.board_id = board_id
        self.title = title
        self._list_id = list_id
        self._rank = rank
        self._assignee: str | None = None
        self._labels: set[str] = set()
        self._due_date: date | None = None
        self._archived = False
        self._checklist: dict[str, ChecklistItem] = {}
        self._next_item = itertools.count(1)

    @property
    def list_id(self) -> str:
        return self._list_id

    @property
    def rank(self) -> float:
        return self._rank

    @property
    def assignee(self) -> str | None:
        return self._assignee

    @property
    def labels(self) -> frozenset[str]:
        return frozenset(self._labels)

    @property
    def due_date(self) -> date | None:
        return self._due_date

    @property
    def archived(self) -> bool:
        return self._archived

    @property
    def checklist(self) -> tuple[ChecklistItem, ...]:
        return tuple(self._checklist.values())

    def is_overdue(self, today: date) -> bool:
        return not self._archived and self._due_date is not None and self._due_date < today

    # ---- 只应由 CardStore 调用：写入的同时它也在维护索引 ----

    def _place(self, list_id: str, rank: float) -> None:
        self._list_id, self._rank = list_id, rank

    def _assign(self, user_id: str | None) -> None:
        self._assignee = user_id

    def _set_due(self, due: date | None) -> None:
        self._due_date = due

    def _archive(self) -> None:
        self._archived = True

    # ---- 标签与清单：不进任何索引，谁都能直接调用 ----

    def add_label(self, label: str) -> None:
        self._labels.add(label)

    def remove_label(self, label: str) -> None:
        self._labels.discard(label)

    def add_checklist_item(self, text: str) -> ChecklistItem:
        item = ChecklistItem(f"chk-{next(self._next_item)}", text)
        self._checklist[item.item_id] = item
        return item

    def toggle_checklist_item(self, item_id: str) -> ChecklistItem:
        item = self._checklist.get(item_id)
        if item is None:
            raise UnknownCardError(f"unknown checklist item {item_id!r} on card {self.id!r}")
        item.done = not item.done
        return item


# --------------------------------------------------------------------------
# CardStore：卡片的存储与三类索引。不知道工作流规则，只知道"把卡片放进哪一列"。


class CardStore:
    """卡片仓库：按列的秩排序索引（分组查询）、按指派人的索引（跨看板查询）、按到期日的索引
    （只收未归档且设了到期日的卡，逾期查询因此只扫『真的可能逾期』的这一小撮卡，不扫全部卡）。
    """

    def __init__(self) -> None:
        self._cards: dict[str, Card] = {}
        self._order: dict[str, list[str]] = {}
        self._assignee_index: dict[str, set[str]] = {}
        self._due_index: dict[str, date] = {}
        self._lock = threading.Lock()
        self._next_id = itertools.count(1)

    def _require(self, card_id: str) -> Card:
        try:
            return self._cards[card_id]
        except KeyError:
            raise UnknownCardError(card_id) from None

    def card(self, card_id: str) -> Card:
        with self._lock:
            return self._require(card_id)

    def create_card(self, board_id: str, list_id: str, title: str) -> Card:
        with self._lock:
            order = self._order.setdefault(list_id, [])
            prev_rank = self._cards[order[-1]].rank if order else None
            rank = rank_between(prev_rank, None)
            card = Card(f"card-{next(self._next_id)}", board_id, list_id, title, rank)
            self._cards[card.id] = card
            order.append(card.id)
            return card

    def cards_in_list(self, list_id: str) -> tuple[Card, ...]:
        with self._lock:
            return tuple(self._cards[cid] for cid in self._order.get(list_id, ()))

    def relocate(self, card_id: str, target_list_id: str, index: int | None = None) -> None:
        """把卡片挪到 `target_list_id`，插入到位置 `index`（`None` 表示列尾）。跨列移动与同列
        内重排走的是同一条路径——对索引来说都只是"从旧列摘掉、在新列按秩插入"。
        """
        with self._lock:
            card = self._require(card_id)
            old_order = self._order.setdefault(card.list_id, [])
            if card_id in old_order:
                old_order.remove(card_id)
            new_order = self._order.setdefault(target_list_id, [])
            idx = len(new_order) if index is None else max(0, min(index, len(new_order)))
            try:
                new_rank = self._rank_at(new_order, idx)
            except RankExhaustedError:
                self._rebalance(target_list_id)
                new_order = self._order[target_list_id]
                new_rank = self._rank_at(new_order, idx)
            card._place(target_list_id, new_rank)
            new_order.insert(idx, card_id)

    def _rank_at(self, order: list[str], idx: int) -> float:
        prev_rank = self._cards[order[idx - 1]].rank if idx > 0 else None
        next_rank = self._cards[order[idx]].rank if idx < len(order) else None
        return rank_between(prev_rank, next_rank)

    def _rebalance(self, list_id: str) -> None:
        for i, cid in enumerate(self._order[list_id]):
            self._cards[cid]._place(list_id, float(i))

    def assign(self, card_id: str, user_id: str | None) -> None:
        with self._lock:
            card = self._require(card_id)
            if card.assignee is not None:
                self._assignee_index.get(card.assignee, set()).discard(card_id)
            card._assign(user_id)
            if user_id is not None:
                self._assignee_index.setdefault(user_id, set()).add(card_id)

    def set_due_date(self, card_id: str, due: date | None) -> None:
        with self._lock:
            card = self._require(card_id)
            card._set_due(due)
            if due is not None and not card.archived:
                self._due_index[card_id] = due
            else:
                self._due_index.pop(card_id, None)

    def archive(self, card_id: str) -> None:
        with self._lock:
            card = self._require(card_id)
            card._archive()
            self._order.get(card.list_id, []).remove(card_id)
            if card.assignee is not None:
                self._assignee_index.get(card.assignee, set()).discard(card_id)
            self._due_index.pop(card_id, None)

    def cards_for_assignee(self, user_id: str) -> tuple[Card, ...]:
        with self._lock:
            return tuple(self._cards[cid] for cid in self._assignee_index.get(user_id, ()))

    def overdue_cards(self, today: date) -> tuple[Card, ...]:
        with self._lock:
            return tuple(self._cards[cid] for cid, due in self._due_index.items() if due < today)

    @property
    def indexed_card_count(self) -> int:
        """还挂在某个列索引里的卡片数——归档会让它变小，这是"索引会缩小"这条承诺的可验证证据。"""
        with self._lock:
            return sum(len(v) for v in self._order.values())


# --------------------------------------------------------------------------
# TaskBoardService：门面。创建看板与列、发卡、按工作流移动、指派、标签、到期日、归档、查询。


class TaskBoardService:
    """任务看板系统的入口。只有它同时知道 `Workflow`（这一步移动合不合法）和 `CardStore`
    （移动之后索引该怎么变），两个被编排的对象互不知道对方的存在——和餐厅题里
    `RestaurantService` 编排 `FloorManager`/`Kitchen` 是同一个道理。
    """

    def __init__(self, clock: Clock = utc_now) -> None:
        self._clock = clock
        self._boards: dict[str, Board] = {}
        self._store = CardStore()
        self._log: list[ActivityEvent] = []
        self._lock = threading.Lock()
        self._event_ids = itertools.count(1)

    def create_board(self, board_id: str, name: str) -> Board:
        with self._lock:
            if board_id in self._boards:
                raise DuplicateListError(f"board {board_id!r} already exists")
            board = Board(board_id, name)
            self._boards[board_id] = board
            return board

    def board(self, board_id: str) -> Board:
        try:
            return self._boards[board_id]
        except KeyError:
            raise UnknownBoardError(board_id) from None

    def add_list(self, board_id: str, list_id: str, name: str) -> BoardList:
        return self.board(board_id).add_list(list_id, name)

    def allow_transition(self, board_id: str, from_list: str, to_list: str) -> None:
        self.board(board_id).workflow.allow(from_list, to_list)

    def _record(self, card_id: str, event_type: ActivityType, actor: str, detail: str = "") -> None:
        with self._lock:
            event = ActivityEvent(f"evt-{next(self._event_ids)}", card_id, event_type, actor,
                                  self._clock(), detail)
            self._log.append(event)

    # ---- 第 1 关：看板、列、卡片 ----

    def create_card(self, board_id: str, list_id: str, title: str, actor: str) -> Card:
        board = self.board(board_id)
        if not board.has_list(list_id):
            raise UnknownListError(list_id)
        card = self._store.create_card(board_id, list_id, title)
        self._record(card.id, ActivityType.CREATED, actor, f"list={list_id}")
        return card

    def card(self, card_id: str) -> Card:
        return self._store.card(card_id)

    def reorder_card(self, card_id: str, index: int, actor: str) -> Card:
        """在同一列内重排位置——不是跨状态的转移，因此不查工作流。"""
        card = self._require_active(card_id)
        self._store.relocate(card_id, card.list_id, index)
        self._record(card_id, ActivityType.MOVED, actor, f"reorder@{card.list_id}")
        return card

    # ---- 第 2 关：工作流转移、指派、标签、到期日 ----

    def move_card(self, card_id: str, target_list_id: str, actor: str, index: int | None = None) -> Card:
        card = self._require_active(card_id)
        board = self.board(card.board_id)
        if not board.has_list(target_list_id):
            raise UnknownListError(target_list_id)
        if target_list_id != card.list_id and not board.workflow.can_transition(card.list_id, target_list_id):
            raise IllegalTransitionError(f"{card.list_id} -> {target_list_id} is not an allowed transition")
        origin = card.list_id
        self._store.relocate(card_id, target_list_id, index)
        self._record(card_id, ActivityType.MOVED, actor, f"{origin}->{target_list_id}")
        return card

    def _require_active(self, card_id: str) -> Card:
        card = self._store.card(card_id)
        if card.archived:
            raise CardArchivedError(card_id)
        return card

    def assign_card(self, card_id: str, user_id: str, actor: str) -> Card:
        card = self._require_active(card_id)
        self._store.assign(card_id, user_id)
        self._record(card_id, ActivityType.ASSIGNED, actor, user_id)
        return card

    def unassign_card(self, card_id: str, actor: str) -> Card:
        card = self._require_active(card_id)
        self._store.assign(card_id, None)
        self._record(card_id, ActivityType.UNASSIGNED, actor)
        return card

    def label_card(self, card_id: str, label: str, actor: str) -> Card:
        card = self._require_active(card_id)
        card.add_label(label)
        self._record(card_id, ActivityType.LABELED, actor, label)
        return card

    def unlabel_card(self, card_id: str, label: str, actor: str) -> Card:
        card = self._require_active(card_id)
        card.remove_label(label)
        self._record(card_id, ActivityType.UNLABELED, actor, label)
        return card

    def set_due_date(self, card_id: str, due: date | None, actor: str) -> Card:
        card = self._require_active(card_id)
        self._store.set_due_date(card_id, due)
        event_type = ActivityType.DUE_DATE_SET if due is not None else ActivityType.DUE_DATE_CLEARED
        self._record(card_id, event_type, actor, str(due) if due else "")
        return card

    def archive_card(self, card_id: str, actor: str) -> Card:
        card = self._require_active(card_id)
        self._store.archive(card_id)
        self._record(card_id, ActivityType.ARCHIVED, actor)
        return card

    # ---- 第 4 关：清单——不碰移动逻辑 ----

    def add_checklist_item(self, card_id: str, text: str, actor: str) -> ChecklistItem:
        card = self._require_active(card_id)
        item = card.add_checklist_item(text)
        self._record(card_id, ActivityType.CHECKLIST_ITEM_ADDED, actor, item.item_id)
        return item

    def toggle_checklist_item(self, card_id: str, item_id: str, actor: str) -> ChecklistItem:
        card = self._require_active(card_id)
        item = card.toggle_checklist_item(item_id)
        self._record(card_id, ActivityType.CHECKLIST_ITEM_TOGGLED, actor, item_id)
        return item

    # ---- 第 3 关：查询 ----

    def board_view(self, board_id: str) -> Mapping[str, tuple[Card, ...]]:
        """按列分组的看板视图——每一列各自一次索引查询，不扫全站的卡。"""
        board = self.board(board_id)
        return {list_id: self._store.cards_in_list(list_id) for list_id in board.list_ids()}

    def cards_for_assignee(self, user_id: str) -> tuple[Card, ...]:
        return self._store.cards_for_assignee(user_id)

    def overdue_cards(self) -> tuple[Card, ...]:
        return self._store.overdue_cards(self._clock().date())

    def history_for(self, card_id: str) -> tuple[ActivityEvent, ...]:
        with self._lock:
            return tuple(e for e in self._log if e.card_id == card_id)

    @property
    def indexed_card_count(self) -> int:
        return self._store.indexed_card_count


def _demo() -> None:
    service = TaskBoardService()
    service.create_board("b1", "Sprint 42")
    for list_id, name in (("todo", "To Do"), ("doing", "In Progress"), ("done", "Done")):
        service.add_list("b1", list_id, name)
    for a, b in (("todo", "doing"), ("doing", "done"), ("doing", "todo")):
        service.allow_transition("b1", a, b)
    card = service.create_card("b1", "todo", "写设计文档", actor="ada")
    service.assign_card(card.id, "grace", actor="ada")
    service.move_card(card.id, "doing", actor="grace")
    print("board view:", {k: [c.title for c in v] for k, v in service.board_view("b1").items()})
    print("grace's cards:", [c.title for c in service.cards_for_assignee("grace")])


if __name__ == "__main__":
    _demo()
