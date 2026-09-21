import asyncio

import pytest


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example_part1(impl):
    lines = ["3", "a,b", "c", "d,e"]
    assert impl.part1(lines) == ["a", "b", "c", "d", "e"]


@pytest.mark.part1
@pytest.mark.edge
def test_part1_empty_page_does_not_shift_alignment(impl):
    # page 1 is empty ('-'), page 2 has one item -- output must still be just that one item,
    # not lose page 2 or misread it as page 1's content.
    assert impl.part1(["2", "-", "x"]) == ["x"]


@pytest.mark.part1
@pytest.mark.edge
def test_part1_single_page(impl):
    assert impl.part1(["1", "only"]) == ["only"]


@pytest.mark.part1
@pytest.mark.edge
def test_part1_calls_are_strictly_sequential(impl):
    """No two fetch_page calls are ever in flight at once, and they happen in page order."""
    order: list[int] = []
    in_flight = 0
    max_in_flight = 0

    async def fetch_page(page):
        nonlocal in_flight, max_in_flight
        order.append(page)
        in_flight += 1
        max_in_flight = max(max_in_flight, in_flight)
        await asyncio.sleep(0.01)
        in_flight -= 1
        return {"items": [f"p{page}"], "total_pages": 3}

    items = asyncio.run(impl.fetch_all_sequential(fetch_page))
    assert order == [1, 2, 3]
    assert max_in_flight == 1
    assert items == ["p1", "p2", "p3"]


@pytest.mark.part1
@pytest.mark.edge
def test_part1_total_pages_invalid_raises(impl):
    async def fetch_page(page):
        return {"items": [], "total_pages": 0}

    with pytest.raises(ValueError):
        asyncio.run(impl.fetch_all_sequential(fetch_page))


@pytest.mark.part1
@pytest.mark.edge
def test_part1_page_line_count_mismatch_raises(impl):
    with pytest.raises(ValueError):
        impl.part1(["3", "a", "b"])  # declares 3 pages, gives 2


@pytest.mark.part1
@pytest.mark.io
def test_part1_io(run_script):
    r = run_script("PART 1\n3\na,b\nc\nd,e\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "a\nb\nc\nd\ne\n"


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_worked_example_part2(impl):
    lines = ["4 2", "p1", "p2", "p3", "p4"]
    assert impl.part2(lines) == ["p1", "p2", "p3", "p4"]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_order_stable_under_variable_latency(impl):
    """Page 2 is deliberately the slowest and page 4 the fastest; output must still be page order."""
    pages = {1: ["p1"], 2: ["p2"], 3: ["p3"], 4: ["p4"]}
    delays = {1: 0.0, 2: 0.05, 3: 0.01, 4: 0.0}

    async def fetch_page(page):
        await asyncio.sleep(delays[page])
        return {"items": pages[page], "total_pages": 4}

    items = asyncio.run(impl.fetch_all_concurrent(fetch_page, max_concurrency=4))
    assert items == ["p1", "p2", "p3", "p4"]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_concurrency_is_bounded(impl):
    in_flight = 0
    max_in_flight = 0

    async def fetch_page(page):
        nonlocal in_flight, max_in_flight
        in_flight += 1
        max_in_flight = max(max_in_flight, in_flight)
        await asyncio.sleep(0.02)
        in_flight -= 1
        return {"items": [f"p{page}"], "total_pages": 10}

    items = asyncio.run(impl.fetch_all_concurrent(fetch_page, max_concurrency=3))
    assert max_in_flight == 3
    assert items == [f"p{i}" for i in range(1, 11)]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_max_concurrency_invalid_raises(impl):
    async def fetch_page(page):
        return {"items": [], "total_pages": 1}

    with pytest.raises(ValueError):
        asyncio.run(impl.fetch_all_concurrent(fetch_page, max_concurrency=0))


@pytest.mark.part2
@pytest.mark.edge
def test_part2_matches_sequential_result(impl):
    pages = {p: [f"item{p}-{i}" for i in range(3)] for p in range(1, 13)}

    async def fetch_page(page):
        return {"items": pages[page], "total_pages": 12}

    sequential = asyncio.run(impl.fetch_all_sequential(fetch_page))
    concurrent = asyncio.run(impl.fetch_all_concurrent(fetch_page, max_concurrency=5))
    assert concurrent == sequential


@pytest.mark.part2
@pytest.mark.perf
def test_part2_perf_200_pages_bounded_concurrency(impl):
    import time

    async def fetch_page(page):
        await asyncio.sleep(0.01)
        return {"items": [f"p{page}"], "total_pages": 200}

    t0 = time.perf_counter()
    items = asyncio.run(impl.fetch_all_concurrent(fetch_page, max_concurrency=50))
    elapsed = time.perf_counter() - t0

    assert len(items) == 200
    assert elapsed < 2.0, f"took {elapsed:.2f}s"


@pytest.mark.part2
@pytest.mark.io
def test_part2_io(run_script):
    r = run_script("PART 2\n4 2\np1\np2\np3\np4\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "p1\np2\np3\np4\n"


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
def test_worked_example_part3(impl):
    lines = ["2 2 3", "a,b|0", "b,c|2"]
    assert impl.part3(lines) == ["a", "b", "c"]


@pytest.mark.part3
@pytest.mark.edge
def test_part3_retries_exhausted_raises(impl):
    attempts = {"n": 0}

    async def fetch_page(page):
        attempts["n"] += 1
        raise impl.TransientError("always fails")

    async def fast_sleep(_seconds):
        return None

    with pytest.raises(impl.TransientError):
        asyncio.run(
            impl.fetch_all_with_retry(
                fetch_page, max_concurrency=1, max_retries=2, base_delay=0.0, sleep=fast_sleep
            )
        )
    assert attempts["n"] == 3  # 1 initial try + 2 retries


@pytest.mark.part3
@pytest.mark.edge
def test_part3_retry_succeeds_within_budget(impl):
    attempts = {"n": 0}

    async def fetch_page(page):
        attempts["n"] += 1
        if attempts["n"] <= 2:
            raise impl.TransientError("flaky")
        return {"items": ["ok"], "total_pages": 1}

    async def fast_sleep(_seconds):
        return None

    items = asyncio.run(
        impl.fetch_all_with_retry(
            fetch_page, max_concurrency=1, max_retries=2, base_delay=0.0, sleep=fast_sleep
        )
    )
    assert items == ["ok"]
    assert attempts["n"] == 3


@pytest.mark.part3
@pytest.mark.edge
def test_part3_non_transient_exception_not_retried(impl):
    sleep_calls = []

    async def fetch_page(page):
        raise RuntimeError("not a TransientError")

    async def spy_sleep(seconds):
        sleep_calls.append(seconds)

    with pytest.raises(RuntimeError):
        asyncio.run(
            impl.fetch_all_with_retry(
                fetch_page, max_concurrency=1, max_retries=5, base_delay=1.0, sleep=spy_sleep
            )
        )
    assert sleep_calls == []


@pytest.mark.part3
@pytest.mark.edge
def test_part3_exponential_backoff_delays(impl):
    sleep_calls: list[float] = []
    attempts = {"n": 0}

    async def fetch_page(page):
        attempts["n"] += 1
        if attempts["n"] <= 2:
            raise impl.TransientError("flaky")
        return {"items": ["ok"], "total_pages": 1}

    async def spy_sleep(seconds):
        sleep_calls.append(seconds)

    asyncio.run(
        impl.fetch_all_with_retry(
            fetch_page, max_concurrency=1, max_retries=3, base_delay=1.0, sleep=spy_sleep
        )
    )
    assert sleep_calls == [1.0, 2.0]  # base_delay * 2**0, base_delay * 2**1


@pytest.mark.part3
@pytest.mark.edge
def test_part3_dedup_preserves_first_seen_order(impl):
    pages = {1: ["a", "b"], 2: ["b", "c"], 3: ["c", "d"]}

    async def fetch_page(page):
        return {"items": pages[page], "total_pages": 3}

    async def fast_sleep(_seconds):
        return None

    items = asyncio.run(
        impl.fetch_all_with_retry(
            fetch_page, max_concurrency=3, max_retries=0, base_delay=0.0, sleep=fast_sleep
        )
    )
    assert items == ["a", "b", "c", "d"]


@pytest.mark.part3
@pytest.mark.edge
@pytest.mark.parametrize("bad_kwargs", [{"max_concurrency": 0}, {"max_retries": -1}])
def test_part3_invalid_arguments_raise(impl, bad_kwargs):
    async def fetch_page(page):
        return {"items": [], "total_pages": 1}

    async def fast_sleep(_seconds):
        return None

    kwargs = {"max_concurrency": 1, "max_retries": 1, "base_delay": 0.0, "sleep": fast_sleep}
    kwargs.update(bad_kwargs)
    with pytest.raises(ValueError):
        asyncio.run(impl.fetch_all_with_retry(fetch_page, **kwargs))


@pytest.mark.part3
@pytest.mark.io
def test_part3_io(run_script):
    r = run_script("PART 3\n2 2 3\na,b|0\nb,c|2\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "a\nb\nc\n"
