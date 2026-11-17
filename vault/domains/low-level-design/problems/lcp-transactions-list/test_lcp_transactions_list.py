"""交易列表视图模型的测试：合同每一条、示例逐字运行、隔离的各个方向。"""
import copy
import dataclasses
import importlib
import os

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

ALL, CREDIT, DEBIT = "all", "credit", "debit"
MAX_ID = 9_007_199_254_740_991


def txn(tid, kind, amount="$1.00", date="01-01-2030", address="1 Test Way", city="Testville", loc=None, zip_code=90000):
    loc_id = tid + 1000 if loc is None else loc
    return impl.Transaction(tid, date, kind, amount, impl.Location(loc_id, address, city, zip_code))


def item_tuples(snap):
    return [(i.id, i.address, i.city, i.amount, i.date) for i in snap.items]


def flags(snap):
    return [(f.filter, f.active) for f in snap.filters]


def as_plain(obj):
    return dataclasses.asdict(obj)


@pytest.fixture
def sample():
    return [
        txn(7, CREDIT, "$30.00", "02-03-2031", "4 Mill Lane", "Ashford", loc=71, zip_code=20001),
        txn(8, DEBIT, "$5.25", "03-03-2031", "12 Quay Street", "Brookvale", loc=72, zip_code=20002),
        txn(9, CREDIT, "$2.00", "04-03-2031", "8 Hill Rise", "Cresswell", loc=73, zip_code=20003),
    ]


# ---- 规则 1：构造与筛选项 ----

def test_initial_snapshot_all_selected_and_filters_in_fixed_order(sample):
    snap = impl.TransactionsList(sample).snapshot()
    assert snap.activeFilter == ALL
    assert flags(snap) == [(ALL, True), (CREDIT, False), (DEBIT, False)]
    assert all(type(f.active) is bool for f in snap.filters)
    assert item_tuples(snap) == [
        (7, "4 Mill Lane", "Ashford", "$30.00", "02-03-2031"),
        (8, "12 Quay Street", "Brookvale", "$5.25", "03-03-2031"),
        (9, "8 Hill Rise", "Cresswell", "$2.00", "04-03-2031"),
    ]


def test_readme_style_example_end_to_end():
    first = txn(31, CREDIT, "$9.90", "11-05-2032", "3 Dock Road", "Seaton", loc=5, zip_code=30001)
    second = txn(32, DEBIT, "$1.10", "12-05-2032", "6 Elm Court", "Tarnby", loc=6, zip_code=30002)
    view = impl.TransactionsList([first, second])
    assert item_tuples(view.snapshot()) == [
        (31, "3 Dock Road", "Seaton", "$9.90", "11-05-2032"),
        (32, "6 Elm Court", "Tarnby", "$1.10", "12-05-2032"),
    ]
    view.selectFilter(DEBIT)
    snap = view.snapshot()
    assert item_tuples(snap) == [(32, "6 Elm Court", "Tarnby", "$1.10", "12-05-2032")]
    assert flags(snap) == [(ALL, False), (CREDIT, False), (DEBIT, True)]
    view.replaceTransactions([txn(33, DEBIT, "$7.00", "13-05-2032", "9 Fern Gate", "Ulverby", loc=7, zip_code=30003)])
    snap = view.snapshot()
    assert snap.activeFilter == DEBIT
    assert item_tuples(snap) == [(33, "9 Fern Gate", "Ulverby", "$7.00", "13-05-2032")]
    view.replaceTransactions([])
    snap = view.snapshot()
    assert snap.activeFilter == DEBIT and snap.items == []
    assert flags(snap) == [(ALL, False), (CREDIT, False), (DEBIT, True)]


@pytest.mark.parametrize("name,expected_ids", [(ALL, [7, 8, 9]), (CREDIT, [7, 9]), (DEBIT, [8])])
def test_each_filter_shows_the_right_rows(sample, name, expected_ids):
    view = impl.TransactionsList(sample)
    view.selectFilter(name)
    snap = view.snapshot()
    assert [i.id for i in snap.items] == expected_ids
    assert [f.filter for f in snap.filters if f.active] == [name]
    assert snap.activeFilter == name


def test_repeated_selection_is_harmless(sample):
    view = impl.TransactionsList(sample)
    view.selectFilter(CREDIT)
    first = as_plain(view.snapshot())
    view.selectFilter(CREDIT)
    view.selectFilter(CREDIT)
    assert as_plain(view.snapshot()) == first
    view.selectFilter(ALL)
    view.selectFilter(ALL)
    assert [i.id for i in view.snapshot().items] == [7, 8, 9]


def test_filter_with_no_match_stays_active_and_empty():
    view = impl.TransactionsList([txn(1, CREDIT), txn(2, CREDIT)])
    view.selectFilter(DEBIT)
    snap = view.snapshot()
    assert snap.items == []
    assert snap.activeFilter == DEBIT
    assert flags(snap) == [(ALL, False), (CREDIT, False), (DEBIT, True)]


def test_empty_initial_list():
    view = impl.TransactionsList([])
    snap = view.snapshot()
    assert snap.items == [] and snap.activeFilter == ALL
    assert flags(snap) == [(ALL, True), (CREDIT, False), (DEBIT, False)]
    view.selectFilter(CREDIT)
    assert view.snapshot().items == []


# ---- 规则 3：展示项 ----

def test_input_order_is_kept_not_sorted():
    rows = [txn(50, CREDIT, date="09-09-2030"), txn(-4, DEBIT, date="01-01-2030"), txn(0, CREDIT, date="05-05-2030"),
            txn(12, DEBIT, date="03-03-2030")]
    view = impl.TransactionsList(rows)
    assert [i.id for i in view.snapshot().items] == [50, -4, 0, 12]
    view.selectFilter(DEBIT)
    assert [i.id for i in view.snapshot().items] == [-4, 12]


def test_item_id_is_transaction_id_and_location_fields_are_not_leaked():
    view = impl.TransactionsList([txn(5, CREDIT, loc=999, zip_code=12345)])
    item = view.snapshot().items[0]
    assert item.id == 5
    assert [f.name for f in dataclasses.fields(item)] == ["id", "address", "city", "amount", "date"]
    assert 999 not in as_plain(item).values() and 12345 not in as_plain(item).values()


def test_extreme_integer_ids_survive():
    rows = [txn(MAX_ID, CREDIT, loc=-MAX_ID, zip_code=-MAX_ID), txn(-MAX_ID, DEBIT, loc=MAX_ID, zip_code=MAX_ID)]
    snap = impl.TransactionsList(rows).snapshot()
    assert [i.id for i in snap.items] == [MAX_ID, -MAX_ID]
    assert all(type(i.id) is int for i in snap.items)


def test_display_strings_are_copied_verbatim():
    odd = txn(1, CREDIT, amount="  €1.234,50 \t", date=" 2031年3月4日\n", address="  Rue de l'Église  ", city="Zürich ")
    zero = txn(2, DEBIT, amount="", date="", address="", city="")
    snap = impl.TransactionsList([odd, zero]).snapshot()
    assert item_tuples(snap) == [
        (1, "  Rue de l'Église  ", "Zürich ", "  €1.234,50 \t", " 2031年3月4日\n"),
        (2, "", "", "", ""),
    ]


# ---- 规则 4：换列表 ----

def test_replace_keeps_filter_and_applies_it_immediately(sample):
    view = impl.TransactionsList(sample)
    view.selectFilter(CREDIT)
    view.replaceTransactions([txn(20, DEBIT), txn(21, CREDIT), txn(22, CREDIT), txn(23, DEBIT)])
    snap = view.snapshot()
    assert snap.activeFilter == CREDIT
    assert [i.id for i in snap.items] == [21, 22]


def test_replace_is_total_and_keeps_replacement_order(sample):
    view = impl.TransactionsList(sample)
    view.replaceTransactions([txn(9, CREDIT), txn(3, CREDIT), txn(8, DEBIT)])
    assert [i.id for i in view.snapshot().items] == [9, 3, 8]
    view.replaceTransactions([txn(3, DEBIT)])
    assert [i.id for i in view.snapshot().items] == [3]
    view.selectFilter(CREDIT)
    assert view.snapshot().items == []


def test_replace_with_all_selected_then_back_to_default():
    view = impl.TransactionsList([txn(1, CREDIT)])
    view.replaceTransactions([])
    assert view.snapshot().items == []
    view.replaceTransactions([txn(2, DEBIT)])
    snap = view.snapshot()
    assert snap.activeFilter == ALL and [i.id for i in snap.items] == [2]


# ---- 规则 6：隔离 ----

def test_inputs_are_not_modified_by_the_view(sample):
    before = copy.deepcopy(sample)
    view = impl.TransactionsList(sample)
    view.selectFilter(DEBIT)
    view.snapshot()
    replacement = [txn(40, CREDIT), txn(41, DEBIT)]
    replacement_before = copy.deepcopy(replacement)
    view.replaceTransactions(replacement)
    view.snapshot()
    assert sample == before
    assert replacement == replacement_before


def test_caller_edits_after_construction_do_not_reach_the_view(sample):
    view = impl.TransactionsList(sample)
    expected = as_plain(view.snapshot())
    sample[0].location.address = "edited"
    sample[0].amount = "edited"
    sample[1].txnType = CREDIT
    sample[2].location = impl.Location(0, "other", "other", 0)
    sample.append(txn(99, DEBIT))
    sample.clear()
    assert as_plain(view.snapshot()) == expected
    view.selectFilter(DEBIT)
    assert [i.id for i in view.snapshot().items] == [8]


def test_caller_edits_after_replace_do_not_reach_the_view():
    view = impl.TransactionsList([])
    incoming = [txn(1, CREDIT, address="before"), txn(2, DEBIT)]
    view.replaceTransactions(incoming)
    expected = as_plain(view.snapshot())
    incoming[0].location.address = "after"
    incoming[0].date = "after"
    incoming.reverse()
    incoming.pop()
    assert as_plain(view.snapshot()) == expected


def test_one_object_shared_by_two_slots_is_still_isolated():
    shared = txn(4, CREDIT)
    view = impl.TransactionsList([shared])
    view.replaceTransactions([shared])
    shared.location.city = "moved"
    assert view.snapshot().items[0].city == "Testville"


def test_snapshot_edits_do_not_touch_the_view_or_other_snapshots(sample):
    view = impl.TransactionsList(sample)
    reference = as_plain(view.snapshot())
    kept = view.snapshot()
    scratch = view.snapshot()
    scratch.items.append(None)
    scratch.items[0].address = "scribble"
    scratch.items[1].id = -1
    scratch.filters[0].active = False
    scratch.filters[2].active = True
    scratch.filters.clear()
    scratch.activeFilter = "nonsense"
    scratch.items.clear()
    assert as_plain(view.snapshot()) == reference
    assert as_plain(kept) == reference


def test_old_snapshots_survive_later_selections_and_replacements(sample):
    view = impl.TransactionsList(sample)
    first = view.snapshot()
    first_plain = as_plain(first)
    view.selectFilter(CREDIT)
    second = view.snapshot()
    second_plain = as_plain(second)
    view.replaceTransactions([txn(60, DEBIT)])
    view.selectFilter(DEBIT)
    assert as_plain(first) == first_plain
    assert as_plain(second) == second_plain
    assert first.items is not second.items and first.filters is not second.filters


def test_two_snapshots_share_no_mutable_object(sample):
    view = impl.TransactionsList(sample)
    a, b = view.snapshot(), view.snapshot()
    assert a is not b and a.items is not b.items and a.filters is not b.filters
    assert all(x is not y for x, y in zip(a.items, b.items))
    assert all(x is not y for x, y in zip(a.filters, b.filters))


def test_instances_are_independent(sample):
    one = impl.TransactionsList(sample)
    two = impl.TransactionsList(copy.deepcopy(sample))
    one.selectFilter(CREDIT)
    one.replaceTransactions([])
    snap = two.snapshot()
    assert snap.activeFilter == ALL
    assert [i.id for i in snap.items] == [7, 8, 9]
    two.selectFilter(DEBIT)
    assert one.snapshot().activeFilter == CREDIT


def test_a_thousand_rows_keep_order_and_filter_split():
    rows = [txn(n, CREDIT if n % 3 else DEBIT) for n in range(1000, 0, -1)]
    view = impl.TransactionsList(rows)
    assert [i.id for i in view.snapshot().items] == list(range(1000, 0, -1))
    view.selectFilter(DEBIT)
    assert [i.id for i in view.snapshot().items] == [n for n in range(1000, 0, -1) if n % 3 == 0]

