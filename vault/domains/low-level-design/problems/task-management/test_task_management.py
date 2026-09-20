"""任务看板的验收测试：秩排序的位置维护（含秩耗尽后的重排）、工作流转移的合法性、
三条产品查询各自的索引、归档收缩索引、清单不碰移动逻辑、并发建卡的不变量。

所有断言只看公开方法与属性（`list_id`、`rank`、`assignee`、`labels`、`due_date`、`archived`、
`checklist`、`indexed_card_count` 等），不碰任何下划线开头的东西。看板与卡片的搭建放在每个
测试函数体内，不是 fixture：starter 的 `__init__` 会 `raise NotImplementedError`，构造放在
测试体内才会被 pytest 记成一次明确的失败。
"""

from __future__ import annotations

import importlib
import os
import threading
from datetime import date, datetime, timedelta, timezone

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


class FrozenClock:
    def __init__(self, start: datetime) -> None:
        self._now = start

    def __call__(self) -> datetime:
        return self._now

    def advance(self, days: int) -> None:
        self._now += timedelta(days=days)


def make_service(clock: FrozenClock | None = None) -> "impl.TaskBoardService":
    return impl.TaskBoardService(clock=clock or FrozenClock(datetime(2026, 1, 1, tzinfo=timezone.utc)))


def make_board(service, board_id: str = "b1") -> None:
    service.create_board(board_id, "Sprint")
    for list_id, name in (("todo", "To Do"), ("doing", "In Progress"), ("done", "Done")):
        service.add_list(board_id, list_id, name)
    for a, b in (("todo", "doing"), ("doing", "done"), ("doing", "todo")):
        service.allow_transition(board_id, a, b)


def test_cards_append_in_rank_order() -> None:
    service = make_service()
    make_board(service)
    a = service.create_card("b1", "todo", "a", actor="ada")
    b = service.create_card("b1", "todo", "b", actor="ada")
    c = service.create_card("b1", "todo", "c", actor="ada")
    titles = [card.title for card in service.board_view("b1")["todo"]]
    assert titles == ["a", "b", "c"]
    assert a.rank < b.rank < c.rank


def test_reorder_within_list_changes_position_only() -> None:
    service = make_service()
    make_board(service)
    a = service.create_card("b1", "todo", "a", actor="ada")
    b = service.create_card("b1", "todo", "b", actor="ada")
    c = service.create_card("b1", "todo", "c", actor="ada")
    service.reorder_card(c.id, 0, actor="ada")
    titles = [card.title for card in service.board_view("b1")["todo"]]
    assert titles == ["c", "a", "b"]
    assert c.list_id == "todo"


def test_move_across_lists_allowed_by_workflow() -> None:
    service = make_service()
    make_board(service)
    card = service.create_card("b1", "todo", "task", actor="ada")
    service.move_card(card.id, "doing", actor="ada")
    assert card.list_id == "doing"
    assert [c.title for c in service.board_view("b1")["todo"]] == []
    assert [c.title for c in service.board_view("b1")["doing"]] == ["task"]


def test_move_rejected_by_workflow_raises() -> None:
    service = make_service()
    make_board(service)
    card = service.create_card("b1", "todo", "task", actor="ada")
    with pytest.raises(impl.IllegalTransitionError):
        service.move_card(card.id, "done", actor="ada")


def test_move_to_current_list_is_a_reorder_not_a_workflow_transition() -> None:
    service = make_service()
    make_board(service)
    a = service.create_card("b1", "todo", "a", actor="ada")
    b = service.create_card("b1", "todo", "b", actor="ada")
    service.move_card(b.id, "todo", actor="ada", index=0)
    assert [c.title for c in service.board_view("b1")["todo"]] == ["b", "a"]


def test_rank_between_eventually_exhausts_and_signals_caller() -> None:
    prev, nxt = 0.0, 1.0
    for _ in range(2000):
        try:
            mid = impl.rank_between(prev, nxt)
        except impl.RankExhaustedError:
            return
        nxt = mid
    pytest.fail("expected RankExhaustedError once the gap underflows")


def test_repeated_insertion_in_same_gap_stays_correctly_ordered() -> None:
    """秩间距被反复挤占最终会耗尽，`reorder_card` 必须透明地重排整列而不是把异常抛给调用方。"""
    service = make_service()
    make_board(service)
    first = service.create_card("b1", "todo", "first", actor="ada")
    last = service.create_card("b1", "todo", "last", actor="ada")
    for i in range(80):
        card = service.create_card("b1", "todo", f"mid-{i}", actor="ada")
        service.reorder_card(card.id, 1, actor="ada")  # 一直插到 first 之后
    cards = service.board_view("b1")["todo"]
    assert len(cards) == 82
    ranks = [c.rank for c in cards]
    assert ranks == sorted(ranks)
    assert len(set(ranks)) == len(ranks)
    assert cards[0].id == first.id and cards[-1].id == last.id


def test_assign_and_unassign_update_cross_board_index() -> None:
    service = make_service()
    make_board(service, "b1")
    make_board(service, "b2")
    c1 = service.create_card("b1", "todo", "a", actor="ada")
    c2 = service.create_card("b2", "todo", "b", actor="ada")
    service.assign_card(c1.id, "grace", actor="ada")
    service.assign_card(c2.id, "grace", actor="ada")
    assigned = {c.id for c in service.cards_for_assignee("grace")}
    assert assigned == {c1.id, c2.id}
    service.unassign_card(c1.id, actor="ada")
    assert {c.id for c in service.cards_for_assignee("grace")} == {c2.id}
    assert c1.assignee is None


def test_labels_add_and_remove() -> None:
    service = make_service()
    make_board(service)
    card = service.create_card("b1", "todo", "a", actor="ada")
    service.label_card(card.id, "urgent", actor="ada")
    service.label_card(card.id, "bug", actor="ada")
    assert card.labels == frozenset({"urgent", "bug"})
    service.unlabel_card(card.id, "urgent", actor="ada")
    assert card.labels == frozenset({"bug"})


def test_overdue_query_only_returns_unarchived_past_due_cards() -> None:
    clock = FrozenClock(datetime(2026, 1, 10, tzinfo=timezone.utc))
    service = make_service(clock)
    make_board(service)
    overdue = service.create_card("b1", "todo", "overdue", actor="ada")
    future = service.create_card("b1", "todo", "future", actor="ada")
    no_due = service.create_card("b1", "todo", "no-due", actor="ada")
    service.set_due_date(overdue.id, date(2026, 1, 1), actor="ada")
    service.set_due_date(future.id, date(2026, 6, 1), actor="ada")
    assert {c.id for c in service.overdue_cards()} == {overdue.id}
    assert overdue.is_overdue(date(2026, 1, 10))
    assert not no_due.is_overdue(date(2026, 1, 10))


def test_archive_removes_card_from_indexes_but_keeps_it_addressable() -> None:
    service = make_service()
    make_board(service)
    card = service.create_card("b1", "todo", "a", actor="ada")
    service.assign_card(card.id, "grace", actor="ada")
    service.set_due_date(card.id, date(2020, 1, 1), actor="ada")
    before = service.indexed_card_count
    service.archive_card(card.id, actor="ada")
    assert service.indexed_card_count == before - 1
    assert card.archived is True
    assert [c.title for c in service.board_view("b1")["todo"]] == []
    assert card.id not in {c.id for c in service.cards_for_assignee("grace")}
    assert card.id not in {c.id for c in service.overdue_cards()}
    assert service.card(card.id) is card  # 仍能按 id 直接查到，只是不再出现在索引视图里


def test_archived_card_rejects_further_mutation() -> None:
    service = make_service()
    make_board(service)
    card = service.create_card("b1", "todo", "a", actor="ada")
    service.archive_card(card.id, actor="ada")
    with pytest.raises(impl.CardArchivedError):
        service.move_card(card.id, "doing", actor="ada")
    with pytest.raises(impl.CardArchivedError):
        service.assign_card(card.id, "grace", actor="ada")


def test_checklist_independent_of_move_logic() -> None:
    service = make_service()
    make_board(service)
    card = service.create_card("b1", "todo", "a", actor="ada")
    item = service.add_checklist_item(card.id, "write tests", actor="ada")
    assert card.checklist == (item,)
    assert item.done is False
    service.toggle_checklist_item(card.id, item.item_id, actor="ada")
    assert card.checklist[0].done is True
    service.move_card(card.id, "doing", actor="ada")
    assert card.checklist[0].done is True
    assert card.checklist[0].item_id == item.item_id


def test_activity_log_is_append_only_source_of_truth() -> None:
    service = make_service()
    make_board(service)
    card = service.create_card("b1", "todo", "a", actor="ada")
    service.assign_card(card.id, "grace", actor="ada")
    service.move_card(card.id, "doing", actor="grace")
    events = service.history_for(card.id)
    kinds = [e.type for e in events]
    assert kinds == [impl.ActivityType.CREATED, impl.ActivityType.ASSIGNED, impl.ActivityType.MOVED]
    assert events[-1].actor == "grace"
    assert events[-1].detail == "todo->doing"


def test_unknown_card_and_list_raise() -> None:
    service = make_service()
    make_board(service)
    with pytest.raises(impl.UnknownCardError):
        service.card("card-missing")
    with pytest.raises(impl.UnknownListError):
        service.create_card("b1", "backlog", "x", actor="ada")
    with pytest.raises(impl.UnknownBoardError):
        service.board("ghost")


def test_duplicate_list_id_rejected() -> None:
    service = make_service()
    make_board(service)
    with pytest.raises(impl.DuplicateListError):
        service.add_list("b1", "todo", "Again")


def test_board_view_groups_cards_by_list_in_declared_order() -> None:
    service = make_service()
    make_board(service)
    service.create_card("b1", "todo", "a", actor="ada")
    service.create_card("b1", "doing", "b", actor="ada")
    view = service.board_view("b1")
    assert list(view.keys()) == ["todo", "doing", "done"]
    assert [c.title for c in view["todo"]] == ["a"]
    assert [c.title for c in view["doing"]] == ["b"]
    assert view["done"] == ()


def test_concurrent_card_creation_has_no_lost_cards_or_duplicate_ranks() -> None:
    service = make_service()
    make_board(service)
    n = 12
    barrier = threading.Barrier(n)
    created: list[object] = [None] * n

    def worker(i: int) -> None:
        barrier.wait()
        created[i] = service.create_card("b1", "todo", f"card-{i}", actor="ada")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert all(c is not None for c in created)
    ids = {c.id for c in created}
    assert len(ids) == n  # 没有两个线程拿到同一个 card id
    cards = service.board_view("b1")["todo"]
    assert len(cards) == n
    ranks = [c.rank for c in cards]
    assert len(set(ranks)) == n  # 没有两张卡挤到同一个秩上
    assert ranks == sorted(ranks)
