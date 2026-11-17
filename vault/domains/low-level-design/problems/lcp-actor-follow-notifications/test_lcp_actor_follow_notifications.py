import dataclasses
import importlib
import os
import sys
import threading

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))
Notice = impl.Notice

# 合同点名的空白字符，在测试里单独列一遍（区间：09–0D、1C–20、1680、2000–2006、2008–200A、2028–2029、205F、3000）
BLANKS = (
    [chr(c) for c in range(0x09, 0x0E)]
    + [chr(c) for c in range(0x1C, 0x21)]
    + [" "]
    + [chr(c) for c in range(0x2000, 0x2007)]
    + [chr(c) for c in range(0x2008, 0x200B)]
    + [" ", " ", " ", "　"]
)
# 看起来像空白、但合同说是合法字符的：str.strip() 会把它们吃掉
NOT_BLANKS = [" ", "\u0085", " ", " ", "​", "﻿"]


@pytest.fixture(autouse=True)
def fast_thread_switching():
    """把线程切换间隔压到最小，让没加锁的"检查再动作"更容易在测试里露出来。"""
    old = sys.getswitchinterval()
    sys.setswitchinterval(1e-6)
    yield
    sys.setswitchinterval(old)


def make():
    return impl.NotificationService()


def run_threads(targets):
    """用屏障让所有目标函数同时起跑；返回按目标顺序排列的结果或异常。"""
    barrier = threading.Barrier(len(targets))
    results = [None] * len(targets)

    def worker(i, target):
        barrier.wait()
        try:
            results[i] = target()
        except BaseException as exc:  # noqa: BLE001 - 测试要把异常当结果收集
            results[i] = exc

    threads = [threading.Thread(target=worker, args=(i, t)) for i, t in enumerate(targets)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=30)
        assert not t.is_alive()
    return results


# ---- 合同给的示例 ----

def test_readme_example_and_idempotent_retry():
    service = make()
    service.follow("alice", "actor-1")
    assert service.add_movie("m1", "First film", ["actor-1"]) is True
    assert service.add_movie("m1", "First film", ["actor-1"]) is False
    assert service.inbox("alice") == [Notice("m1", "First film")]


def test_public_cases_follow_unfollow_empty():
    service = make()
    service.follow("dana", "star-7")
    service.add_movie("f9", "Harbour Lights", ["star-7", "star-8"])
    assert service.inbox("dana") == [Notice("f9", "Harbour Lights")]

    other = make()
    other.follow("alice", "actor-1")
    other.unfollow("alice", "actor-1")
    other.add_movie("m1", "Movie", ["actor-1"])
    assert other.inbox("alice") == []
    assert make().inbox("new-user") == []


def test_return_values_are_exact():
    service = make()
    assert service.follow("u", "a") is None
    assert service.unfollow("u", "a") is None
    assert service.add_movie("m", "t", []) is True
    assert service.add_movie("m", "t", []) is False


# ---- 关注与取关 ----

def test_unfollow_removes_only_that_relationship():
    service = make()
    for user, actor in [("alice", "a1"), ("alice", "a2"), ("bob", "a1")]:
        service.follow(user, actor)
    service.unfollow("alice", "a1")
    service.add_movie("m1", "t1", ["a1"])
    service.add_movie("m2", "t2", ["a2"])
    assert service.inbox("alice") == [Notice("m2", "t2")]
    assert service.inbox("bob") == [Notice("m1", "t1")]
    assert service.subscription_count == 2


def test_unfollow_of_absent_relationship_is_a_noop():
    service = make()
    service.unfollow("ghost", "a1")
    service.follow("alice", "a1")
    service.unfollow("alice", "other-actor")
    service.unfollow("bob", "a1")
    assert service.subscription_count == 1
    service.add_movie("m1", "t", ["a1"])
    assert service.inbox("alice") == [Notice("m1", "t")]


def test_duplicate_follow_is_a_noop():
    service = make()
    service.follow("alice", "a1")
    service.follow("alice", "a1")
    assert service.subscription_count == 1
    service.add_movie("m1", "t", ["a1"])
    assert service.inbox("alice") == [Notice("m1", "t")]
    service.unfollow("alice", "a1")
    assert service.subscription_count == 0


def test_following_never_backfills_and_unfollow_keeps_history():
    service = make()
    service.add_movie("old", "Old", ["a1"])
    service.follow("alice", "a1")
    assert service.inbox("alice") == []
    service.add_movie("new", "New", ["a1"])
    service.unfollow("alice", "a1")
    assert service.inbox("alice") == [Notice("new", "New")]


def test_empty_index_entries_are_dropped():
    service = make()
    for i in range(50):
        service.follow(f"u{i}", f"a{i % 5}")
    assert service.subscription_count == 50 and service.tracked_actor_count == 5
    for i in range(50):
        service.unfollow(f"u{i}", f"a{i % 5}")
    assert service.subscription_count == 0
    assert service.tracked_actor_count == 0


# ---- 谁收到通知 ----

def test_follower_of_several_cast_members_gets_exactly_one_notice():
    service = make()
    service.follow("alice", "a1")
    service.follow("alice", "a2")
    service.follow("alice", "a3")
    service.add_movie("m1", "t", ["a1", "a2", "a1", "a2", "a3"])
    assert service.inbox("alice") == [Notice("m1", "t")]


def test_only_followers_of_the_cast_are_notified_and_empty_cast_notifies_nobody():
    service = make()
    service.follow("alice", "a1")
    service.follow("bob", "a9")
    service.follow("carol", "a1")
    service.add_movie("m1", "t", ["a1", "a2"])
    assert service.inbox("alice") == [Notice("m1", "t")]
    assert service.inbox("carol") == [Notice("m1", "t")]
    assert service.inbox("bob") == []
    assert service.add_movie("m2", "t2", []) is True
    assert service.inbox("alice") == [Notice("m1", "t")]
    assert service.inbox("bob") == []


def test_ids_are_case_sensitive_and_kept_exactly():
    service = make()
    service.follow("Alice", "Actor")
    service.follow(" alice", "actor")
    service.add_movie("M1", "t", ["Actor"])
    assert service.inbox("Alice") == [Notice("M1", "t")]
    assert service.inbox(" alice") == []
    assert service.inbox("alice") == []
    service.add_movie("m1", "t", [])
    assert service.movie_count == 2


# ---- 重复导入与冲突 ----

def test_repeated_import_is_a_noop_even_if_followers_changed():
    service = make()
    service.follow("alice", "a1")
    assert service.add_movie("m1", "t", ["a1"]) is True
    service.follow("bob", "a1")
    assert service.add_movie("m1", "t", ["a1"]) is False
    assert service.inbox("alice") == [Notice("m1", "t")]
    assert service.inbox("bob") == []


def test_cast_order_and_duplication_do_not_matter_for_equality():
    service = make()
    assert service.add_movie("m1", "t", ["a", "b", "c"]) is True
    assert service.add_movie("m1", "t", ["c", "a", "b", "a", "c"]) is False
    assert service.add_movie("e", "t", []) is True
    assert service.add_movie("e", "t", []) is False


def test_conflict_raises_and_changes_nothing():
    service = make()
    service.follow("alice", "a1")
    service.follow("bob", "a2")
    service.add_movie("m1", "Title", ["a1"])
    for title, cast in [("Other", ["a1"]), ("Title", ["a1", "a2"]), ("Title", []), ("Other", ["a2"])]:
        with pytest.raises(RuntimeError, match="^movie_conflict$"):
            service.add_movie("m1", title, cast)
    assert service.inbox("alice") == [Notice("m1", "Title")]
    assert service.inbox("bob") == []
    assert service.movie_count == 1
    # 记录没被冲突的导入改写：原来的内容仍然是"重复导入"
    assert service.add_movie("m1", "Title", ["a1"]) is False


def test_title_comparison_is_exact():
    service = make()
    service.add_movie("m1", "Title", [])
    for other in ["title", "Title ", " Title"]:
        with pytest.raises(RuntimeError):
            service.add_movie("m1", other, [])


# ---- 收件箱：顺序与快照 ----

def test_inbox_keeps_insertion_order_not_id_order():
    service = make()
    service.follow("alice", "a1")
    for movie_id in ["z", "a", "m", "B"]:
        service.add_movie(movie_id, f"title-{movie_id}", ["a1"])
    assert [n.movie_id for n in service.inbox("alice")] == ["z", "a", "m", "B"]


def test_inbox_returns_an_independent_snapshot():
    service = make()
    service.follow("alice", "a1")
    service.add_movie("m1", "t1", ["a1"])
    first = service.inbox("alice")
    first.append(Notice("fake", "fake"))
    first.clear()
    assert service.inbox("alice") == [Notice("m1", "t1")]
    snapshot = service.inbox("alice")
    service.add_movie("m2", "t2", ["a1"])
    assert snapshot == [Notice("m1", "t1")]
    assert service.inbox("alice") == [Notice("m1", "t1"), Notice("m2", "t2")]


def test_notice_is_immutable():
    service = make()
    service.follow("alice", "a1")
    service.add_movie("m1", "t1", ["a1"])
    notice = service.inbox("alice")[0]
    with pytest.raises(dataclasses.FrozenInstanceError):
        notice.title = "changed"
    assert service.inbox("alice")[0].title == "t1"


def test_unknown_user_gets_a_fresh_empty_list_each_time():
    service = make()
    first = service.inbox("nobody")
    first.append(Notice("x", "x"))
    assert service.inbox("nobody") == []


def test_input_cast_is_snapshotted_at_call_time():
    service = make()
    cast = ["a1"]
    service.add_movie("m1", "t", cast)
    cast.append("a2")
    assert service.add_movie("m1", "t", ["a1"]) is False
    with pytest.raises(RuntimeError):
        service.add_movie("m1", "t", ["a1", "a2"])


def test_instances_are_independent():
    one, two = make(), make()
    one.follow("alice", "a1")
    one.add_movie("m1", "t", ["a1"])
    assert two.inbox("alice") == []
    assert two.add_movie("m1", "different", ["a9"]) is True


# ---- 输入校验 ----

BAD_IDS = [None, 1, 1.5, True, b"x", ("a",), ["a"], "", " ", "\t\n", "　　"]


@pytest.mark.parametrize("bad", BAD_IDS)
def test_invalid_ids_raise_before_any_state_change(bad):
    service = make()
    service.follow("alice", "a1")
    with pytest.raises(ValueError, match="^invalid_input$"):
        service.follow(bad, "a1")
    with pytest.raises(ValueError, match="^invalid_input$"):
        service.follow("alice", bad)
    with pytest.raises(ValueError, match="^invalid_input$"):
        service.unfollow(bad, "a1")
    with pytest.raises(ValueError, match="^invalid_input$"):
        service.unfollow("alice", bad)
    with pytest.raises(ValueError, match="^invalid_input$"):
        service.add_movie(bad, "t", ["a1"])
    with pytest.raises(ValueError, match="^invalid_input$"):
        service.add_movie("m1", bad, ["a1"])
    with pytest.raises(ValueError, match="^invalid_input$"):
        service.add_movie("m1", "t", ["a1", bad])
    with pytest.raises(ValueError, match="^invalid_input$"):
        service.inbox(bad)
    assert service.subscription_count == 1
    assert service.movie_count == 0
    assert service.add_movie("m1", "t", ["a1"]) is True
    assert service.inbox("alice") == [Notice("m1", "t")]


@pytest.mark.parametrize("bad", [None, ("a1",), {"a1"}, "a1", (a for a in ["a1"]), 5])
def test_actors_must_be_a_list(bad):
    service = make()
    with pytest.raises(ValueError, match="^invalid_input$"):
        service.add_movie("m1", "t", bad)
    assert service.movie_count == 0


def test_every_listed_blank_character_is_blank():
    service = make()
    for ch in BLANKS:
        for text in (ch, ch * 3):
            with pytest.raises(ValueError):
                service.follow(text, "a1")
    assert service.subscription_count == 0


def test_lookalike_characters_are_valid_and_kept_exactly():
    service = make()
    for ch in NOT_BLANKS:
        service.follow(ch, ch)
        service.follow(f"{ch} ", ch)
        assert service.add_movie(f"id{ch}", ch, [ch]) is True
        assert service.inbox(ch) == [Notice(f"id{ch}", ch)]
        assert service.inbox(f"{ch} ") == [Notice(f"id{ch}", ch)]
    # 首尾夹着空白字符的标识符也合法，原样保存
    service.follow(" a 　", "x")
    assert service.add_movie("m", "t", ["x"]) is True
    assert service.inbox(" a 　") == [Notice("m", "t")]
    assert service.inbox("a") == []


def test_validation_wins_over_conflict_and_leaves_state_intact():
    service = make()
    service.follow("alice", "a1")
    service.add_movie("m1", "t", ["a1"])
    with pytest.raises(ValueError):
        service.add_movie("m1", " ", ["a1"])
    with pytest.raises(ValueError):
        service.add_movie("m1", "other", ["a1", None])
    assert service.add_movie("m1", "t", ["a1"]) is False
    assert service.inbox("alice") == [Notice("m1", "t")]


def test_large_duplicated_cast_is_fine():
    service = make()
    service.follow("alice", "a1")
    assert service.add_movie("m1", "t", ["a1"] * 10_000) is True
    assert service.inbox("alice") == [Notice("m1", "t")]
    assert service.add_movie("m1", "t", ["a1"]) is False


# ---- 并发 ----

def test_concurrent_identical_imports_one_true_one_notice_per_follower():
    service = make()
    users = [f"u{i}" for i in range(10)]
    for u in users:
        service.follow(u, "a1")
        service.follow(u, "a2")
    rounds = 40
    for r in range(rounds):
        results = run_threads([lambda r=r: service.add_movie(f"m{r}", "t", ["a1", "a2"])] * 32)
        assert results.count(True) == 1
        assert results.count(False) == 31
    expected = [Notice(f"m{r}", "t") for r in range(rounds)]
    for u in users:
        assert service.inbox(u) == expected


def test_concurrent_conflicting_imports_exactly_one_wins_and_nothing_leaks():
    service = make()
    for u in ("alice", "bob"):
        service.follow(u, "a1")
    titles = [f"title-{i}" for i in range(8)]
    results = run_threads([lambda t=t: service.add_movie("m1", t, ["a1"]) for t in titles])
    winners = [i for i, r in enumerate(results) if r is True]
    assert len(winners) == 1
    for i, r in enumerate(results):
        if i != winners[0]:
            assert isinstance(r, RuntimeError) and str(r) == "movie_conflict"
    expected = [Notice("m1", titles[winners[0]])]
    assert service.inbox("alice") == expected and service.inbox("bob") == expected
    assert service.movie_count == 1


def test_unfollow_racing_with_add_movie_has_a_valid_serial_order():
    for _ in range(100):
        service = make()
        service.follow("alice", "a1")
        results = run_threads([lambda: service.unfollow("alice", "a1"), lambda: service.add_movie("m1", "t", ["a1"])])
        assert results[1] is True
        assert service.inbox("alice") in ([], [Notice("m1", "t")])
        assert service.subscription_count == 0


def test_follow_racing_with_add_movie_never_double_notifies():
    for _ in range(100):
        service = make()
        results = run_threads([lambda: service.follow("alice", "a1"), lambda: service.add_movie("m1", "t", ["a1"])])
        assert results[1] is True
        assert service.inbox("alice") in ([], [Notice("m1", "t")])


def test_concurrent_distinct_imports_each_delivered_once_and_per_thread_order_kept():
    service = make()
    service.follow("alice", "a1")
    threads, per_thread = 8, 25

    def importer(t):
        return [service.add_movie(f"t{t}-m{i}", "title", ["a1"]) for i in range(per_thread)]

    results = run_threads([lambda t=t: importer(t) for t in range(threads)])
    assert all(all(r) and len(r) == per_thread for r in results)
    ids = [n.movie_id for n in service.inbox("alice")]
    assert len(ids) == threads * per_thread == len(set(ids))
    for t in range(threads):
        mine = [i for i in ids if i.startswith(f"t{t}-")]
        assert mine == [f"t{t}-m{i}" for i in range(per_thread)]


def test_readers_only_ever_see_a_prefix_of_the_history():
    service = make()
    service.follow("alice", "a1")
    total = 200
    expected = [Notice(f"m{i}", "t") for i in range(total)]
    seen = []

    def writer():
        for i in range(total):
            service.add_movie(f"m{i}", "t", ["a1"])

    def reader():
        for _ in range(300):
            seen.append(service.inbox("alice"))

    run_threads([writer, reader, reader])
    for snapshot in seen:
        assert snapshot == expected[: len(snapshot)]
    assert service.inbox("alice") == expected


def test_concurrent_follow_unfollow_leaves_no_residue():
    service = make()

    def churn(i):
        for _ in range(50):
            service.follow(f"u{i}", "a1")
            service.follow(f"u{i}", "a2")
            service.unfollow(f"u{i}", "a1")
            service.unfollow(f"u{i}", "a2")

    run_threads([lambda i=i: churn(i) for i in range(8)])
    assert service.subscription_count == 0
    assert service.tracked_actor_count == 0
