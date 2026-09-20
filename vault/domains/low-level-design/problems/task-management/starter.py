"""任务看板（Task Management）练习骨架：公开 API 与参考解一模一样，方法体留空。

把每个 `raise NotImplementedError` 换成你自己的实现，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/task-management -q`。
内部表示随你选：测试只看公开方法与属性（`list_id`、`rank`、`assignee`、`labels`、`due_date`、
`archived`、`checklist`、`indexed_card_count` 等），不碰任何下划线开头的东西。
"""

from __future__ import annotations

import itertools
import threading
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import date, datetime, timezone
from enum import Enum
from typing import Callable

Clock = Callable[[], datetime]


def utc_now() -> datetime:
    """默认时钟。"""
    return datetime.now(timezone.utc)


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


class RankExhaustedError(Exception):
    """相邻两张卡的秩已经挨得太近，浮点精度分不出中点了。"""


def rank_between(prev_rank: float | None, next_rank: float | None) -> float:
    raise NotImplementedError


class ActivityType(Enum):
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
    event_id: str
    card_id: str
    type: ActivityType
    actor: str
    at: datetime
    detail: str = ""


@dataclass(slots=True)
class ChecklistItem:
    item_id: str
    text: str
    done: bool = False


class Workflow:
    def __init__(self, states: Iterable[str] = ()) -> None:
        raise NotImplementedError

    def add_state(self, state_id: str) -> None:
        raise NotImplementedError

    def allow(self, from_state: str, to_state: str) -> None:
        raise NotImplementedError

    def can_transition(self, from_state: str, to_state: str) -> bool:
        raise NotImplementedError

    def states(self) -> frozenset[str]:
        raise NotImplementedError


@dataclass(slots=True)
class BoardList:
    id: str
    name: str


class Board:
    def __init__(self, board_id: str, name: str) -> None:
        raise NotImplementedError

    def add_list(self, list_id: str, name: str) -> BoardList:
        raise NotImplementedError

    def has_list(self, list_id: str) -> bool:
        raise NotImplementedError

    def list_name(self, list_id: str) -> str:
        raise NotImplementedError

    def list_ids(self) -> tuple[str, ...]:
        raise NotImplementedError


class Card:
    def __init__(self, card_id: str, board_id: str, list_id: str, title: str, rank: float) -> None:
        raise NotImplementedError

    @property
    def list_id(self) -> str:
        raise NotImplementedError

    @property
    def rank(self) -> float:
        raise NotImplementedError

    @property
    def assignee(self) -> str | None:
        raise NotImplementedError

    @property
    def labels(self) -> frozenset[str]:
        raise NotImplementedError

    @property
    def due_date(self) -> date | None:
        raise NotImplementedError

    @property
    def archived(self) -> bool:
        raise NotImplementedError

    @property
    def checklist(self) -> tuple[ChecklistItem, ...]:
        raise NotImplementedError

    def is_overdue(self, today: date) -> bool:
        raise NotImplementedError

    def add_label(self, label: str) -> None:
        raise NotImplementedError

    def remove_label(self, label: str) -> None:
        raise NotImplementedError

    def add_checklist_item(self, text: str) -> ChecklistItem:
        raise NotImplementedError

    def toggle_checklist_item(self, item_id: str) -> ChecklistItem:
        raise NotImplementedError


class CardStore:
    def __init__(self) -> None:
        raise NotImplementedError

    def card(self, card_id: str) -> Card:
        raise NotImplementedError

    def create_card(self, board_id: str, list_id: str, title: str) -> Card:
        raise NotImplementedError

    def cards_in_list(self, list_id: str) -> tuple[Card, ...]:
        raise NotImplementedError

    def relocate(self, card_id: str, target_list_id: str, index: int | None = None) -> None:
        raise NotImplementedError

    def assign(self, card_id: str, user_id: str | None) -> None:
        raise NotImplementedError

    def set_due_date(self, card_id: str, due: date | None) -> None:
        raise NotImplementedError

    def archive(self, card_id: str) -> None:
        raise NotImplementedError

    def cards_for_assignee(self, user_id: str) -> tuple[Card, ...]:
        raise NotImplementedError

    def overdue_cards(self, today: date) -> tuple[Card, ...]:
        raise NotImplementedError

    @property
    def indexed_card_count(self) -> int:
        raise NotImplementedError


class TaskBoardService:
    def __init__(self, clock: Clock = utc_now) -> None:
        raise NotImplementedError

    def create_board(self, board_id: str, name: str) -> Board:
        raise NotImplementedError

    def board(self, board_id: str) -> Board:
        raise NotImplementedError

    def add_list(self, board_id: str, list_id: str, name: str) -> BoardList:
        raise NotImplementedError

    def allow_transition(self, board_id: str, from_list: str, to_list: str) -> None:
        raise NotImplementedError

    def create_card(self, board_id: str, list_id: str, title: str, actor: str) -> Card:
        raise NotImplementedError

    def card(self, card_id: str) -> Card:
        raise NotImplementedError

    def reorder_card(self, card_id: str, index: int, actor: str) -> Card:
        raise NotImplementedError

    def move_card(self, card_id: str, target_list_id: str, actor: str, index: int | None = None) -> Card:
        raise NotImplementedError

    def assign_card(self, card_id: str, user_id: str, actor: str) -> Card:
        raise NotImplementedError

    def unassign_card(self, card_id: str, actor: str) -> Card:
        raise NotImplementedError

    def label_card(self, card_id: str, label: str, actor: str) -> Card:
        raise NotImplementedError

    def unlabel_card(self, card_id: str, label: str, actor: str) -> Card:
        raise NotImplementedError

    def set_due_date(self, card_id: str, due: date | None, actor: str) -> Card:
        raise NotImplementedError

    def archive_card(self, card_id: str, actor: str) -> Card:
        raise NotImplementedError

    def add_checklist_item(self, card_id: str, text: str, actor: str) -> ChecklistItem:
        raise NotImplementedError

    def toggle_checklist_item(self, card_id: str, item_id: str, actor: str) -> ChecklistItem:
        raise NotImplementedError

    def board_view(self, board_id: str) -> Mapping[str, tuple[Card, ...]]:
        raise NotImplementedError

    def cards_for_assignee(self, user_id: str) -> tuple[Card, ...]:
        raise NotImplementedError

    def overdue_cards(self) -> tuple[Card, ...]:
        raise NotImplementedError

    def history_for(self, card_id: str) -> tuple[ActivityEvent, ...]:
        raise NotImplementedError

    @property
    def indexed_card_count(self) -> int:
        raise NotImplementedError
