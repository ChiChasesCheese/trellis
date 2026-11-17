import importlib
import os
import random
import threading
from concurrent.futures import ThreadPoolExecutor

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))
ServiceError = impl.ServiceError

LOAN_KEYS = {"id", "borrower", "lender", "principal", "outstanding", "status"}


def make(**balances):
    return impl.LoanService(dict(balances))


def fails(status, code, fn, *args):
    with pytest.raises(ServiceError) as caught:
        fn(*args)
    assert (caught.value.status, caught.value.code) == (status, code)


def funded(principal=60, ann=0, bob=100):
    """一笔已放款的贷款：ann 借，bob 出。"""
    service = make(ann=ann, bob=bob, cat=0)
    loan = service.create("ann", principal)
    service.fund(loan["id"], "bob")
    return service, loan["id"]


def snapshot_of(service, loan_ids, users):
    return ([service.get(i) for i in loan_ids], {u: service.balance(u) for u in users})


# ---- 合同里的例子 ----

def test_contract_example_full_walkthrough():
    service = make(ann=0, bob=100)
    loan = service.create("ann", 60)
    assert service.fund(loan["id"], "bob") == {
        "id": 1, "borrower": "ann", "lender": "bob", "principal": 60, "outstanding": 60, "status": "active"}
    assert service.repay(loan["id"], "ann", 20)["outstanding"] == 40
    assert (service.balance("ann"), service.balance("bob")) == (40, 60)


def test_create_returns_exact_pending_shape_and_moves_no_money():
    service = make(ann=7, bob=50)
    loan = service.create("ann", 30)
    assert loan == {"id": 1, "borrower": "ann", "lender": None, "principal": 30, "outstanding": 30,
                    "status": "pending"}
    assert set(loan) == LOAN_KEYS
    assert (service.balance("ann"), service.balance("bob")) == (7, 50)


def test_created_loan_is_retrievable_by_its_returned_id():
    service = make(ann=0)
    first, second = service.create("ann", 5), service.create("ann", 9)
    assert (first["id"], second["id"]) == (1, 2)
    assert service.get(first["id"]) == first
    assert service.get(second["id"]) == second


# ---- 金额与用户的校验 ----

@pytest.mark.parametrize("bad", [0, -1, -10**20, True, False, 5.0, 2.5, "5", None, [5], (5,)])
def test_create_rejects_bad_amounts(bad):
    fails(400, "invalid_amount", make(ann=0).create, "ann", bad)


@pytest.mark.parametrize("bad", [0, -3, True, 1.0, "1", None])
def test_repay_rejects_bad_amounts_before_anything_else(bad):
    service, loan_id = funded()
    fails(400, "invalid_amount", service.repay, loan_id, "ann", bad)
    # 金额排在最前：贷款不存在、借款人不对时，也先报金额
    fails(400, "invalid_amount", service.repay, 99, "nobody", bad)


def test_create_checks_amount_before_borrower():
    fails(400, "invalid_amount", make(ann=0).create, "ghost", 0)
    fails(404, "user_not_found", make(ann=0).create, "ghost", 10)


def test_balance_of_unknown_user_is_404():
    service = make(ann=3)
    fails(404, "user_not_found", service.balance, "ghost")
    fails(404, "user_not_found", service.balance, None)
    fails(404, "user_not_found", service.balance, ["ann"])  # 不可哈希的值也不能变成 TypeError


def test_get_unknown_loan_is_404_and_ids_must_be_real_ints():
    service = make(ann=0)
    service.create("ann", 4)
    fails(404, "loan_not_found", service.get, 2)
    fails(404, "loan_not_found", service.get, 0)
    fails(404, "loan_not_found", service.get, True)  # True 与 1 哈希相同，不能误中第一笔
    fails(404, "loan_not_found", service.get, "1")
    fails(404, "loan_not_found", service.get, [1])


def test_huge_amounts_are_exact():
    big = 10**30
    service = make(ann=0, bob=big + 5)
    loan = service.create("ann", big)
    service.fund(loan["id"], "bob")
    assert service.repay(loan["id"], "ann", big - 1)["outstanding"] == 1
    assert (service.balance("ann"), service.balance("bob")) == (1, big + 4)


# ---- 编号只给成功的创建 ----

def test_failed_creates_do_not_consume_ids():
    service = make(ann=0)
    fails(400, "invalid_amount", service.create, "ann", -4)
    fails(404, "user_not_found", service.create, "ghost", 4)
    assert service.create("ann", 4)["id"] == 1
    fails(400, "invalid_amount", service.create, "ann", 0)
    assert service.create("ann", 4)["id"] == 2


# ---- 放款 ----

def test_fund_moves_principal_and_activates():
    service = make(ann=5, bob=100)
    loan = service.create("ann", 80)
    result = service.fund(loan["id"], "bob")
    assert result == {"id": 1, "borrower": "ann", "lender": "bob", "principal": 80, "outstanding": 80,
                      "status": "active"}
    assert service.get(1) == result
    assert (service.balance("ann"), service.balance("bob")) == (85, 20)


def test_fund_exact_balance_is_enough():
    service = make(ann=0, bob=80)
    loan = service.create("ann", 80)
    assert service.fund(loan["id"], "bob")["status"] == "active"
    assert service.balance("bob") == 0


def test_fund_one_cent_short_fails_and_changes_nothing():
    service = make(ann=1, bob=79)
    loan = service.create("ann", 80)
    fails(409, "insufficient_balance", service.fund, loan["id"], "bob")
    assert snapshot_of(service, [1], ["ann", "bob"]) == ([loan], {"ann": 1, "bob": 79})
    service2 = make(ann=0, bob=100)
    service2.create("ann", 80)
    assert service2.fund(1, "bob")["status"] == "active"  # 失败的那次没有把贷款卡住


def test_fund_check_order_loan_then_lender_then_state_then_balance():
    service = make(ann=0, bob=500, poor=1)
    loan = service.create("ann", 100)
    fails(404, "loan_not_found", service.fund, 99, "ghost")  # 贷款先于出借人
    fails(404, "user_not_found", service.fund, loan["id"], "ghost")
    fails(409, "invalid_state", service.fund, loan["id"], "ann")  # 自己借给自己：ann 余额为 0 也先报状态
    service.fund(loan["id"], "bob")
    fails(409, "invalid_state", service.fund, loan["id"], "poor")  # 已放款：穷出借人也先报状态
    fails(404, "user_not_found", service.fund, loan["id"], "ghost")  # 已放款：出借人不存在仍先于状态


def test_fund_by_the_borrower_is_rejected_even_when_rich():
    service = make(ann=1000)
    loan = service.create("ann", 10)
    fails(409, "invalid_state", service.fund, loan["id"], "ann")
    assert service.get(loan["id"])["status"] == "pending"
    assert service.balance("ann") == 1000


def test_a_loan_funds_only_once_even_for_the_same_lender():
    service = make(ann=0, bob=300, cat=300)
    loan = service.create("ann", 100)
    service.fund(loan["id"], "bob")
    fails(409, "invalid_state", service.fund, loan["id"], "bob")
    fails(409, "invalid_state", service.fund, loan["id"], "cat")
    assert (service.balance("ann"), service.balance("bob"), service.balance("cat")) == (100, 200, 300)
    assert service.get(loan["id"])["lender"] == "bob"


# ---- 还款 ----

def test_repay_partial_then_full():
    service, loan_id = funded(principal=90, ann=0, bob=100)
    part = service.repay(loan_id, "ann", 35)
    assert (part["outstanding"], part["status"]) == (55, "active")
    done = service.repay(loan_id, "ann", 55)
    assert (done["outstanding"], done["status"]) == (0, "repaid")
    assert (service.balance("ann"), service.balance("bob")) == (0, 100)


def test_repay_exact_balance_is_enough():
    service, loan_id = funded(principal=40, ann=0, bob=40)
    assert service.balance("ann") == 40
    assert service.repay(loan_id, "ann", 40)["status"] == "repaid"
    assert service.balance("ann") == 0


def test_repay_with_too_little_balance_fails_and_changes_nothing():
    service, loan_id = funded(principal=60, ann=0, bob=100)  # ann 现有 60，欠 60
    side = service.create("cat", 55)
    service.fund(side["id"], "ann")  # ann 把 55 借给 cat，只剩 5
    before = snapshot_of(service, [loan_id, side["id"]], ["ann", "bob", "cat"])
    fails(409, "insufficient_balance", service.repay, loan_id, "ann", 6)
    assert snapshot_of(service, [loan_id, side["id"]], ["ann", "bob", "cat"]) == before
    assert service.repay(loan_id, "ann", 5)["outstanding"] == 55  # 借款人仍然能还他付得起的数


def test_repay_check_order():
    service = make(ann=0, bob=100, cat=0)
    loan = service.create("ann", 50)
    fails(404, "loan_not_found", service.repay, 99, "ann", 5)
    fails(403, "forbidden", service.repay, loan["id"], "cat", 5)  # pending 的贷款：归属先于状态
    fails(409, "invalid_state", service.repay, loan["id"], "ann", 5)  # 归属对了，pending 不能还
    service.fund(loan["id"], "bob")
    fails(403, "forbidden", service.repay, loan["id"], "bob", 5)  # 出借人也不是借款人
    fails(403, "forbidden", service.repay, loan["id"], "ghost", 5)  # 不存在的用户同样是 403
    fails(409, "invalid_state", service.repay, loan["id"], "ann", 51)  # 超额
    service.repay(loan["id"], "ann", 50)
    fails(409, "invalid_state", service.repay, loan["id"], "ann", 1)  # 已结清


def test_overpayment_is_reported_before_insufficient_balance():
    service, loan_id = funded(principal=30, ann=0, bob=30)
    service.repay(loan_id, "ann", 25)  # ann 剩 5，欠 5
    fails(409, "invalid_state", service.repay, loan_id, "ann", 6)  # 6 既超额又付不起，先报状态


def test_repay_on_pending_loan_changes_nothing():
    service = make(ann=100, bob=100)
    loan = service.create("ann", 20)
    fails(409, "invalid_state", service.repay, loan["id"], "ann", 20)
    assert snapshot_of(service, [1], ["ann", "bob"]) == ([loan], {"ann": 100, "bob": 100})


# ---- 隔离 ----

def test_returned_snapshots_are_detached():
    service = make(ann=0, bob=100)
    created = service.create("ann", 50)
    created["status"] = "repaid"
    created["outstanding"] = 0
    assert service.get(1)["status"] == "pending"
    fetched = service.get(1)
    fetched["principal"] = 10**9
    fetched["borrower"] = "mallory"
    assert service.get(1)["principal"] == 50 and service.get(1)["borrower"] == "ann"
    funded_loan = service.fund(1, "bob")
    funded_loan["lender"] = "mallory"
    assert service.get(1)["lender"] == "bob"
    repaid = service.repay(1, "ann", 10)
    repaid["outstanding"] = -1
    assert service.get(1)["outstanding"] == 40


def test_each_call_returns_a_new_object():
    service = make(ann=0)
    service.create("ann", 5)
    assert service.get(1) is not service.get(1)
    assert service.get(1) == service.get(1)


def test_constructor_copies_the_balances():
    start = {"ann": 0, "bob": 100}
    service = impl.LoanService(start)
    start["bob"] = 0
    start["zed"] = 5
    assert service.balance("bob") == 100
    fails(404, "user_not_found", service.balance, "zed")
    loan = service.create("ann", 60)
    service.fund(loan["id"], "bob")
    assert start == {"ann": 0, "bob": 0, "zed": 5}  # 服务也没有回写调用方的字典


def test_total_balance_never_changes_through_the_lifecycle():
    service = make(ann=3, bob=100, cat=0)
    total = service.total_balance()
    assert total == 103
    loan = service.create("ann", 60)
    assert service.total_balance() == total
    service.fund(loan["id"], "bob")
    assert service.total_balance() == total
    service.repay(loan["id"], "ann", 25)
    service.repay(loan["id"], "ann", 35)
    assert service.total_balance() == total


def test_instances_are_independent():
    first, second = make(ann=0, bob=100), make(ann=0, bob=100)
    loan = first.create("ann", 70)
    first.fund(loan["id"], "bob")
    fails(404, "loan_not_found", second.get, 1)
    assert second.create("ann", 3)["id"] == 1
    assert (second.balance("ann"), second.balance("bob")) == (0, 100)


# ---- 并发 ----

def run_together(count, job):
    barrier = threading.Barrier(count)

    def worker(i):
        barrier.wait()
        try:
            return ("ok", job(i))
        except ServiceError as error:
            return ("err", (error.status, error.code))

    with ThreadPoolExecutor(max_workers=count) as pool:
        return list(pool.map(worker, range(count)))


def test_concurrent_funding_of_one_loan_succeeds_exactly_once():
    lenders = {f"l{i}": 100 for i in range(16)}
    service = make(ann=0, **lenders)
    loan = service.create("ann", 100)
    results = run_together(16, lambda i: service.fund(loan["id"], f"l{i}"))
    assert sum(1 for kind, _ in results if kind == "ok") == 1
    assert {value for kind, value in results if kind == "err"} == {(409, "invalid_state")}
    assert service.balance("ann") == 100
    assert sum(service.balance(name) for name in lenders) == 1500
    assert service.total_balance() == 1600
    winner = service.get(loan["id"])["lender"]
    assert service.balance(winner) == 0


def test_concurrent_funding_of_many_loans_never_overdraws_the_lender():
    service = make(ann=0, bob=100)
    ids = [service.create("ann", 30)["id"] for _ in range(10)]
    results = run_together(10, lambda i: service.fund(ids[i], "bob"))
    assert sum(1 for kind, _ in results if kind == "ok") == 3  # 100 // 30
    assert {value for kind, value in results if kind == "err"} == {(409, "insufficient_balance")}
    assert (service.balance("ann"), service.balance("bob")) == (90, 10)


def test_concurrent_repayments_never_exceed_outstanding():
    service, loan_id = funded(principal=100, ann=0, bob=100)
    results = run_together(20, lambda i: service.repay(loan_id, "ann", 10))
    assert sum(1 for kind, _ in results if kind == "ok") == 10
    assert {value for kind, value in results if kind == "err"} == {(409, "invalid_state")}
    assert service.get(loan_id)["status"] == "repaid"
    assert (service.balance("ann"), service.balance("bob")) == (0, 100)


def test_concurrent_creates_get_distinct_consecutive_ids():
    service = make(ann=0)
    results = run_together(32, lambda i: service.create("ann", i + 1)["id"])
    assert sorted(value for _, value in results) == list(range(1, 33))
    assert {service.get(i)["principal"] for i in range(1, 33)} == set(range(1, 33))


def test_random_operations_conserve_money_and_keep_balances_non_negative():
    rng = random.Random(20240601)
    users = ["u0", "u1", "u2", "u3", "u4"]
    service = make(**{u: rng.randrange(0, 200) for u in users})
    total = service.total_balance()
    for _ in range(600):
        action = rng.choice(["create", "fund", "repay"])
        try:
            if action == "create":
                service.create(rng.choice(users), rng.randrange(-5, 120))
            elif action == "fund":
                service.fund(rng.randrange(0, 40), rng.choice(users))
            else:
                service.repay(rng.randrange(0, 40), rng.choice(users), rng.randrange(-5, 120))
        except ServiceError:
            pass
        assert service.total_balance() == total
        assert min(service.balance(u) for u in users) >= 0
    for loan_id in range(1, 40):
        try:
            loan = service.get(loan_id)
        except ServiceError:
            break
        assert 0 <= loan["outstanding"] <= loan["principal"]
        assert (loan["status"] == "repaid") == (loan["outstanding"] == 0 and loan["lender"] is not None)
        assert (loan["lender"] is None) == (loan["status"] == "pending")
