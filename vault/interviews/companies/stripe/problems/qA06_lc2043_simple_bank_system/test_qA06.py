import random
import time

import pytest

LC_INIT = [10, 100, 20, 50, 30]


def run_lc(bank):
    return [bank.withdraw(3, 10), bank.transfer(5, 1, 20), bank.deposit(5, 20), bank.transfer(3, 4, 15), bank.withdraw(10, 50)]


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_lc_example(impl):
    b = impl.Bank(LC_INIT)
    assert run_lc(b) == [True, True, True, False, False]
    assert b.balances() == [30, 100, 10, 50, 30]


@pytest.mark.part1
@pytest.mark.edge
def test_account_index_boundaries(impl):
    b = impl.Bank([5, 5])
    assert b.deposit(0, 1) is False and b.deposit(3, 1) is False and b.deposit(-1, 1) is False
    assert b.withdraw(0, 1) is False and b.withdraw(3, 1) is False
    assert b.transfer(1, 3, 1) is False and b.transfer(0, 1, 1) is False
    assert b.balances() == [5, 5]  # nothing moved, in particular the source of the failed transfer
    assert b.deposit(1, 1) is True and b.deposit(2, 1) is True and b.balances() == [6, 6]


@pytest.mark.part1
@pytest.mark.edge
def test_withdraw_exact_balance_and_zero(impl):
    b = impl.Bank([10])
    assert b.withdraw(1, 11) is False
    assert b.withdraw(1, 10) is True and b.balances() == [0]
    assert b.withdraw(1, 1) is False
    assert b.withdraw(1, 0) is True and b.deposit(1, 0) is True and b.balances() == [0]


@pytest.mark.part1
@pytest.mark.edge
def test_transfer_self_and_insufficient(impl):
    b = impl.Bank([10, 0])
    assert b.transfer(1, 1, 10) is True and b.balances() == [10, 0]
    assert b.transfer(1, 1, 11) is False
    assert b.transfer(2, 1, 1) is False and b.balances() == [10, 0]
    assert b.transfer(1, 2, 10) is True and b.balances() == [0, 10]


@pytest.mark.part1
@pytest.mark.edge
def test_large_integers_no_overflow(impl):
    b = impl.Bank([10**12] * 3)
    for _ in range(10_000):
        assert b.deposit(2, 10**12)
    assert b.balances()[1] == 10**12 + 10_000 * 10**12
    assert b.transfer(2, 1, 10**16) is True
    assert b.balances()[0] == 10**12 + 10**16


@pytest.mark.part1
def test_random_against_model(impl):
    rng = random.Random(0)
    for _ in range(50):
        n = rng.randrange(1, 5)
        init = [rng.randrange(0, 20) for _ in range(n)]
        b, model = impl.Bank(init), list(init)
        for _ in range(30):
            op = rng.choice(["deposit", "withdraw", "transfer"])
            a, c, m = rng.randrange(0, n + 2), rng.randrange(0, n + 2), rng.randrange(0, 15)
            if op == "deposit":
                exp = 1 <= a <= n
                if exp:
                    model[a - 1] += m
                assert b.deposit(a, m) is exp
            elif op == "withdraw":
                exp = 1 <= a <= n and model[a - 1] >= m
                if exp:
                    model[a - 1] -= m
                assert b.withdraw(a, m) is exp
            else:
                exp = 1 <= a <= n and 1 <= c <= n and model[a - 1] >= m
                if exp:
                    model[a - 1] -= m
                    model[c - 1] += m
                assert b.transfer(a, c, m) is exp
            assert b.balances() == model


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_log_records_lc_sequence(impl):
    b = impl.Bank(LC_INIT)
    run_lc(b)
    assert [r.id for r in b.log] == [1, 2, 3, 4, 5]
    assert [r.ok for r in b.log] == [True, True, True, False, False]
    assert [r.kind for r in b.log] == ["withdraw", "transfer", "deposit", "transfer", "withdraw"]
    assert b.log[1].src == 5 and b.log[1].dst == 1 and b.log[1].amount == 20 and b.log[1].ref is None


@pytest.mark.part2
def test_reversal_example(impl):
    b = impl.Bank(LC_INIT)
    run_lc(b)
    assert b.reverse(2) is True and b.balances() == [10, 100, 10, 50, 50]
    assert b.reverse(2) is False           # already reversed
    assert b.reverse(4) is False           # original was not ok
    assert b.reverse(6) is False           # id 6 is the reverse record itself
    assert b.reverse(1) is True and b.balances() == [10, 100, 20, 50, 50]
    assert b.reverse(99) is False and b.reverse(0) is False
    assert len(b.log) == 12  # 5 LC calls + 7 reverse attempts, failed ones included
    assert b.log[5].kind == "reverse" and b.log[5].ref == 2 and b.log[5].ok is True
    assert b.reversed_ids == {1, 2}


@pytest.mark.part2
@pytest.mark.edge
def test_reversal_must_be_fundable(impl):
    b = impl.Bank([5])
    assert b.deposit(1, 5) is True and b.withdraw(1, 8) is True and b.balances() == [2]
    assert b.reverse(1) is False and b.balances() == [2]       # undoing the deposit needs 5
    assert b.reverse(2) is True and b.balances() == [10]       # undoing the withdraw credits 8
    assert b.reverse(1) is True and b.balances() == [5]        # now fundable
    # transfer reversal needs the funds at dst
    b = impl.Bank([10, 0])
    assert b.transfer(1, 2, 10) is True and b.withdraw(2, 4) is True
    assert b.reverse(1) is False and b.balances() == [0, 6]
    assert b.deposit(2, 4) is True and b.reverse(1) is True and b.balances() == [10, 0]


@pytest.mark.part2
@pytest.mark.edge
def test_reverse_records_failed_attempts_too(impl):
    b = impl.Bank([1])
    assert b.reverse(1) is False
    assert len(b.log) == 1 and b.log[0].kind == "reverse" and b.log[0].ok is False and b.log[0].ref == 1
    assert b.reversed_ids == set()


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_lending_example(impl):
    b = impl.Bank([10, 100], reserve=50)
    assert b.withdraw(1, 30) is True and b.balances() == [0, 100] and b.reserve == 30 and b.debts() == [20, 0]
    assert b.withdraw(1, 40) is False and b.reserve == 30
    assert b.deposit(1, 25) is True and b.balances() == [5, 100] and b.reserve == 50 and b.debts() == [0, 0]
    assert b.transfer(1, 2, 15) is True
    assert b.balances() == [0, 115] and b.reserve == 40 and b.debts() == [10, 0]
    assert b.max_outstanding == 20


@pytest.mark.part3
@pytest.mark.edge
def test_lending_boundaries(impl):
    b = impl.Bank([0], reserve=10)
    assert b.withdraw(1, 10) is True and b.reserve == 0 and b.debts() == [10]   # shortfall == reserve
    assert b.withdraw(1, 1) is False                                             # reserve exhausted
    assert b.deposit(1, 3) is True and b.balances() == [0] and b.reserve == 3 and b.debts() == [7]
    assert b.deposit(1, 100) is True and b.balances() == [93] and b.reserve == 10 and b.debts() == [0]
    assert b.max_outstanding == 10
    # reserve=0 behaves exactly like Part 1
    b0 = impl.Bank(LC_INIT)
    assert run_lc(b0) == [True, True, True, False, False] and b0.reserve == 0 and b0.debts() == [0] * 5


@pytest.mark.part3
@pytest.mark.edge
def test_reversal_never_borrows_but_repays(impl):
    b = impl.Bank([0, 0], reserve=10)
    assert b.withdraw(1, 6) is True and b.debts() == [6, 0]
    assert b.deposit(2, 5) is True
    assert b.reverse(2) is True and b.balances() == [0, 0]     # plain debit, funded
    assert b.reverse(2) is False
    assert b.reverse(1) is True                                # credits 6 back -> repays the debt
    assert b.balances() == [0, 0] and b.debts() == [0, 0] and b.reserve == 10
    b = impl.Bank([0, 3], reserve=10)
    assert b.transfer(2, 1, 3) is True and b.withdraw(1, 3) is True
    assert b.reverse(1) is False                               # dst has 0; no loan for reversals
    assert b.balances() == [0, 0] and b.reserve == 10


@pytest.mark.part3
def test_incoming_transfer_repays_and_max_outstanding_peaks(impl):
    b = impl.Bank([0, 50, 0], reserve=100)
    assert b.withdraw(1, 30) and b.withdraw(3, 40)              # debts 30 + 40 = 70 outstanding
    assert b.max_outstanding == 70 and b.reserve == 30
    assert b.transfer(2, 1, 50) is True                         # repays 30, 20 lands
    assert b.balances() == [20, 0, 0] and b.debts() == [0, 0, 40] and b.reserve == 60
    assert b.max_outstanding == 70


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_all_parts(run_script):
    lc = "10 100 20 50 30\nwithdraw 3 10\ntransfer 5 1 20\ndeposit 5 20\ntransfer 3 4 15\nwithdraw 10 50\n"
    r = run_script("PART 1\n" + lc)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "true\ntrue\ntrue\nfalse\nfalse\nbalances 30 100 10 50 30\n"
    r = run_script("PART 2\n" + lc + "reverse 2\nreverse 2\n")
    assert r.stdout == "true\ntrue\ntrue\nfalse\nfalse\ntrue\nfalse\nbalances 10 100 10 50 50\n"
    r = run_script("PART 3\n10 100\nRESERVE 50\nwithdraw 1 30\nwithdraw 1 40\ndeposit 1 25\ntransfer 1 2 15\n\n")
    assert r.stdout == "true\nfalse\ntrue\ntrue\nbalances 0 115\nreserve 40\ndebts 10 0\nmax_outstanding 20\n"
    assert run_script("").stdout == ""


@pytest.mark.part1
@pytest.mark.perf
def test_perf_lc_max(impl, run_script):
    rng = random.Random(0)
    n = 100_000
    init = [rng.randrange(0, 10**12) for _ in range(n)]
    ops = []
    for _ in range(10_000):
        op = rng.choice(["deposit", "withdraw", "transfer"])
        if op == "transfer":
            ops.append(f"transfer {rng.randrange(1, n + 1)} {rng.randrange(1, n + 1)} {rng.randrange(0, 10**12)}")
        else:
            ops.append(f"{op} {rng.randrange(1, n + 1)} {rng.randrange(0, 10**12)}")
    t0 = time.perf_counter()
    b = impl.Bank(init)
    for c in ops:
        name, *args = c.split()
        getattr(b, name)(*map(int, args))
    assert time.perf_counter() - t0 < 2.0
    r = run_script("PART 1\n" + " ".join(map(str, init)) + "\n" + "\n".join(ops) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == 10_001
    assert r.seconds < 2.0 and r.max_rss_mb < 256
