import time

import pytest


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_part1_worked_example_line_driven(impl):
    lines = ["MEMO 2 3", "MEMO 2 3", "MEMO 5 1", "MEMO CALLS", "TIMED 4"]
    assert impl.part1(lines) == ["5", "5", "6", "2", "16"]


@pytest.mark.part1
def test_memoize_worked_example(impl):
    calls = []

    @impl.memoize
    def add(x, y=1):
        calls.append((x, y))
        return x + y

    assert add(1, 2) == 3
    assert add(1, 2) == 3  # cache hit: no new call recorded
    assert add(2, y=3) == 5
    assert add(2, y=3) == 5
    assert calls == [(1, 2), (2, 3)]
    assert (add.hits, add.misses) == (2, 2)


@pytest.mark.part1
def test_timed_worked_example(impl):
    @impl.timed
    def square(x):
        return x * x

    assert square(4) == 16
    assert square.last_seconds >= 0.0
    assert square(5) == 25
    assert square.last_seconds >= 0.0  # updates on every call, not just the first


@pytest.mark.part1
@pytest.mark.edge
def test_wraps_preserves_metadata_timed_and_memoize(impl):
    def base(x):
        """base docstring."""
        return x

    for deco in (impl.timed, impl.memoize):
        wrapped = deco(base)
        assert wrapped.__name__ == "base"
        assert wrapped.__doc__ == "base docstring."


@pytest.mark.part1
@pytest.mark.edge
def test_memoize_distinguishes_args_and_kwargs(impl):
    # the cache key is the raw (args, kwargs) shape, not the bound signature -- f(5), f(5, 0)
    # and f(5, b=0) are three distinct cache entries even though they compute the same value.
    calls = []

    @impl.memoize
    def f(a, b=0):
        calls.append((a, b))
        return a - b

    assert f(5) == 5
    assert f(5, 0) == 5
    assert f(5, b=0) == 5
    assert len(calls) == 3
    assert (f.hits, f.misses) == (0, 3)
    # repeating the exact same call shape is the only thing that hits the cache
    assert f(5) == 5
    assert (f.hits, f.misses) == (1, 3)


@pytest.mark.part1
@pytest.mark.edge
def test_memoize_cache_clear_resets_counts_and_forces_recompute(impl):
    calls = []

    @impl.memoize
    def f(x):
        calls.append(x)
        return x

    f(1)
    f(1)
    assert (f.hits, f.misses) == (1, 1)
    f.cache_clear()
    assert (f.hits, f.misses) == (0, 0)
    f(1)
    assert calls == [1, 1]  # recomputed after clear
    assert f.misses == 1


@pytest.mark.part1
@pytest.mark.io
def test_part1_io(run_script):
    r = run_script("PART 1\nMEMO 2 3\nMEMO 2 3\nMEMO 5 1\nMEMO CALLS\nTIMED 4\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "5\n5\n6\n2\n16\n"
    r_empty = run_script("PART 1\n")
    assert r_empty.returncode == 0, r_empty.stderr
    assert r_empty.stdout == ""


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_part2_worked_examples_line_driven(impl):
    lines = ["RETRY 3 2", "RETRY 3 5"]
    assert impl.part2(lines) == ["ok 3", "error ValueError 3"]


@pytest.mark.part2
@pytest.mark.fmt
def test_part2_error_output_format_exact(impl):
    # fail_times > times: exhausts all `times` attempts, format is 'error <ExcType> <attempts>'
    out = impl.part2(["RETRY 1 1"])
    assert out == ["error ValueError 1"]


@pytest.mark.part2
@pytest.mark.edge
def test_retry_exhausts_and_reraises_original_exception(impl):
    flaky = impl.make_flaky(5)
    wrapped = impl.retry(3, exceptions=(ValueError,))(flaky)
    with pytest.raises(ValueError, match="transient failure #3"):
        wrapped()
    assert wrapped.attempts == 3


@pytest.mark.part2
@pytest.mark.edge
def test_retry_times_must_be_positive(impl):
    with pytest.raises(ValueError):
        impl.retry(0)
    with pytest.raises(ValueError):
        impl.retry(-1)


@pytest.mark.part2
@pytest.mark.edge
def test_retry_backoff_and_sleep_called_with_increasing_attempt(impl):
    sleep_calls = []
    flaky = impl.make_flaky(2)
    wrapped = impl.retry(
        3, exceptions=(ValueError,), backoff=lambda attempt: attempt * 0.1, sleep=sleep_calls.append
    )(flaky)
    assert wrapped() == "ok"
    assert wrapped.attempts == 3
    assert sleep_calls == [0.1, 0.2]  # sleeps after attempt 1 and attempt 2, not after success


@pytest.mark.part2
@pytest.mark.edge
def test_retry_non_matching_exception_propagates_immediately_no_retry(impl):
    calls = []

    def boom():
        calls.append(1)
        raise TypeError("not retried")

    wrapped = impl.retry(5, exceptions=(ValueError,))(boom)
    with pytest.raises(TypeError):
        wrapped()
    assert len(calls) == 1  # never retried: TypeError is not in `exceptions`


@pytest.mark.part2
@pytest.mark.io
def test_part2_io(run_script):
    r = run_script("PART 2\nRETRY 3 2\nRETRY 3 5\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "ok 3\nerror ValueError 3\n"


@pytest.mark.part2
@pytest.mark.perf
def test_part2_perf_many_retry_calls(impl):
    wrapped = impl.retry(3)(lambda: "ok")
    t0 = time.perf_counter()
    for _ in range(200_000):
        wrapped()
    elapsed = time.perf_counter() - t0
    assert elapsed < 2.0, f"took {elapsed:.2f}s"


# ------------------------------------------------------------------------ Part 3 (reconstructed)
@pytest.mark.part3
def test_part3_worked_example_line_driven(impl):
    lines = ["LIMIT 3 10", "CALL 0", "CALL 1", "CALL 2", "CALL 3", "CALL 11"]
    assert impl.part3(lines) == ["ok", "ok", "ok", "limited", "ok"]


@pytest.mark.part3
@pytest.mark.edge
def test_rate_limited_window_slides_after_expiry(impl):
    t = [0.0]
    wrapped = impl.rate_limited(1, 10, clock=lambda: t[0])(lambda: "ok")
    assert wrapped() == "ok"  # t=0, window now full (capacity 1)
    t[0] = 9
    with pytest.raises(impl.RateLimitExceeded):
        wrapped()  # t=9: age is 9 < 10, still inside the window
    t[0] = 10
    assert wrapped() == "ok"  # t=10: age is exactly 10 >= per_seconds -> evicted, window reopens


@pytest.mark.part3
@pytest.mark.edge
def test_rate_limited_invalid_params_raise(impl):
    with pytest.raises(ValueError):
        impl.rate_limited(0, 10)
    with pytest.raises(ValueError):
        impl.rate_limited(3, 0)
    with pytest.raises(ValueError):
        impl.rate_limited(3, -1)


@pytest.mark.part3
@pytest.mark.edge
def test_rate_limited_preserves_metadata(impl):
    @impl.rate_limited(2, 5)
    def greet():
        """greet docstring."""
        return "hi"

    assert greet.__name__ == "greet"
    assert greet.__doc__ == "greet docstring."


@pytest.mark.part3
@pytest.mark.io
def test_part3_io(run_script):
    r = run_script("PART 3\nLIMIT 3 10\nCALL 0\nCALL 1\nCALL 2\nCALL 3\nCALL 11\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "ok\nok\nok\nlimited\nok\n"


@pytest.mark.part3
@pytest.mark.perf
def test_part3_perf_many_calls(impl):
    t = [0.0]
    wrapped = impl.rate_limited(1000, 1.0, clock=lambda: t[0])(lambda: "ok")
    t0 = time.perf_counter()
    ok_count = 0
    for i in range(200_000):
        t[0] = i * 0.00001  # 20 "seconds" of simulated time spread over 200k calls
        try:
            wrapped()
            ok_count += 1
        except impl.RateLimitExceeded:
            pass
    elapsed = time.perf_counter() - t0
    assert elapsed < 2.0, f"took {elapsed:.2f}s"
    assert ok_count == 2000  # 1000 calls/sec cap * ~2s of simulated time actually admitted
