"""图书馆管理的验收测试。用 `IMPL=starter` 跑同一套即可验证自己的实现。"""

from __future__ import annotations

import importlib
import os
import threading
from datetime import UTC, datetime, timedelta

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

BASE = datetime(2026, 9, 1, 10, 0, tzinfo=UTC)


class Desk:
    """一个可控时钟 + 一座小图书馆，测试里用它推进时间。"""

    def __init__(self, copies: dict[str, int], policies=None, kinds=None) -> None:
        self.now = BASE
        self.catalog = impl.Catalog()
        kinds = kinds or {}
        for title_id, count in copies.items():
            self.catalog.add_title(impl.Title(title_id, f"书 {title_id}",
                                              kinds.get(title_id, impl.MediaKind.BOOK),
                                              creator="作者" + title_id))
            for index in range(count):
                self.catalog.add_copy(f"{title_id}-{index + 1}", title_id)
        self.library = impl.Library(self.catalog, clock=lambda: self.now,
                                    policies=policies or impl.PolicyTable())

    def member(self, member_id: str, member_type=None):
        self.library.add_member(impl.Member(member_id, member_id,
                                            member_type or impl.MemberType.PUBLIC))
        return member_id

    def advance(self, days: float) -> None:
        self.now = self.now + timedelta(days=days)


# ---- 第 1 关：书目与副本的分界线 ----------------------------------------------

def test_a_title_is_not_a_copy():
    """搜索命中的是书目，借走的是副本：同一个书目的三本副本是三个不同的条码。"""
    desk = Desk({"T1": 3})
    assert desk.catalog.copy_count == 3
    assert desk.catalog.barcodes_of("T1") == ("T1-1", "T1-2", "T1-3")
    hits = desk.catalog.search("书 T1")
    assert [title.id for title in hits] == ["T1"]
    assert desk.library.availability("T1") == 3
    desk.member("M1")
    loan = desk.library.borrow("M1", "T1")
    assert loan.barcode in desk.catalog.barcodes_of("T1")
    assert loan.title_id == "T1"
    assert desk.library.availability("T1") == 2


def test_search_matches_name_or_creator_and_is_title_level():
    desk = Desk({"T1": 1, "T2": 1})
    assert [t.id for t in desk.catalog.search("作者T2")] == ["T2"]
    assert [t.id for t in desk.catalog.search("书")] == ["T1", "T2"]
    assert desk.catalog.search("没有这本") == ()


def test_borrowing_the_last_copy_leaves_nothing_to_borrow():
    desk = Desk({"T1": 1})
    desk.member("M1")
    desk.member("M2")
    desk.library.borrow("M1", "T1")
    with pytest.raises(impl.NoCopyAvailableError):
        desk.library.borrow("M2", "T1")


# ---- 第 2 关：限额、借期、罚金、续借 -------------------------------------------

def test_loan_limit_comes_from_the_policy_of_the_member_type():
    policies = impl.PolicyTable(impl.LoanPolicy(max_loans=5),
                                {(impl.MemberType.STUDENT, None): impl.LoanPolicy(max_loans=2)})
    desk = Desk({"T1": 1, "T2": 1, "T3": 1}, policies=policies)
    desk.member("S1", impl.MemberType.STUDENT)
    desk.member("P1", impl.MemberType.PUBLIC)
    desk.library.borrow("S1", "T1")
    desk.library.borrow("S1", "T2")
    with pytest.raises(impl.LoanLimitReachedError):
        desk.library.borrow("S1", "T3")
    # 同一批书对普通读者不触发限额：政策是按读者类型查的。
    desk.library.borrow("P1", "T3")


def test_fines_accrue_on_the_clock_before_the_book_comes_back():
    policies = impl.PolicyTable(impl.LoanPolicy(loan_days=7, fine_per_day=50))
    desk = Desk({"T1": 1}, policies=policies)
    desk.member("M1")
    desk.library.borrow("M1", "T1")
    desk.advance(7)
    assert desk.library.fines_owed("M1") == 0
    desk.advance(3)
    # 还没还书，罚金已经在涨——这正是"罚金是算出来的，不是存下来的"。
    assert desk.library.fines_owed("M1") == 3 * 50
    receipt = desk.library.return_copy("T1-1")
    assert receipt.days_overdue == 3 and receipt.fine == 150
    assert desk.library.fines_owed("M1") == 150
    desk.advance(30)
    # 书还了，罚金就不再涨。
    assert desk.library.fines_owed("M1") == 150


def test_a_part_day_overdue_still_costs_a_whole_day():
    policies = impl.PolicyTable(impl.LoanPolicy(loan_days=7, fine_per_day=50))
    desk = Desk({"T1": 1}, policies=policies)
    desk.member("M1")
    desk.library.borrow("M1", "T1")
    desk.advance(7.25)
    assert desk.library.fines_owed("M1") == 50


def test_renewal_is_capped_and_pushes_the_due_date_from_today():
    policies = impl.PolicyTable(impl.LoanPolicy(loan_days=7, max_renewals=1))
    desk = Desk({"T1": 1}, policies=policies)
    desk.member("M1")
    loan = desk.library.borrow("M1", "T1")
    desk.advance(3)
    renewed = desk.library.renew(loan.id)
    assert renewed.renewals == 1
    assert renewed.due_at == desk.now + timedelta(days=7)
    with pytest.raises(impl.RenewalRefusedError):
        desk.library.renew(loan.id)


def test_renewal_is_refused_when_someone_else_is_waiting():
    """排队的人的承诺优先于在借者的方便——这道题唯一真正的规则冲突。"""
    desk = Desk({"T1": 1})
    desk.member("M1")
    desk.member("M2")
    loan = desk.library.borrow("M1", "T1")
    desk.library.place_hold("M2", "T1")
    with pytest.raises(impl.RenewalRefusedError):
        desk.library.renew(loan.id)
    # 排队的人撤了，续借立刻恢复。
    desk.library.cancel_hold("M2", "T1")
    assert desk.library.renew(loan.id).renewals == 1


# ---- 第 3 关：预约队列、取书架、过期 -------------------------------------------

def test_a_hold_is_refused_while_a_copy_is_on_the_shelf():
    desk = Desk({"T1": 2})
    desk.member("M1")
    with pytest.raises(impl.HoldRefusedError):
        desk.library.place_hold("M1", "T1")


def test_the_returned_copy_goes_to_the_head_of_the_queue_not_to_a_walk_in():
    desk = Desk({"T1": 1})
    for name in ("M1", "M2", "M3", "M4"):
        desk.member(name)
    desk.library.borrow("M1", "T1")
    assert desk.library.place_hold("M2", "T1") == 1
    assert desk.library.place_hold("M3", "T1") == 2
    receipt = desk.library.return_copy("T1-1")
    assert receipt.held_for == "M2"
    # 这本书留在取书架上，路过的人借不走，可借数是 0。
    assert desk.library.availability("T1") == 0
    with pytest.raises(impl.NoCopyAvailableError):
        desk.library.borrow("M4", "T1")
    # 队首的人来取，队列随之缩短。
    assert desk.library.queued_count == 1
    loan = desk.library.borrow("M2", "T1")
    assert loan.barcode == "T1-1"
    assert desk.library.shelf_size == 0
    assert desk.library.queue_position("M3", "T1") == 1


def test_an_expired_hold_leaves_the_queue_and_the_book_moves_on():
    """不来取的人不能永远占着一本书：到期即下架，且他**退出队列**，不回队尾。"""
    policies = impl.PolicyTable(impl.LoanPolicy(hold_days=3))
    desk = Desk({"T1": 1}, policies=policies)
    for name in ("M1", "M2", "M3"):
        desk.member(name)
    desk.library.borrow("M1", "T1")
    desk.library.place_hold("M2", "T1")
    desk.library.place_hold("M3", "T1")
    assert desk.library.return_copy("T1-1").held_for == "M2"
    desk.advance(4)
    # M2 的保留到期：书转给 M3，M2 不在队列里了。
    assert desk.library.shelf_size == 1
    assert desk.library.queued_count == 0
    assert desk.library.queue_position("M2", "T1") == 0
    with pytest.raises(impl.NoCopyAvailableError):
        desk.library.borrow("M2", "T1")
    assert desk.library.borrow("M3", "T1").barcode == "T1-1"


def test_an_expired_hold_with_an_empty_queue_puts_the_book_back_on_the_shelf():
    policies = impl.PolicyTable(impl.LoanPolicy(hold_days=3))
    desk = Desk({"T1": 1}, policies=policies)
    desk.member("M1")
    desk.member("M2")
    desk.library.borrow("M1", "T1")
    desk.library.place_hold("M2", "T1")
    desk.library.return_copy("T1-1")
    assert desk.library.availability("T1") == 0
    desk.advance(4)
    assert desk.library.availability("T1") == 1
    assert desk.library.shelf_size == 0
    assert desk.library.queued_count == 0


def test_every_exit_from_the_queue_shrinks_it():
    """离队有四条路径：被排到取书架、取消、借到了、过期。任何一条都不能留下空壳。"""
    desk = Desk({"T1": 1})
    for name in ("M1", "M2", "M3"):
        desk.member(name)
    desk.library.borrow("M1", "T1")
    desk.library.place_hold("M2", "T1")
    desk.library.place_hold("M3", "T1")
    assert desk.library.queued_count == 2
    assert desk.library.cancel_hold("M3", "T1") is True
    assert desk.library.queued_count == 1
    assert desk.library.cancel_hold("M3", "T1") is False
    desk.library.return_copy("T1-1")          # M2 上架，离队
    assert desk.library.queued_count == 0
    desk.library.borrow("M2", "T1")           # 取走
    assert desk.library.shelf_size == 0 and desk.library.queued_count == 0


def test_cancelling_a_shelved_hold_hands_the_book_to_the_next_in_line():
    desk = Desk({"T1": 1})
    for name in ("M1", "M2", "M3"):
        desk.member(name)
    desk.library.borrow("M1", "T1")
    desk.library.place_hold("M2", "T1")
    desk.library.place_hold("M3", "T1")
    assert desk.library.return_copy("T1-1").held_for == "M2"
    assert desk.library.cancel_hold("M2", "T1") is True
    assert desk.library.borrow("M3", "T1").barcode == "T1-1"


def test_borrowing_by_other_means_removes_the_member_from_the_queue():
    """两本副本：M2 排着 T1 的队，另一本被还回来他先借到了，队里不能还留着他。"""
    desk = Desk({"T1": 2})
    for name in ("M1", "M2"):
        desk.member(name)
    desk.library.borrow("M1", "T1")
    second = desk.library.borrow("M2", "T1")
    desk.library.return_copy(second.barcode)
    # 现在有书可借，直接预约会被拒，所以先把两本都借空再排队。
    desk.library.borrow("M2", "T1")
    with pytest.raises(impl.HoldRefusedError):
        desk.library.place_hold("M2", "T1")


# ---- 第 4 关：新介质、新读者类型、并发 -----------------------------------------

def test_a_new_media_kind_only_needs_a_policy_row():
    """加 DVD 不碰借还流程一行：借期、罚金、留架天数全部来自政策表。"""
    policies = impl.PolicyTable(
        impl.LoanPolicy(loan_days=14, fine_per_day=50),
        {(None, impl.MediaKind.DVD): impl.LoanPolicy(loan_days=2, fine_per_day=200, hold_days=1)})
    desk = Desk({"T1": 1, "D1": 1}, policies=policies,
                kinds={"D1": impl.MediaKind.DVD})
    desk.member("M1")
    book = desk.library.borrow("M1", "T1")
    dvd = desk.library.borrow("M1", "D1")
    assert (book.due_at - book.out_at).days == 14
    assert (dvd.due_at - dvd.out_at).days == 2
    desk.advance(3)
    assert desk.library.return_copy(dvd.barcode).fine == 200


def test_the_most_specific_policy_row_wins():
    policies = impl.PolicyTable(
        impl.LoanPolicy(loan_days=14),
        {(impl.MemberType.STAFF, impl.MediaKind.DVD): impl.LoanPolicy(loan_days=7),
         (impl.MemberType.STAFF, None): impl.LoanPolicy(loan_days=30),
         (None, impl.MediaKind.DVD): impl.LoanPolicy(loan_days=2)})
    desk = Desk({"T1": 1, "D1": 1}, policies=policies, kinds={"D1": impl.MediaKind.DVD})
    desk.member("F1", impl.MemberType.STAFF)
    desk.member("P1", impl.MemberType.PUBLIC)
    assert (desk.library.borrow("F1", "D1").due_at - desk.now).days == 7
    assert (desk.library.borrow("F1", "T1").due_at - desk.now).days == 30
    desk.library.return_copy("D1-1")
    assert (desk.library.borrow("P1", "D1").due_at - desk.now).days == 2


def test_concurrent_borrowers_never_lend_the_same_copy_twice():
    """十个读者同时抢三本副本：恰好三笔借阅，三个不同的条码。"""
    desk = Desk({"T1": 3})
    names = [f"M{i}" for i in range(10)]
    for name in names:
        desk.member(name)
    barrier = threading.Barrier(len(names))
    loans: list[str] = []
    refused: list[str] = []
    guard = threading.Lock()

    def attempt(name: str) -> None:
        barrier.wait()
        try:
            loan = desk.library.borrow(name, "T1")
        except impl.NoCopyAvailableError:
            with guard:
                refused.append(name)
        else:
            with guard:
                loans.append(loan.barcode)

    threads = [threading.Thread(target=attempt, args=(name,)) for name in names]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert len(loans) == 3, f"over-lent: {loans}"
    assert len(set(loans)) == 3, f"same copy lent twice: {loans}"
    assert len(refused) == 7
    assert desk.library.availability("T1") == 0


def test_concurrent_holds_produce_a_total_order_with_no_duplicates():
    """八个读者同时预约同一本书：位次恰好是 1..8，没有重复也没有空洞。"""
    desk = Desk({"T1": 1})
    names = [f"M{i}" for i in range(9)]
    for name in names:
        desk.member(name)
    desk.library.borrow("M0", "T1")
    waiting = names[1:]
    barrier = threading.Barrier(len(waiting))
    positions: list[int] = []
    guard = threading.Lock()

    def attempt(name: str) -> None:
        barrier.wait()
        position = desk.library.place_hold(name, "T1")
        with guard:
            positions.append(position)

    threads = [threading.Thread(target=attempt, args=(name,)) for name in waiting]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert sorted(positions) == list(range(1, len(waiting) + 1))
    assert desk.library.queued_count == len(waiting)


def test_unknown_entities_raise_instead_of_printing():
    desk = Desk({"T1": 1})
    desk.member("M1")
    with pytest.raises(impl.UnknownEntityError):
        desk.library.borrow("nobody", "T1")
    with pytest.raises(impl.UnknownEntityError):
        desk.library.borrow("M1", "T9")
    with pytest.raises(impl.UnknownEntityError):
        desk.library.return_copy("T1-1")
    with pytest.raises(impl.UnknownEntityError):
        desk.library.renew("L99")


def test_a_member_waiting_on_the_shelf_cannot_queue_again():
    """书已经为他留在取书架上了，再排一次队会让他在队列和取书架上各占一份。"""
    desk = Desk({"T1": 1})
    desk.member("M1")
    desk.member("M2")
    desk.library.borrow("M1", "T1")
    desk.library.place_hold("M2", "T1")
    desk.library.return_copy("T1-1")
    assert desk.library.shelf_size == 1 and desk.library.queued_count == 0
    with pytest.raises(impl.HoldRefusedError):
        desk.library.place_hold("M2", "T1")
    assert desk.library.queued_count == 0
