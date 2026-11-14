from __future__ import annotations

import json
import time
from pathlib import Path

import pytest

DATA = Path(__file__).resolve().parent / "data"
PATTERNS = {k: [tuple(p) for p in v] for k, v in json.loads((DATA / "patterns.json").read_text()).items()}


def replay(impl, path: Path) -> list[list[str]]:
    """Run scenario.txt; return the payloads of every `take`, in order."""
    q, takes = impl.MessageQueue(), []
    for line in path.read_text().splitlines():
        parts = line.split()
        if not parts or parts[0].startswith("#"):
            continue
        op, args = parts[0], parts[1:]
        if op == "add":
            q.add_channel(args[0])
        elif op == "sub":
            q.subscribe(args[0], args[1])
        elif op == "unsub":
            q.unsubscribe(args[0], args[1])
        elif op == "pub":
            q.enqueue(args[0], args[1].split(","), args[2])
        elif op == "take":
            n = int(args[1]) if len(args) > 1 else None
            takes.append([m.payload for m in q.consume(args[0], n)])
    return q, takes


def exact_ok(pairs, blocks) -> bool:
    """Every wanted pair is covered and no block delivers an unwanted pair."""
    covered = {(p, c) for ps, cs in blocks for p in ps for c in cs}
    return covered == set(pairs)


# ---------------------------------------------------------------- Part 1: the queue


@pytest.mark.part1
def test_fan_out_once_per_consumer(impl):
    q = impl.MessageQueue(["a", "b", "c"])
    q.subscribe("x", "a")
    q.subscribe("x", "b")
    q.subscribe("y", "b")
    q.subscribe("z", "c")
    mid = q.enqueue("p", ["a", "b"], "hello")
    assert [m.payload for m in q.consume("x")] == ["hello"]  # on both tags, gets it once
    (m,) = q.consume("y")
    assert (m.id, m.producer, m.channels) == (mid, "p", frozenset({"a", "b"}))
    assert q.consume("z") == []


@pytest.mark.part1
def test_fifo_and_partial_consume(impl):
    q = impl.MessageQueue(["a"])
    q.subscribe("x", "a")
    ids = [q.enqueue("p", ["a"], i) for i in range(5)]
    assert ids == sorted(ids) and len(set(ids)) == 5
    assert [m.payload for m in q.consume("x", 2)] == [0, 1]
    assert q.pending("x") == 3
    assert [m.payload for m in q.consume("x", 10)] == [2, 3, 4]
    assert q.consume("x") == [] and q.pending("x") == 0


@pytest.mark.part1
def test_only_messages_after_subscribing(impl):
    q = impl.MessageQueue(["a"])
    q.enqueue("p", ["a"], "early")
    q.subscribe("x", "a")
    q.enqueue("p", ["a"], "late")
    assert [m.payload for m in q.consume("x")] == ["late"]


@pytest.mark.part1
def test_unsubscribe_stops_new_messages_keeps_old(impl):
    q = impl.MessageQueue(["a", "b"])
    q.subscribe("x", "a")
    q.subscribe("x", "b")
    q.enqueue("p", ["a"], 1)
    q.unsubscribe("x", "a")
    q.enqueue("p", ["a"], 2)
    q.enqueue("p", ["b"], 3)
    assert [m.payload for m in q.consume("x")] == [1, 3]
    assert q.subscriptions("x") == {"b"}
    q.unsubscribe("x", "a")  # again: no-op


@pytest.mark.part1
def test_add_channel_at_runtime(impl):
    q = impl.MessageQueue(["a"])
    q.subscribe("x", "a")
    assert q.add_channel("b") == 1 and q.add_channel("c") == 2
    q.subscribe("x", "c")
    q.enqueue("p", ["c"], "new")
    assert q.subscriptions("x") == {"a", "c"}
    assert [m.payload for m in q.consume("x")] == ["new"]


@pytest.mark.part1
def test_masks_and_shared_channels(impl):
    q = impl.MessageQueue(["a", "b", "c", "d"])
    assert q.channel_mask(["a", "c"]) == 0b0101
    q.subscribe("x", "a")
    q.subscribe("x", "c")
    q.subscribe("y", "c")
    q.subscribe("y", "d")
    q.enqueue("p", ["a", "b"], None)
    assert q.shared_channels("x", "y") == {"c"}
    assert q.shared_channels("p", "x") == {"a"}  # a producer's channels = where it has published
    assert q.shared_channels("p", "y") == set()
    assert q.shared_channels("x", "nobody") == set()


@pytest.mark.part1
def test_bits_to_names(impl):
    assert impl.bits_to_names(0b1011, ["a", "b", "c", "d"]) == {"a", "b", "d"}
    assert impl.bits_to_names(0, ["a"]) == set()


@pytest.mark.part1
def test_scenario_replay(impl):
    _, takes = replay(impl, DATA / "scenario.txt")
    assert takes == [["mmlu-drop-2pt"], ["mmlu-drop-2pt"], ["p99-up"], ["disk-80pct"], ["build-1041-green"],
                     ["p99-up"]]


# ---------------------------------------------------------------- Part 2: union-find groups


@pytest.mark.part2
def test_union_find_basics(impl):
    uf = impl.UnionFind()
    assert uf.union(1, 2) and uf.union(3, 4) and uf.union(2, 4)
    assert not uf.union(1, 3)  # already together
    assert uf.find(1) == uf.find(4)
    assert uf.find(5) == 5  # unseen element is its own set
    assert uf.size[uf.find(1)] == 4


@pytest.mark.part2
def test_groups_are_transitive(impl):
    got = impl.groups({"p1": ["a"], "c1": ["a", "b"], "p2": ["b"], "c2": ["z"], "p3": ["z"], "lonely": []})
    assert got == [["c1", "p1", "p2"], ["c2", "p3"]]


@pytest.mark.part2
def test_channel_named_like_a_participant(impl):
    assert impl.groups({"x": ["y"], "y": ["q"]}) == [["x"], ["y"]]


@pytest.mark.part2
def test_share_groups_on_live_queue_after_unsubscribe(impl):
    q, _ = replay(impl, DATA / "scenario.txt")
    assert q.share_groups() == [["archive", "ci"], ["bench", "dash", "evalbot", "pager", "perf-bot", "watchdog"]]
    q.unsubscribe("dash", "evals")  # dash was the only bridge between the evals side and the perf side
    assert q.share_groups() == [["archive", "ci"], ["bench", "dash", "perf-bot"], ["evalbot", "pager", "watchdog"]]


@pytest.mark.part2
@pytest.mark.perf
def test_union_find_long_chain_is_fast(impl):
    uf = impl.UnionFind()
    t0 = time.perf_counter()
    for i in range(200_000):
        uf.union(i, i + 1)
    assert uf.find(0) == uf.find(200_000)
    assert time.perf_counter() - t0 < 3


# ---------------------------------------------------------------- Part 3: fewest channels with isolation


@pytest.mark.part3
@pytest.mark.parametrize("name,expected", [("one_team", 1), ("two_teams", 2), ("chain", 1), ("matching", 4),
                                           ("full_block", 1), ("crown_3", 1)])
def test_min_channels(impl, name, expected):
    assert impl.min_channels(PATTERNS[name]) == expected


@pytest.mark.part3
def test_plan_is_valid_and_isolated(impl):
    pairs = PATTERNS["two_teams"]
    plan = impl.plan_channels(pairs)
    assert all(plan[p] == plan[c] for p, c in pairs)  # every pair shares a channel
    assert plan["ci"] != plan["bench"]  # unrelated teams never share
    assert set(plan) == {x for pair in pairs for x in pair}


@pytest.mark.part3
def test_plan_works_on_the_queue(impl):
    pairs = PATTERNS["two_teams"]
    plan = impl.plan_channels(pairs)
    q = impl.MessageQueue(sorted(set(plan.values())))
    for _, c in pairs:
        q.subscribe(c, plan[c])
    for p in {p for p, _ in pairs}:
        q.enqueue(p, [plan[p]], f"from {p}")
    assert {m.payload for m in q.consume("perfbot")} == {"from bench"}
    assert {m.payload for m in q.consume("pager")} == {"from ci"}


# ---------------------------------------------------------------- Part 4: exact delivery (stretch)


@pytest.mark.part4
@pytest.mark.parametrize("name,expected", [("one_team", 2), ("two_teams", 2), ("chain", 3), ("matching", 4),
                                           ("full_block", 1), ("crown_3", 3)])
def test_min_channels_exact(impl, name, expected):
    blocks = impl.min_channels_exact(PATTERNS[name])
    assert len(blocks) == expected
    assert exact_ok(PATTERNS[name], blocks)


# ---------------------------------------------------------------- edge cases


@pytest.mark.edge
def test_errors(impl):
    q = impl.MessageQueue(["a"])
    with pytest.raises(ValueError):
        q.add_channel("a")
    with pytest.raises(KeyError):
        q.subscribe("x", "nope")
    with pytest.raises(KeyError):
        q.enqueue("p", ["a", "nope"], 1)
    with pytest.raises(ValueError):
        q.enqueue("p", [], 1)


@pytest.mark.edge
def test_failed_enqueue_changes_nothing(impl):
    q = impl.MessageQueue(["a"])
    q.subscribe("x", "a")
    with pytest.raises(KeyError):
        q.enqueue("p", ["a", "nope"], 1)
    assert q.pending("x") == 0 and q.shared_channels("p", "x") == set()


@pytest.mark.edge
def test_unknown_consumer_and_empty_inputs(impl):
    q = impl.MessageQueue()
    assert q.consume("ghost") == [] and q.pending("ghost") == 0 and q.subscriptions("ghost") == set()
    assert q.share_groups() == []
    assert impl.min_channels([]) == 0 and impl.min_channels_exact([]) == []
    assert impl.groups({}) == []
