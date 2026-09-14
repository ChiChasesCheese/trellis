import random

import pytest


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example(impl):
    out = impl.part1(["BEST 2 3 a 5 b 7 c 7", "BEST 2 1 a 10"])
    assert out == ["b c", "a b"]


@pytest.mark.part1
def test_class_api_directly(impl):
    t = impl.BookSalesTracker()
    assert t.best_sellers(["a", "b", "c"], [5, 7, 7], 2) == ["b", "c"]
    assert t.best_sellers(["a"], [10], 2) == ["a", "b"]


@pytest.mark.part1
@pytest.mark.edge
def test_k_zero_or_negative_returns_empty(impl):
    t = impl.BookSalesTracker()
    t.best_sellers(["a"], [5], 1)
    assert t.best_sellers([], [], 0) == []
    assert t.best_sellers([], [], -3) == []


@pytest.mark.part1
@pytest.mark.edge
def test_k_larger_than_book_count_returns_all(impl):
    t = impl.BookSalesTracker()
    t.best_sellers(["a", "b"], [1, 2], 2)
    assert t.best_sellers([], [], 10) == ["b", "a"]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_update_is_pure_query(impl):
    t = impl.BookSalesTracker()
    t.best_sellers(["a"], [5], 1)
    assert t.best_sellers([], [], 1) == ["a"]


@pytest.mark.part1
@pytest.mark.edge
def test_duplicate_book_in_same_call_merges_before_applying(impl):
    t = impl.BookSalesTracker()
    assert t.best_sellers(["a", "a", "b"], [3, 4, 5], 2) == ["a", "b"]  # a: 3+4=7 > b: 5


@pytest.mark.part1
@pytest.mark.edge
def test_tie_on_total_breaks_alphabetically(impl):
    t = impl.BookSalesTracker()
    assert t.best_sellers(["zebra", "apple", "mango"], [5, 5, 5], 3) == ["apple", "mango", "zebra"]


# ------------------------------------------------------------------------ Part 2 (efficiency)
@pytest.mark.part2
def test_lazy_heap_repeated_updates_stay_correct(impl):
    t = impl.BookSalesTracker()
    for _ in range(50):
        t.best_sellers(["a"], [1], 1)
    for _ in range(30):
        t.best_sellers(["b"], [1], 1)
    assert t.best_sellers([], [], 1) == ["a"]  # a: 50 > b: 30


@pytest.mark.part2
def test_random_cross_check_against_naive_model(impl):
    """Cross-check the (presumably heap-backed) implementation against a trivial dict + full sort
    on the same random update/query sequence."""
    rng = random.Random(0)
    t = impl.BookSalesTracker()
    naive: dict[str, int] = {}
    names = [f"b{i}" for i in range(15)]

    for _ in range(500):
        if rng.random() < 0.7:
            book = rng.choice(names)
            delta = rng.randint(1, 20)
            t.best_sellers([book], [delta], 1)
            naive[book] = naive.get(book, 0) + delta
        else:
            k = rng.randint(1, len(names))
            got = t.best_sellers([], [], k)
            expected = [
                name for name, _ in sorted(naive.items(), key=lambda kv: (-kv[1], kv[0]))
            ][:k]
            assert got == expected


@pytest.mark.part2
@pytest.mark.perf
def test_perf_100000_updates_10000_queries(run_script):
    rng = random.Random(0)
    names = [f"book{i}" for i in range(2000)]
    lines = ["PART 2"]
    for i in range(100_000):
        lines.append(f"BEST 1 1 {rng.choice(names)} {rng.randint(1, 5)}")
    for i in range(10_000):
        lines.append(f"BEST 10 0")
    r = run_script("\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"
    assert r.max_rss_mb < 256


# ------------------------------------------------------------------------ Part 3 (refunds, rank)
@pytest.mark.part3
def test_worked_example_refund_and_rank(impl):
    out = impl.part3(
        ["BEST 1 1 a 15", "BEST 1 1 a -100", "BEST 1 1 a -15", "RANK a", "RANK zzz"]
    )
    assert out == ["a", "ERROR", "a", "1", "-"]


@pytest.mark.part3
@pytest.mark.edge
def test_refund_to_exact_zero_is_allowed(impl):
    t = impl.BookSalesTracker()
    t.best_sellers(["a"], [10], 1)
    assert t.best_sellers(["a"], [-10], 1) == ["a"]  # a is the only known book, total is 0


@pytest.mark.part3
@pytest.mark.edge
def test_refund_below_zero_raises_and_has_no_side_effect(impl):
    t = impl.BookSalesTracker()
    t.best_sellers(["a"], [10], 1)
    with pytest.raises(ValueError):
        t.best_sellers(["a"], [-11], 1)
    assert t.rank("a") == 1
    assert t.best_sellers([], [], 1) == ["a"]  # still 10, unaffected by the rejected call


@pytest.mark.part3
@pytest.mark.edge
def test_batch_refund_all_or_nothing_across_multiple_books(impl):
    t = impl.BookSalesTracker()
    t.best_sellers(["a", "b"], [5, 5], 2)
    with pytest.raises(ValueError):
        # a would go to 2 (fine) but b would go to -1 (invalid) -- the WHOLE call must be
        # rejected, including a's otherwise-valid change.
        t.best_sellers(["a", "b"], [-3, -6], 2)
    assert t.rank("a") == 1  # unchanged: a and b tie at 5, a wins alphabetically
    assert t.rank("b") == 2


@pytest.mark.part3
@pytest.mark.edge
def test_rank_unknown_book_raises_key_error(impl):
    t = impl.BookSalesTracker()
    t.best_sellers(["a"], [1], 1)
    with pytest.raises(KeyError):
        t.rank("ghost")


@pytest.mark.part3
@pytest.mark.edge
def test_rank_matches_best_sellers_ordering(impl):
    t = impl.BookSalesTracker()
    t.best_sellers(["a", "b", "c", "d"], [10, 20, 20, 5], 4)
    assert t.rank("b") == 1  # b, c tie at 20; b < c alphabetically
    assert t.rank("c") == 2
    assert t.rank("a") == 3
    assert t.rank("d") == 4


# ------------------------------------------------------------------------ fmt / io
@pytest.mark.part1
@pytest.mark.fmt
def test_output_space_joined_and_dash_when_empty(impl):
    assert impl.part1(["BEST 3 0"]) == ["-"]
    assert impl.part1(["BEST 1 1 a 1"]) == ["a"]


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\nBEST 2 3 a 5 b 7 c 7\nBEST 2 1 a 10\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "b c\na b\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_part3(run_script):
    r = run_script(
        "PART 3\nBEST 1 1 a 15\nBEST 1 1 a -100\nBEST 1 1 a -15\nRANK a\nRANK zzz\n"
    )
    assert r.returncode == 0, r.stderr
    assert r.stdout == "a\nERROR\na\n1\n-\n"
