import random

import pytest


def _brute_top_k(events, k):
    users_by_tag = {}
    for user, tag in events:
        users_by_tag.setdefault(tag, set()).add(user)
    ranked = sorted(users_by_tag.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    return [(t, len(u)) for t, u in ranked[:k]]


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example_part1(impl):
    events = [("u1", "snow"), ("u2", "snow"), ("u1", "cloud"), ("u3", "snow"), ("u2", "cloud"), ("u4", "data")]
    assert impl.top_k_hashtags(events, 2) == [("snow", 3), ("cloud", 2)]


@pytest.mark.part1
@pytest.mark.edge
def test_dedupes_same_user_same_tag(impl):
    assert impl.top_k_hashtags([("u1", "a"), ("u1", "a"), ("u1", "a")], 5) == [("a", 1)]


@pytest.mark.part1
@pytest.mark.edge
def test_tie_break_by_tag_ascending(impl):
    events = [("u1", "z"), ("u1", "a")]  # both popularity 1
    assert impl.top_k_hashtags(events, 2) == [("a", 1), ("z", 1)]


@pytest.mark.part1
@pytest.mark.edge
def test_k_zero_and_k_larger_than_tags(impl):
    events = [("u1", "a"), ("u2", "b")]
    assert impl.top_k_hashtags(events, 0) == []
    assert impl.top_k_hashtags(events, 10) == [("a", 1), ("b", 1)]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_events(impl):
    assert impl.top_k_hashtags([], 3) == []


@pytest.mark.part1
@pytest.mark.edge
def test_negative_k_raises(impl):
    with pytest.raises(ValueError):
        impl.top_k_hashtags([("u", "a")], -1)


@pytest.mark.part1
@pytest.mark.edge
def test_agrees_with_brute_force_random(impl):
    rng = random.Random(0)
    for _ in range(200):
        n = rng.randint(0, 40)
        events = [(f"u{rng.randint(0,5)}", f"t{rng.randint(0,4)}") for _ in range(n)]
        k = rng.randint(0, 6)
        assert impl.top_k_hashtags(events, k) == _brute_top_k(events, k), (events, k)


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_worked_example_part2(impl):
    c = impl.HashtagCounter()
    c.add("u1", "snow")
    assert c.top(2) == [("snow", 1)]
    c.add("u2", "snow")
    assert c.top(2) == [("snow", 2)]
    c.add("u1", "cloud")
    assert c.top(2) == [("snow", 2), ("cloud", 1)]


@pytest.mark.part2
@pytest.mark.edge
def test_streaming_dedupes(impl):
    c = impl.HashtagCounter()
    c.add("u1", "a")
    c.add("u1", "a")
    c.add("u1", "a")
    assert c.top(5) == [("a", 1)]


@pytest.mark.part2
@pytest.mark.edge
def test_streaming_top_zero(impl):
    c = impl.HashtagCounter()
    c.add("u1", "a")
    assert c.top(0) == []


@pytest.mark.part2
@pytest.mark.edge
def test_streaming_negative_k_raises(impl):
    c = impl.HashtagCounter()
    with pytest.raises(ValueError):
        c.top(-1)


@pytest.mark.part2
def test_streaming_matches_batch_random(impl):
    rng = random.Random(1)
    c = impl.HashtagCounter()
    events = []
    for _ in range(100):
        user, tag = f"u{rng.randint(0,6)}", f"t{rng.randint(0,4)}"
        c.add(user, tag)
        events.append((user, tag))
        if rng.random() < 0.2:
            k = rng.randint(0, 5)
            assert c.top(k) == impl.top_k_hashtags(events, k)


# ------------------------------------------------------------------------ Part 3
WINDOW_EVENTS = [
    (1, "u1", "snow"), (2, "u2", "snow"), (100, "u3", "snow"),
    (101, "u1", "cloud"), (102, "u4", "cloud"), (103, "u5", "cloud"),
]


@pytest.mark.part3
def test_worked_example_part3(impl):
    assert impl.top_k_hashtags_windowed(WINDOW_EVENTS, 2, 10) == [("cloud", 3), ("snow", 1)]
    assert impl.top_k_hashtags_windowed(WINDOW_EVENTS, 2, 1000) == [("cloud", 3), ("snow", 3)]


@pytest.mark.part3
@pytest.mark.edge
def test_unsorted_events_still_correct(impl):
    shuffled = list(reversed(WINDOW_EVENTS))
    assert impl.top_k_hashtags_windowed(shuffled, 2, 10) == [("cloud", 3), ("snow", 1)]


@pytest.mark.part3
@pytest.mark.edge
def test_window_zero_keeps_only_max_ts(impl):
    result = impl.top_k_hashtags_windowed(WINDOW_EVENTS, 5, 0)
    assert result == [("cloud", 1)]  # only ts == 103 -> u5, cloud


@pytest.mark.part3
@pytest.mark.edge
def test_user_counts_once_per_tag_in_window(impl):
    events = [(1, "u1", "a"), (2, "u1", "a"), (3, "u1", "a")]
    assert impl.top_k_hashtags_windowed(events, 5, 100) == [("a", 1)]


@pytest.mark.part3
@pytest.mark.edge
def test_empty_events_returns_empty(impl):
    assert impl.top_k_hashtags_windowed([], 3, 10) == []


@pytest.mark.part3
@pytest.mark.edge
def test_negative_k_or_window_raises(impl):
    with pytest.raises(ValueError):
        impl.top_k_hashtags_windowed(WINDOW_EVENTS, -1, 10)
    with pytest.raises(ValueError):
        impl.top_k_hashtags_windowed(WINDOW_EVENTS, 2, -1)


@pytest.mark.part3
def test_windowed_agrees_with_brute_force_random(impl):
    rng = random.Random(2)
    for _ in range(150):
        n = rng.randint(1, 30)
        events = [(rng.randint(0, 50), f"u{rng.randint(0,5)}", f"t{rng.randint(0,4)}") for _ in range(n)]
        k = rng.randint(0, 5)
        window = rng.randint(0, 60)
        max_ts = max(e[0] for e in events)
        cutoff = max_ts - window
        filtered = [(u, t) for ts, u, t in events if ts >= cutoff]
        assert impl.top_k_hashtags_windowed(events, k, window) == _brute_top_k(filtered, k), (events, k, window)


# ------------------------------------------------------------------------ perf / io
@pytest.mark.part1
@pytest.mark.perf
def test_perf_many_events(run_script):
    rng = random.Random(0)
    n = 100_000
    lines = [f"u{rng.randint(0,999)},tag{rng.randint(0,199)}" for _ in range(n)]
    body = "\n".join(lines)
    stdin = f"PART 1\nN {n}\n{body}\nK 5\n"
    r = run_script(stdin, timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    body = "\n".join(["u1,snow", "u2,snow", "u1,cloud", "u3,snow", "u2,cloud", "u4,data"])
    r = run_script(f"PART 1\nN 6\n{body}\nK 2\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "snow 3\ncloud 2\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    body = "\n".join(["ADD u1,snow", "TOP 2", "ADD u2,snow", "TOP 2", "ADD u1,cloud"])
    r = run_script(f"PART 2\nN 5\n{body}\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "Q 1\nsnow 1\nQ 1\nsnow 2\n"


@pytest.mark.part3
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part3(run_script):
    body = "\n".join(["1,u1,snow", "2,u2,snow", "100,u3,snow", "101,u1,cloud", "102,u4,cloud", "103,u5,cloud"])
    r = run_script(f"PART 3\nN 6\n{body}\nK 2 W 10\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "cloud 3\nsnow 1\n"
