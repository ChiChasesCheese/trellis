import copy
import importlib
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))
ServiceError = impl.ServiceError


def fails(status, code, fn, *args, **kwargs):
    """调用必须抛 ServiceError(status, code)。"""
    with pytest.raises(ServiceError) as info:
        fn(*args, **kwargs)
    assert (info.value.status, info.value.code) == (status, code)


def service_with(*invoices):
    service = impl.ReconciliationService()
    if invoices:
        assert service.register_invoices(list(invoices)) == (201, {"registered_count": len(invoices)})
    return service


def statuses(service):
    return {row["invoice_id"]: (row["status"], row["settled_by_payment_id"]) for row in service.list_invoices()[1]}


def pay(service, text, forgiveness=0, key=None):
    return service.reconcile_payment(text, forgiveness=forgiveness, key=key)


# ---- README 里的例子与公开用例 ----

def test_readme_batch_example():
    service = service_with("INV A, 2026-03-01, 100", "INV B, 2026-03-02, 100")
    status, result = service.reconcile_batch([
        {"payment": "p1, 1, paying for:INV A", "key": "retry-1"},
        {"payment": "p1, 1, paying for:INV A", "key": "retry-1"},
        {"payment": "p2, 100"},
    ])
    assert status == 200
    assert [row["status"] for row in result["results"]] == [201, 200, 201]
    assert [row["body"]["settled_invoice_id"] for row in result["results"]] == ["INV A", "INV A", "INV B"]
    assert [row["body"]["tier_used"] for row in result["results"]] == ["id", "id", "exact"]
    assert result["results"][0]["body"] == result["results"][1]["body"]


def test_readme_batch_rollback_example():
    service = service_with("a, 2026-01-01, 10")
    fails(400, "invalid_input", service.reconcile_batch,
          [{"payment": "p3, 10", "key": "new-key"}, {"payment": "invalid"}])
    assert statuses(service) == {"a": ("UNPAID", None)}
    assert pay(service, "q, 10", key="new-key")[0] == 201  # 键也没有留下


def test_public_register_and_tiers():
    service = impl.ReconciliationService()
    assert service.register_invoices(["INV-1, 2026-03-01, 100", "INV-2, 2026-04-01, 200"]) == (201, {"registered_count": 2})
    service = service_with("INV-7, 2026-03-01, 250", "INV-3, 2026-02-01, 100")
    status, body = pay(service, "pay_1, 100, paying for: INV-7")
    assert (status, body["settled_invoice_id"], body["tier_used"]) == (201, "INV-7", "id")
    service = service_with("INV-9, 2026-04-01, 100", "INV-4, 2026-01-15, 100")
    status, body = pay(service, "pay_2, 100, March rent, thanks")
    assert (status, body["settled_invoice_id"], body["tier_used"]) == (201, "INV-4", "exact")
    service = service_with("INV-1, 2026-05-01, 100", "INV-2, 2026-06-01, 130")
    status, body = pay(service, "pay_3, 98, bank transfer", forgiveness=2)
    assert (status, body["settled_invoice_id"], body["tier_used"]) == (201, "INV-1", "fuzzy")
    service = service_with("INV-1, 2026-05-01, 100")
    status, body = pay(service, "pay_4, 500, no match here")
    assert (status, body["status"], body["settled_invoice_id"]) == (200, "UNMATCHED", None)


def test_message_and_body_shapes():
    service = service_with("INV-1, 2026-03-01, 100")
    assert pay(service, " p1 , 0100, rent") == (201, {
        "status": "MATCHED", "payment_id": "p1", "settled_invoice_id": "INV-1", "tier_used": "exact",
        "message": "Payment p1 paid 100 for invoice INV-1 due on 2026-03-01"})
    assert pay(service, "p2, 7") == (200, {
        "status": "UNMATCHED", "payment_id": "p2", "settled_invoice_id": None, "tier_used": None,
        "message": "Payment p2 could not be matched to any invoice"})


# ---- 登记发票 ----

BAD_BATCHES = [
    [], None, "INV, 2026-03-01, 100", ("INV, 2026-03-01, 100",), [7], [None], ["INV, 2026-03-01"],
    ["INV, 2026-03-01, 100, extra"], ["INV,2026-03-01,100"], [", 2026-03-01, 100"], ["   , 2026-03-01, 100"],
    ["x" * 65 + ", 2026-03-01, 100"],
    ["A, 2026-3-1, 100"], ["A, 2026-02-30, 100"], ["A, 2026-13-01, 100"], ["A, 2026-00-10, 100"],
    ["A, 0000-01-01, 100"], ["A, 20260301, 100"], ["A, 2026-03-01T00:00, 100"], ["A, ２０２６-03-01, 100"],
    ["A, 2025-02-29, 100"],
    ["A, 2026-03-01, 0"], ["A, 2026-03-01, 000"], ["A, 2026-03-01, -5"], ["A, 2026-03-01, +5"],
    ["A, 2026-03-01, 1_0"], ["A, 2026-03-01, １２"], ["A, 2026-03-01, 1.5"], ["A, 2026-03-01, "],
    ["A, 2026-03-01, abc"], ["A, 2026-03-01, 1 0"], ["A, 2026-03-01, ٣"],
]


@pytest.mark.parametrize("batch", BAD_BATCHES, ids=range(len(BAD_BATCHES)))
def test_bad_invoice_batches_are_400_and_store_nothing(batch):
    service = service_with("KEEP, 2026-01-01, 5")
    fails(400, "invalid_input", service.register_invoices, batch)
    assert [row["invoice_id"] for row in service.list_invoices()[1]] == ["KEEP"]


def test_invoice_fields_are_trimmed_and_boundaries_accepted():
    service = impl.ReconciliationService()
    long_id = "x" * 64
    assert service.register_invoices(["  INV 1  ,  2026-03-01 ,  0100 ", f" {long_id} , 2024-02-29, 1"]) == (
        201, {"registered_count": 2})
    rows = service.list_invoices()[1]
    assert rows == [
        {"invoice_id": long_id, "due_date": "2024-02-29", "amount_cents": 1, "status": "UNPAID", "settled_by_payment_id": None},
        {"invoice_id": "INV 1", "due_date": "2026-03-01", "amount_cents": 100, "status": "UNPAID", "settled_by_payment_id": None},
    ]


def test_registration_is_atomic_on_duplicates():
    service = service_with("A, 2026-01-01, 5")
    fails(409, "duplicate_invoice", service.register_invoices, ["B, 2026-01-02, 5", "A, 2026-01-03, 5"])
    fails(409, "duplicate_invoice", service.register_invoices, ["C, 2026-01-02, 5", "C , 2026-01-03, 6"])
    assert [row["invoice_id"] for row in service.list_invoices()[1]] == ["A"]
    assert service.register_invoices(["B, 2026-01-02, 5"]) == (201, {"registered_count": 1})
    assert [row["invoice_id"] for row in service.list_invoices()[1]] == ["A", "B"]


def test_registration_first_error_wins_in_row_order():
    service = service_with("A, 2026-01-01, 5")
    # 批内重复排在畸形行前面：先遇到 409
    fails(409, "duplicate_invoice", service.register_invoices, ["B, 2026-01-01, 5", "B, 2026-01-01, 5", "bad"])
    # 畸形行在前：先遇到 400
    fails(400, "invalid_input", service.register_invoices, ["bad", "B, 2026-01-01, 5", "B, 2026-01-01, 5"])
    # 与账本重复的号要等全部行都通过校验之后才检查：后面的畸形行先报 400
    fails(400, "invalid_input", service.register_invoices, ["A, 2026-01-01, 5", "bad"])
    fails(409, "duplicate_invoice", service.register_invoices, ["A, 2026-01-01, 5", "C, 2026-01-01, 5"])


def test_invoice_ids_are_case_sensitive():
    service = service_with("inv, 2026-01-01, 5", "INV, 2026-01-01, 5")
    assert [row["invoice_id"] for row in service.list_invoices()[1]] == ["INV", "inv"]


# ---- 付款输入 ----

BAD_PAYMENTS = [None, 5, b"p1, 1", ["p1, 1"], "", "p1", "p1,100", "p1, 100,", ", 100", " , 100", "p" * 65 + ", 1",
                "p1, 0", "p1, 00", "p1, -1", "p1, +1", "p1, 1.0", "p1, abc", "p1, ", "p1, １２", "p1, 1_0"]


@pytest.mark.parametrize("payment", BAD_PAYMENTS, ids=range(len(BAD_PAYMENTS)))
def test_bad_payment_strings_are_400(payment):
    service = service_with("INV, 2026-01-01, 1")
    fails(400, "invalid_input", service.reconcile_payment, payment)
    assert statuses(service) == {"INV": ("UNPAID", None)}


@pytest.mark.parametrize("forgiveness", [-1, True, False, 1.5, "1", None, [1]])
def test_bad_forgiveness_is_400(forgiveness):
    service = service_with("INV, 2026-01-01, 1")
    fails(400, "invalid_input", service.reconcile_payment, "p1, 1", forgiveness=forgiveness)


@pytest.mark.parametrize("key", ["", "k" * 65, 5, b"k", ["k"], 1.5])
def test_bad_key_is_400(key):
    service = service_with("INV, 2026-01-01, 1")
    fails(400, "invalid_input", service.reconcile_payment, "p1, 1", key=key)
    assert pay(service, "p1, 1", key="k" * 64)[0] == 201  # 64 个字符是合法边界


def test_payment_id_is_trimmed_and_memo_keeps_commas():
    service = service_with("INV-1, 2026-01-01, 9")
    status, body = pay(service, "  p-1 , 5, note, with, commas, paying for: INV-1")
    assert (status, body["payment_id"], body["settled_invoice_id"], body["tier_used"]) == (201, "p-1", "INV-1", "id")
    assert statuses(service) == {"INV-1": ("PAID", "p-1")}


def test_memo_may_be_empty_or_missing():
    service = service_with("A, 2026-01-01, 5", "B, 2026-01-02, 5")
    assert pay(service, "p1, 5")[1]["settled_invoice_id"] == "A"
    assert pay(service, "p2, 5, ")[1]["settled_invoice_id"] == "B"


# ---- 三级匹配 ----

def test_id_tier_beats_exact_and_ignores_amount():
    service = service_with("INV-1, 2026-05-01, 500", "INV-2, 2026-01-01, 100")
    status, body = pay(service, "p1, 100, paying for: INV-1")
    assert (status, body["settled_invoice_id"], body["tier_used"]) == (201, "INV-1", "id")
    assert statuses(service) == {"INV-1": ("PAID", "p1"), "INV-2": ("UNPAID", None)}


@pytest.mark.parametrize("memo", ["PAYING FOR: INV-1", "Paying Off:INV-1", "pAyInG fOr:   INV-1   ", "x, paying off: INV-1, y",
                                  "PAYİNG FOR: INV-1", "payıng off:INV-1", "PAYİNG OFF: INV-1", "PAYIng for:INV-1"])
def test_marker_is_case_insensitive_with_dotted_and_dotless_i(memo):
    service = service_with("INV-1, 2026-05-01, 500", "OTHER, 2026-01-01, 3")
    status, body = pay(service, f"p1, 3, {memo}")
    assert (status, body["settled_invoice_id"], body["tier_used"]) == (201, "INV-1", "id")


def test_marker_position_survives_case_changing_characters_before_it():
    # 备注里 İ 小写后长度会变；位置必须取自原串
    service = service_with("INV-1, 2026-05-01, 500", "OTHER, 2026-01-01, 3")
    assert pay(service, "p1, 3, İİİİ paying for: INV-1")[1]["settled_invoice_id"] == "INV-1"


def test_invoice_id_in_memo_is_case_sensitive_and_may_contain_spaces():
    service = service_with("INV A, 2026-05-01, 500", "Z, 2026-01-01, 3")
    assert pay(service, "p1, 3, paying for: inv a")[1]["settled_invoice_id"] == "Z"  # 大小写不同：落到第二级
    assert pay(service, "p2, 3, paying for: INV A")[1]["settled_invoice_id"] == "INV A"


def test_marker_id_stops_at_next_comma_only():
    service = service_with("INV-1, 2026-05-01, 500", "Z, 2026-01-01, 3")
    assert pay(service, "p1, 3, paying for: INV-1 thanks")[1]["tier_used"] == "exact"  # 号是 "INV-1 thanks"
    assert pay(service, "p2, 3, paying for: INV-1, thanks")[1]["tier_used"] == "id"


def test_markers_scan_left_to_right_and_skip_unusable_ids():
    service = service_with("A, 2026-05-01, 500", "B, 2026-05-02, 500", "C, 2026-01-01, 3")
    assert pay(service, "p1, 3, paying for: nope, paying off: B, paying for: A")[1]["settled_invoice_id"] == "B"
    assert pay(service, "p2, 3, paying for: B, paying for: A")[1]["settled_invoice_id"] == "A"  # B 已付，跳过
    assert pay(service, "p3, 3, paying for: A")[1]["settled_invoice_id"] == "C"  # A 也已付，落到第二级
    assert pay(service, "p4, 3, paying for:")[1]["status"] == "UNMATCHED"  # 空号不指向任何发票


def test_exact_tier_tie_breaks_by_date_then_id():
    service = service_with("c, 2026-02-01, 100", "b, 2026-02-01, 100", "z, 2026-01-01, 100", "a, 2026-03-01, 100")
    order = [pay(service, f"p{i}, 100")[1]["settled_invoice_id"] for i in range(4)]
    assert order == ["z", "b", "c", "a"]
    assert pay(service, "p9, 100")[1]["status"] == "UNMATCHED"  # 付过的发票不再参与


def test_fuzzy_tier_needs_forgiveness_and_is_inclusive():
    service = service_with("A, 2026-01-01, 95", "B, 2026-01-02, 105", "C, 2026-01-03, 106", "D, 2026-01-04, 94")
    assert pay(service, "p0, 100")[1]["status"] == "UNMATCHED"  # forgiveness=0：没有第三级
    assert pay(service, "p1, 100", forgiveness=5)[1]["settled_invoice_id"] == "A"  # 下界含
    assert pay(service, "p2, 100", forgiveness=5)[1]["settled_invoice_id"] == "B"  # 上界含
    assert pay(service, "p3, 100", forgiveness=5)[1]["status"] == "UNMATCHED"  # 106、94 都在界外一分
    assert pay(service, "p4, 100", forgiveness=6)[1]["settled_invoice_id"] == "C"


def test_fuzzy_tie_breaks_by_date_then_difference_then_id():
    service = service_with("A, 2026-03-02, 104", "B, 2026-03-01, 96", "D, 2026-03-01, 102", "C, 2026-03-01, 98")
    assert pay(service, "p1, 100", forgiveness=5)[1]["settled_invoice_id"] == "C"  # 同日里差最小是 98 与 102，号小的 C
    assert pay(service, "p2, 100", forgiveness=5)[1]["settled_invoice_id"] == "D"
    assert pay(service, "p3, 100", forgiveness=5)[1]["settled_invoice_id"] == "B"  # 同日只剩 96
    assert pay(service, "p4, 100", forgiveness=5)[1]["settled_invoice_id"] == "A"


def test_difference_beats_id_when_dates_are_equal():
    service = service_with("A, 2026-03-01, 104", "Z, 2026-03-01, 101")
    assert pay(service, "p1, 100", forgiveness=5)[1]["settled_invoice_id"] == "Z"


def test_date_beats_difference():
    service = service_with("near, 2026-03-02, 101", "far, 2026-03-01, 104")
    assert pay(service, "p1, 100", forgiveness=5)[1]["settled_invoice_id"] == "far"


def test_exact_beats_fuzzy_even_when_fuzzy_is_earlier():
    service = service_with("early, 2026-01-01, 99", "late, 2026-09-01, 100")
    status, body = pay(service, "p1, 100", forgiveness=5)
    assert (body["settled_invoice_id"], body["tier_used"]) == ("late", "exact")


def test_settled_invoice_is_isolated_from_later_matches():
    service = service_with("A, 2026-01-01, 100", "B, 2026-01-02, 100")
    assert pay(service, "p1, 100, paying for: A")[1]["settled_invoice_id"] == "A"
    assert pay(service, "p2, 100, paying for: A")[1]["settled_invoice_id"] == "B"
    assert pay(service, "p3, 100, paying for: A", forgiveness=50)[1]["status"] == "UNMATCHED"
    assert statuses(service) == {"A": ("PAID", "p1"), "B": ("PAID", "p2")}


def test_unmatched_leaves_ledger_unchanged_and_payment_ids_are_only_labels():
    service = service_with("A, 2026-01-01, 100")
    before = service.list_invoices()
    assert pay(service, "p1, 7")[0] == 200
    assert service.list_invoices() == before
    assert pay(service, "p1, 100")[0] == 201  # 同一个付款号可以再用：它不是隐式幂等键
    assert pay(service, "p1, 100")[0] == 200


def test_huge_amounts_are_exact_integers():
    big = 10**30
    service = service_with(f"A, 2026-01-01, {big}")
    status, body = pay(service, f"p1, {big - 3}", forgiveness=3)
    assert (status, body["tier_used"]) == (201, "fuzzy")
    assert body["message"] == f"Payment p1 paid {big - 3} for invoice A due on 2026-01-01"
    fails(400, "invalid_input", service.reconcile_payment, "p2, " + "9" * 5000)


# ---- 幂等与重试 ----

def test_replay_returns_original_response_even_after_state_changed():
    service = service_with("A, 2026-01-01, 100")
    first = pay(service, "p1, 100", key="k")
    assert first[0] == 201
    service.register_invoices(["B, 2026-01-02, 100"])
    replay = pay(service, "p1, 100", key="k")
    assert replay == (200, first[1])
    assert statuses(service) == {"A": ("PAID", "p1"), "B": ("UNPAID", None)}  # 没有再结算 B


def test_unmatched_responses_are_cached_too():
    service = service_with("A, 2026-01-01, 100")
    assert pay(service, "p1, 55", key="k")[0] == 200
    service.register_invoices(["B, 2026-01-02, 55"])
    status, body = pay(service, "p1, 55", key="k")
    assert (status, body["status"]) == (200, "UNMATCHED")
    assert statuses(service)["B"] == ("UNPAID", None)


def test_conflicting_reuse_of_a_key_is_409_and_changes_nothing():
    service = service_with("A, 2026-01-01, 100", "B, 2026-01-02, 100")
    pay(service, "p1, 100", key="k")
    before = service.list_invoices()
    fails(409, "idempotency_conflict", service.reconcile_payment, "p2, 100", key="k")  # 付款号不同
    fails(409, "idempotency_conflict", service.reconcile_payment, "p1, 101", key="k")  # 金额不同
    fails(409, "idempotency_conflict", service.reconcile_payment, "p1, 100, memo", key="k")  # 备注不同
    fails(409, "idempotency_conflict", service.reconcile_payment, "p1, 100", forgiveness=1, key="k")
    assert service.list_invoices() == before


def test_canonical_payload_strips_the_whole_text_only():
    service = service_with("A, 2026-01-01, 100")
    first = pay(service, "p1, 100, rent", key="k")
    assert pay(service, "  p1, 100, rent \n", key="k") == (200, first[1])
    fails(409, "idempotency_conflict", service.reconcile_payment, "p1,  100, rent", key="k")  # 内部空白算内容


def test_requests_are_validated_before_the_key_is_looked_up():
    service = service_with("A, 2026-01-01, 100")
    pay(service, "p1, 100", key="k")
    fails(400, "invalid_input", service.reconcile_payment, "bad", key="k")
    fails(400, "invalid_input", service.reconcile_payment, "p1, 100", forgiveness=-1, key="k")


def test_keys_are_global_and_whitespace_is_significant():
    service = service_with("A, 2026-01-01, 100", "B, 2026-01-02, 100", "C, 2026-01-03, 100")
    assert pay(service, "p1, 100", key="k")[1]["settled_invoice_id"] == "A"
    assert pay(service, "p2, 100", key=" k")[1]["settled_invoice_id"] == "B"
    assert pay(service, "p3, 100", key=" ")[1]["settled_invoice_id"] == "C"
    fails(409, "idempotency_conflict", service.reconcile_payment, "p2, 100", key="k")


def test_requests_without_a_key_always_use_the_current_ledger():
    service = service_with("A, 2026-01-01, 100", "B, 2026-01-02, 100")
    assert pay(service, "p1, 100")[1]["settled_invoice_id"] == "A"
    assert pay(service, "p1, 100")[1]["settled_invoice_id"] == "B"
    assert pay(service, "p1, 100")[1]["status"] == "UNMATCHED"


def test_replayed_bodies_are_detached_snapshots():
    service = service_with("A, 2026-01-01, 100")
    status, body = pay(service, "p1, 100", key="k")
    original = copy.deepcopy(body)
    body["settled_invoice_id"] = "HACKED"
    again = pay(service, "p1, 100", key="k")[1]
    assert again == original
    again["status"] = "HACKED"
    assert pay(service, "p1, 100", key="k")[1] == original


# ---- 列表与快照 ----

def test_list_is_sorted_by_due_date_then_id_across_batches():
    service = impl.ReconciliationService()
    assert service.list_invoices() == (200, [])
    service.register_invoices(["b, 2026-02-01, 1", "a, 2026-03-01, 1"])
    service.register_invoices(["c, 2026-02-01, 1", "A, 2026-03-01, 1", "z, 2025-12-31, 1"])
    assert [row["invoice_id"] for row in service.list_invoices()[1]] == ["z", "b", "c", "A", "a"]
    assert set(service.list_invoices()[1][0]) == {"invoice_id", "due_date", "amount_cents", "status", "settled_by_payment_id"}


def test_list_returns_detached_snapshots_and_inputs_are_not_retained():
    inputs = ["A, 2026-01-01, 100"]
    service = impl.ReconciliationService()
    service.register_invoices(inputs)
    inputs[0] = "B, 2026-01-01, 100"
    inputs.append("C, 2026-01-01, 1")
    rows = service.list_invoices()[1]
    rows[0]["status"] = "PAID"
    rows.clear()
    assert statuses(service) == {"A": ("UNPAID", None)}


# ---- 批次 ----

def test_batch_rows_see_earlier_settlements_and_each_row_keeps_its_status():
    service = service_with("A, 2026-01-01, 100", "B, 2026-01-02, 100")
    status, result = service.reconcile_batch([{"payment": "p1, 100"}, {"payment": "p2, 100"}, {"payment": "p3, 100"}])
    assert status == 200
    assert [(row["status"], row["body"]["settled_invoice_id"]) for row in result["results"]] == [
        (201, "A"), (201, "B"), (200, None)]  # 没匹配是成功的结果，不让整批失败
    assert statuses(service) == {"A": ("PAID", "p1"), "B": ("PAID", "p2")}


def test_batch_rolls_back_settlements_and_keys_on_a_later_error():
    service = service_with("A, 2026-01-01, 100", "B, 2026-01-02, 100")
    pay(service, "before, 100", key="old")  # 批前已有的状态与键要保留
    fails(400, "invalid_input", service.reconcile_batch,
          [{"payment": "p1, 100", "key": "new"}, {"payment": "p2, 55", "key": "unmatched"}, {"payment": "bad"}])
    assert statuses(service) == {"A": ("PAID", "before"), "B": ("UNPAID", None)}
    assert pay(service, "other, 55", key="new")[0] == 200  # "new" 没有留下；这一次真的评估（B 的金额是 100，所以未匹配）
    assert pay(service, "before, 100", key="old") == (200, {
        "status": "MATCHED", "payment_id": "before", "settled_invoice_id": "A", "tier_used": "exact",
        "message": "Payment before paid 100 for invoice A due on 2026-01-01"})
    assert statuses(service)["B"] == ("UNPAID", None)


def test_batch_idempotency_conflict_rolls_everything_back():
    service = service_with("A, 2026-01-01, 100", "B, 2026-01-02, 100")
    pay(service, "p0, 100", key="old")
    fails(409, "idempotency_conflict", service.reconcile_batch,
          [{"payment": "p1, 100", "key": "fresh"}, {"payment": "different, 100", "key": "old"}])
    assert statuses(service) == {"A": ("PAID", "p0"), "B": ("UNPAID", None)}
    assert pay(service, "q, 100", key="fresh")[1]["settled_invoice_id"] == "B"


def test_same_key_inside_a_batch_replays_or_conflicts():
    service = service_with("A, 2026-01-01, 100", "B, 2026-01-02, 100")
    fails(409, "idempotency_conflict", service.reconcile_batch,
          [{"payment": "p1, 100", "key": "k"}, {"payment": "p1, 100", "forgiveness": 1, "key": "k"}])
    assert statuses(service) == {"A": ("UNPAID", None), "B": ("UNPAID", None)}


def test_batch_first_error_wins_in_row_order():
    service = service_with("A, 2026-01-01, 100")
    pay(service, "p0, 100", key="old")
    fails(409, "idempotency_conflict", service.reconcile_batch,
          [{"payment": "x, 1", "key": "old"}, {"payment": "bad"}])
    fails(400, "invalid_input", service.reconcile_batch,
          [{"payment": "bad"}, {"payment": "x, 1", "key": "old"}])


@pytest.mark.parametrize("batch", [
    None, [], {}, "p1, 1", ({"payment": "p1, 1"},), ["p1, 1"], [None], [{}], [{"forgiveness": 1}],
    [{"payment": "p1, 1", "extra": 1}], [{"payment": "p1, 1", "Key": "k"}], [{"payment": 5}],
    [{"payment": "p1, 1", "forgiveness": True}], [{"payment": "p1, 1", "forgiveness": -1}],
    [{"payment": "p1, 1", "key": ""}], [{"payment": "p1, 1", "key": 5}], [{"payment": "p1, 0"}],
], ids=range(17))
def test_bad_batch_shapes_are_400_and_change_nothing(batch):
    service = service_with("A, 2026-01-01, 1")
    fails(400, "invalid_input", service.reconcile_batch, batch)
    assert statuses(service) == {"A": ("UNPAID", None)}


def test_batch_accepts_optional_fields_and_null_key():
    service = service_with("A, 2026-01-01, 100", "B, 2026-01-02, 98")
    status, result = service.reconcile_batch([
        {"payment": "p1, 100", "key": None, "forgiveness": 0}, {"payment": "p2, 100", "forgiveness": 2}])
    assert [(row["status"], row["body"]["tier_used"]) for row in result["results"]] == [(201, "exact"), (201, "fuzzy")]


def test_batch_does_not_mutate_requests_and_results_are_detached():
    service = service_with("A, 2026-01-01, 100")
    rows = [{"payment": "p1, 100", "key": "k"}, {"payment": "p1, 100", "key": "k"}]
    snapshot = copy.deepcopy(rows)
    _, result = service.reconcile_batch(rows)
    assert rows == snapshot
    first, second = result["results"]
    assert first["body"] == second["body"] and first["body"] is not second["body"]
    first["body"]["settled_invoice_id"] = "HACKED"
    result["results"].clear()
    assert pay(service, "p1, 100", key="k")[1]["settled_invoice_id"] == "A"


def test_single_calls_after_a_rolled_back_batch_start_from_the_old_ledger():
    service = service_with("A, 2026-01-01, 100")
    for _ in range(3):
        fails(400, "invalid_input", service.reconcile_batch, [{"payment": "p1, 100", "key": "k"}, {"payment": "bad"}])
    assert service.list_invoices()[1][0]["status"] == "UNPAID"
    assert pay(service, "p1, 100", key="k")[0] == 201


# ---- 并发 ----

def run_threads(count, work):
    barrier = threading.Barrier(count)

    def worker(index):
        barrier.wait()
        return work(index)

    with ThreadPoolExecutor(count) as pool:
        return list(pool.map(worker, range(count)))


def test_concurrent_same_key_settles_exactly_once():
    service = service_with("A, 2026-01-01, 100", "B, 2026-01-02, 100")
    results = run_threads(64, lambda _: pay(service, "p1, 100", key="k"))
    assert sorted(status for status, _ in results) == [200] * 63 + [201]
    assert all(body == results[0][1] for _, body in results)
    assert statuses(service) == {"A": ("PAID", "p1"), "B": ("UNPAID", None)}


def test_competing_payments_settle_an_invoice_at_most_once():
    service = service_with("A, 2026-01-01, 100")
    results = run_threads(48, lambda i: pay(service, f"p{i}, 100"))
    assert sorted(status for status, _ in results) == [200] * 47 + [201]
    assert sum(1 for _, body in results if body["status"] == "MATCHED") == 1
    assert list(statuses(service).values())[0][0] == "PAID"


def test_concurrent_payments_use_every_invoice_exactly_once():
    service = impl.ReconciliationService()
    service.register_invoices([f"I{i:02d}, 2026-01-{i + 1:02d}, 100" for i in range(30)])
    results = run_threads(30, lambda i: pay(service, f"p{i}, 100"))
    assert {body["settled_invoice_id"] for _, body in results} == {f"I{i:02d}" for i in range(30)}
    assert sorted(payer for _, payer in statuses(service).values()) == sorted(f"p{i}" for i in range(30))


def test_concurrent_batches_are_equivalent_to_some_serial_order():
    service = impl.ReconciliationService()
    service.register_invoices([f"I{i:02d}, 2026-02-{i + 1:02d}, 100" for i in range(16)])
    run_threads(8, lambda i: service.reconcile_batch([{"payment": f"b{i}a, 100"}, {"payment": f"b{i}b, 100"}]))
    owner = {inv: payer for inv, (_, payer) in statuses(service).items()}
    pairs = [(owner[f"I{2 * k:02d}"], owner[f"I{2 * k + 1:02d}"]) for k in range(8)]
    # 每一批占用相邻的两张发票（先 a 后 b）：批次之间没有交错
    assert sorted(pairs) == [(f"b{i}a", f"b{i}b") for i in range(8)]


@pytest.fixture
def fast_switching():
    """让线程切换得很勤，半截状态才有机会被读到；用完恢复。"""
    old = sys.getswitchinterval()
    sys.setswitchinterval(1e-6)
    yield
    sys.setswitchinterval(old)


def test_readers_never_see_half_a_batch(fast_switching):
    service = service_with("X, 2026-01-01, 100", "Y, 2026-01-02, 200")
    stop = threading.Event()
    seen = []

    def reader():
        while not stop.is_set():
            seen.append(tuple(row["status"] for row in service.list_invoices()[1]))

    thread = threading.Thread(target=reader)
    thread.start()
    try:
        for _ in range(200):  # 每次都先结算 X、再因第二行畸形而整体回滚
            fails(400, "invalid_input", service.reconcile_batch, [{"payment": "p, 100"}, {"payment": "bad"}])
        service.reconcile_batch([{"payment": "p, 100"}, {"payment": "q, 200"}])
    finally:
        stop.set()
        thread.join()
    assert seen
    assert set(seen) <= {("UNPAID", "UNPAID"), ("PAID", "PAID")}
