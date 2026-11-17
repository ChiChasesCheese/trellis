import importlib
import os
import random

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

MAX_SAFE = 2**53 - 1
AMOUNT_LIMIT = 1_000_000_000


@pytest.fixture
def path(tmp_path):
    return str(tmp_path / "ledger.db")


@pytest.fixture
def db(path):
    connection = impl.open_database(path)
    yield connection
    connection.close()


def reopen(connection, path):
    connection.close()
    return impl.open_database(path)


# ---- 开工前定下的规则：新账户、序列、缺失 ----


def test_first_account_is_one_with_zero_balance(db):
    assert impl.create_account(db) == impl.Account(1, 0)


def test_account_ids_count_up_by_one(db):
    assert [impl.create_account(db).id for _ in range(4)] == [1, 2, 3, 4]


def test_unknown_account_lookup_is_none_not_error(db):
    impl.create_account(db)
    for missing in (0, -1, 2, 10**6, MAX_SAFE):
        assert impl.get_account(db, missing) is None


def test_existing_account_without_payments_is_zero_not_none(db):
    account = impl.create_account(db)
    found = impl.get_account(db, account.id)
    assert found == impl.Account(1, 0)
    assert type(found.balance) is int


def test_payment_for_missing_account_is_none(db):
    assert impl.create_payment(db, 1, 500) is None
    account = impl.create_account(db)
    assert impl.create_payment(db, account.id + 1, 500) is None


def test_missing_account_payment_consumes_no_id_and_changes_nothing(db):
    account = impl.create_account(db)
    for _ in range(3):
        assert impl.create_payment(db, 77, 900) is None
    first = impl.create_payment(db, account.id, 40)
    assert first == impl.Payment(1, 1, 40)
    assert impl.get_account(db, account.id) == impl.Account(1, 40)
    assert impl.get_account(db, 77) is None


# ---- 余额：求和、正负、零、隔离 ----


def test_balance_sums_positive_and_negative_amounts(db):
    account = impl.create_account(db)
    for amount in (1200, -300, 50, -950):
        impl.create_payment(db, account.id, amount)
    assert impl.get_account(db, account.id) == impl.Account(1, 0 + 1200 - 300 + 50 - 950)


def test_balance_may_go_negative_without_overdraft_check(db):
    account = impl.create_account(db)
    assert impl.create_payment(db, account.id, -700) == impl.Payment(1, 1, -700)
    assert impl.get_account(db, account.id).balance == -700


def test_zero_payment_is_a_record_and_advances_the_sequence(db):
    account = impl.create_account(db)
    assert impl.create_payment(db, account.id, 0) == impl.Payment(1, 1, 0)
    assert impl.create_payment(db, account.id, 0) == impl.Payment(2, 1, 0)
    assert impl.create_payment(db, account.id, 5) == impl.Payment(3, 1, 5)
    assert impl.get_account(db, account.id).balance == 5


def test_identical_submissions_make_two_records(db):
    account = impl.create_account(db)
    one = impl.create_payment(db, account.id, 250)
    two = impl.create_payment(db, account.id, 250)
    assert (one.id, two.id) == (1, 2)
    assert impl.get_account(db, account.id).balance == 500


def test_accounts_are_independent_and_payment_ids_are_global(db):
    a, b = impl.create_account(db), impl.create_account(db)
    assert impl.create_payment(db, a.id, 100) == impl.Payment(1, 1, 100)
    assert impl.create_payment(db, b.id, 30) == impl.Payment(2, 2, 30)
    assert impl.create_payment(db, a.id, -40) == impl.Payment(3, 1, -40)
    assert impl.get_account(db, a.id).balance == 60
    assert impl.get_account(db, b.id).balance == 30


def test_account_and_payment_sequences_are_separate(db):
    a = impl.create_account(db)
    for _ in range(3):
        impl.create_payment(db, a.id, 1)
    assert impl.create_account(db).id == 2
    assert impl.create_payment(db, 2, 1).id == 4


def test_readme_walkthrough_with_own_amounts(db):
    assert impl.create_account(db) == impl.Account(1, 0)
    assert impl.create_payment(db, 1, 700) == impl.Payment(1, 1, 700)
    assert impl.create_payment(db, 1, 1300) == impl.Payment(2, 1, 1300)
    assert impl.get_account(db, 1) == impl.Account(1, 2000)
    assert impl.create_account(db) == impl.Account(2, 0)


# ---- 持久化与隔离 ----


def test_reopen_keeps_accounts_payments_and_balances(db, path):
    a, b = impl.create_account(db), impl.create_account(db)
    impl.create_payment(db, a.id, 900)
    impl.create_payment(db, a.id, -150)
    db = reopen(db, path)
    assert impl.get_account(db, a.id) == impl.Account(1, 750)
    assert impl.get_account(db, b.id) == impl.Account(2, 0)
    db.close()


def test_reopen_keeps_both_id_sequences_going(db, path):
    a = impl.create_account(db)
    impl.create_payment(db, a.id, 10)
    impl.create_payment(db, a.id, 20)
    db = reopen(db, path)
    assert impl.create_payment(db, a.id, 30) == impl.Payment(3, 1, 30)
    assert impl.create_account(db).id == 2
    db.close()


def test_failed_payment_leaves_sequence_untouched_across_reopen(db, path):
    a = impl.create_account(db)
    assert impl.create_payment(db, 9, 1) is None
    db = reopen(db, path)
    assert impl.create_payment(db, a.id, 1).id == 1
    db.close()


def test_two_database_files_share_no_state(tmp_path):
    left = impl.open_database(str(tmp_path / "left.db"))
    right = impl.open_database(str(tmp_path / "right.db"))
    impl.create_account(left)
    impl.create_account(left)
    impl.create_payment(left, 2, 800)
    assert impl.create_account(right) == impl.Account(1, 0)
    assert impl.get_account(right, 2) is None
    assert impl.create_payment(right, 1, 5) == impl.Payment(1, 1, 5)
    assert impl.get_account(left, 2) == impl.Account(2, 800)
    left.close()
    right.close()


def test_functions_do_not_close_the_callers_connection(db):
    account = impl.create_account(db)
    impl.create_payment(db, account.id, 1)
    impl.create_payment(db, 99, 1)
    impl.get_account(db, 99)
    impl.get_account(db, account.id)
    assert db.execute("SELECT 1").fetchone() == (1,)


def test_second_connection_sees_committed_data(db, path):
    account = impl.create_account(db)
    impl.create_payment(db, account.id, 64)
    other = impl.open_database(path)
    assert impl.get_account(other, account.id) == impl.Account(1, 64)
    other.close()


def test_opened_connection_enforces_foreign_keys(db):
    import sqlite3
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("INSERT INTO payments (account_id, amount) VALUES (?, ?)", (41, 5))


# ---- 数值范围 ----


def test_amount_bounds_and_balance_beyond_32_bits_stay_exact_ints(db):
    account = impl.create_account(db)
    for _ in range(5):
        impl.create_payment(db, account.id, AMOUNT_LIMIT)
    for _ in range(2):
        impl.create_payment(db, account.id, -AMOUNT_LIMIT)
    balance = impl.get_account(db, account.id).balance
    assert balance == 3 * AMOUNT_LIMIT and type(balance) is int


def test_balance_at_the_safe_integer_limit_is_exact(db):
    account = impl.create_account(db)
    db.execute("INSERT INTO payments (account_id, amount) VALUES (?, ?)", (account.id, MAX_SAFE - 3))
    impl.create_payment(db, account.id, 3)
    found = impl.get_account(db, account.id)
    assert found.balance == MAX_SAFE and type(found.balance) is int
    impl.create_payment(db, account.id, -AMOUNT_LIMIT)
    assert impl.get_account(db, account.id).balance == MAX_SAFE - AMOUNT_LIMIT


def test_lookup_of_an_id_at_the_safe_limit_after_a_real_one(db):
    db.execute("INSERT INTO accounts (id) VALUES (?)", (MAX_SAFE,))
    assert impl.get_account(db, MAX_SAFE) == impl.Account(MAX_SAFE, 0)
    assert impl.create_payment(db, MAX_SAFE, -9) == impl.Payment(1, MAX_SAFE, -9)


# ---- 与独立模型对拍：不依赖任何一种查询写法 ----


@pytest.mark.parametrize("seed", [3, 11, 2024])
def test_random_operations_match_a_plain_python_model(path, seed):
    rng = random.Random(seed)
    db = impl.open_database(path)
    balances: dict[int, int] = {}
    next_payment = 1
    for step in range(250):
        roll = rng.random()
        if roll < 0.15:
            account = impl.create_account(db)
            assert account == impl.Account(len(balances) + 1, 0)
            balances[account.id] = 0
        elif roll < 0.65:
            target = rng.randint(0, len(balances) + 2)
            amount = rng.choice([0, rng.randint(-AMOUNT_LIMIT, AMOUNT_LIMIT), rng.randint(-500, 500)])
            result = impl.create_payment(db, target, amount)
            if target in balances:
                assert result == impl.Payment(next_payment, target, amount)
                balances[target] += amount
                next_payment += 1
            else:
                assert result is None
        elif roll < 0.95:
            target = rng.randint(0, len(balances) + 2)
            expected = None if target not in balances else impl.Account(target, balances[target])
            assert impl.get_account(db, target) == expected
        else:
            db = reopen(db, path)
    for account_id, balance in balances.items():
        assert impl.get_account(db, account_id) == impl.Account(account_id, balance)
    db.close()
