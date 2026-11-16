import importlib
import os
import sys
import threading
import time

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


class Posts:
    """帖子仓库的假实现：只回答 exists，并记下被问过哪些 ID。"""

    def __init__(self, ids=(10, 20)):
        self.ids = set(ids)
        self.asked = []

    def exists(self, post_id):
        self.asked.append(post_id)
        return post_id in self.ids


class FakeClock:
    def __init__(self, start=1_781_086_734.0):
        self.now = start

    def __call__(self):
        return self.now


def make(clock=None):
    posts = Posts()
    return impl.CommentService(posts, clock=clock or FakeClock()), posts


def comment_keys():
    return {"id", "post_id", "user_id", "content", "created_at", "replies"}


def reply_keys():
    return {"id", "post_id", "comment_id", "user_id", "content", "created_at"}


# ---- README 的例子与公开冒烟测试 ----

def test_readme_example_thread_exact_shapes():
    clock = FakeClock(1_781_086_734.0)
    service, _ = make(clock)
    c = service.add_comment(10, "u1", "Hello Leet")
    assert c == {"id": 1, "post_id": 10, "user_id": "u1", "content": "Hello Leet",
                 "created_at": 1_781_086_734.0, "replies": []}
    clock.now = 1_781_086_739.0
    r = service.add_reply(10, 1, "u2", "Hi Code")
    assert r == {"id": 1, "post_id": 10, "comment_id": 1, "user_id": "u2", "content": "Hi Code",
                 "created_at": 1_781_086_739.0}
    assert service.get_comments(10) == [{**c, "replies": [r]}]
    assert set(c) == comment_keys() and set(r) == reply_keys()


def test_public_smoke_scenario_order_isolation_and_errors():
    service, _ = make()
    assert service.get_comments(10) == []
    c1 = service.add_comment(10, "u1", "First comment")
    c2 = service.add_comment(10, "u2", "Second comment")
    r1 = service.add_reply(10, c1["id"], "u3", "First reply")
    r2 = service.add_reply(10, c1["id"], "u4", "Second reply")
    tree = service.get_comments(10)
    assert [c["id"] for c in tree] == [c1["id"], c2["id"]]
    assert [r["id"] for r in tree[0]["replies"]] == [r1["id"], r2["id"]]
    assert tree[1]["replies"] == []
    assert service.get_comments(20) == []
    with pytest.raises(impl.NotFoundError):
        service.add_reply(20, c1["id"], "u5", "wrong post")
    with pytest.raises(impl.ValidationError):
        service.add_comment(10, "", "bad")
    with pytest.raises(impl.NotFoundError):
        service.add_comment(999, "u1", "bad")


# ---- 校验 ----

BAD_TEXT = [None, 5, 1.5, True, [], b"x", "", " ", "   ", "\t\n", "\u00a0\u2003"]


@pytest.mark.parametrize("bad", BAD_TEXT)
def test_add_comment_rejects_bad_user_id_and_content(bad):
    service, _ = make()
    with pytest.raises(impl.ValidationError):
        service.add_comment(10, bad, "ok")
    with pytest.raises(impl.ValidationError):
        service.add_comment(10, "u1", bad)
    assert service.get_comments(10) == []


@pytest.mark.parametrize("bad", BAD_TEXT)
def test_add_reply_rejects_bad_user_id_and_content(bad):
    service, _ = make()
    service.add_comment(10, "u1", "root")
    with pytest.raises(impl.ValidationError):
        service.add_reply(10, 1, bad, "ok")
    with pytest.raises(impl.ValidationError):
        service.add_reply(10, 1, "u2", bad)
    assert service.get_comments(10)[0]["replies"] == []


def test_text_is_stored_and_returned_exactly_as_given():
    service, _ = make()
    c = service.add_comment(10, " u1 ", "  hello \n")
    r = service.add_reply(10, c["id"], "\tu2", "reply  ")
    assert (c["user_id"], c["content"]) == (" u1 ", "  hello \n")
    assert (r["user_id"], r["content"]) == ("\tu2", "reply  ")
    assert service.get_comments(10)[0]["content"] == "  hello \n"


def test_text_is_checked_before_the_post_is_looked_up():
    service, posts = make()
    with pytest.raises(impl.ValidationError):
        service.add_comment(999, "", "x")
    with pytest.raises(impl.ValidationError):
        service.add_reply(999, 999, "u1", "   ")
    assert posts.asked == []
    with pytest.raises(impl.NotFoundError):
        service.add_comment(999, "u1", "x")
    assert posts.asked == [999]


# ---- 资源关系 ----

def test_missing_post_fails_all_three_methods_and_leaves_no_trace():
    service, _ = make()
    for bad_post in (999, 0, -1, None, "10", True, 10.0):
        with pytest.raises(impl.NotFoundError):
            service.add_comment(bad_post, "u1", "x")
        with pytest.raises(impl.NotFoundError):
            service.add_reply(bad_post, 1, "u1", "x")
        with pytest.raises(impl.NotFoundError):
            service.get_comments(bad_post)
    assert service.add_comment(10, "u1", "first")["id"] == 1


def test_reply_to_missing_or_foreign_comment_is_not_found():
    service, _ = make()
    c = service.add_comment(10, "u1", "root")
    for bad_comment in (999, 0, -1, None, "1", True, 1.0):
        with pytest.raises(impl.NotFoundError):
            service.add_reply(10, bad_comment, "u2", "x")
    with pytest.raises(impl.NotFoundError):
        service.add_reply(20, c["id"], "u2", "wrong post")
    assert service.get_comments(10)[0]["replies"] == []
    assert service.get_comments(20) == []


def test_posts_are_isolated_from_each_other():
    service, _ = make()
    service.add_comment(10, "u1", "on ten")
    service.add_comment(20, "u2", "on twenty")
    assert [c["content"] for c in service.get_comments(10)] == ["on ten"]
    assert [c["content"] for c in service.get_comments(20)] == ["on twenty"]
    assert service.get_comments(10)[0]["post_id"] == 10
    assert service.get_comments(20)[0]["post_id"] == 20


# ---- ID ----

def test_comment_and_reply_ids_are_independent_sequences():
    service, _ = make()
    assert service.add_comment(10, "u", "a")["id"] == 1
    assert service.add_reply(10, 1, "u", "r")["id"] == 1
    assert service.add_comment(10, "u", "b")["id"] == 2
    assert service.add_reply(10, 2, "u", "r")["id"] == 2
    assert service.add_reply(10, 1, "u", "r")["id"] == 3


def test_ids_are_global_not_per_post():
    service, _ = make()
    assert service.add_comment(10, "u", "a")["id"] == 1
    assert service.add_comment(20, "u", "b")["id"] == 2
    assert service.add_reply(20, 2, "u", "r")["id"] == 1
    with pytest.raises(impl.NotFoundError):
        service.add_reply(20, 1, "u", "comment 1 lives on post 10")


def test_a_failed_call_does_not_use_up_an_id():
    service, _ = make()
    with pytest.raises(impl.ValidationError):
        service.add_comment(10, "", "x")
    with pytest.raises(impl.NotFoundError):
        service.add_comment(999, "u", "x")
    assert service.add_comment(10, "u", "a")["id"] == 1
    with pytest.raises(impl.ValidationError):
        service.add_reply(10, 1, "u", " ")
    with pytest.raises(impl.NotFoundError):
        service.add_reply(10, 77, "u", "x")
    with pytest.raises(impl.NotFoundError):
        service.add_reply(20, 1, "u", "x")
    assert service.add_reply(10, 1, "u", "r")["id"] == 1


def test_a_failing_clock_does_not_use_up_an_id():
    calls = {"n": 0}

    def clock():
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("clock down")
        return 5.0

    service = impl.CommentService(Posts(), clock=clock)
    with pytest.raises(RuntimeError):
        service.add_comment(10, "u", "x")
    assert service.add_comment(10, "u", "x")["id"] == 1


# ---- 顺序与时间 ----

def test_order_is_commit_order_even_when_the_clock_goes_backwards():
    clock = FakeClock(1000.0)
    service, _ = make(clock)
    service.add_comment(10, "u", "first")
    clock.now = 500.0
    service.add_comment(10, "u", "second")
    service.add_reply(10, 1, "u", "r-a")
    clock.now = 100.0
    service.add_reply(10, 1, "u", "r-b")
    clock.now = 2000.0
    service.add_reply(10, 1, "u", "r-c")
    tree = service.get_comments(10)
    assert [c["content"] for c in tree] == ["first", "second"]
    assert [r["content"] for r in tree[0]["replies"]] == ["r-a", "r-b", "r-c"]
    assert [r["id"] for r in tree[0]["replies"]] == [1, 2, 3]


def test_replies_stay_under_their_own_comment_when_interleaved():
    service, _ = make()
    service.add_comment(10, "u", "A")
    service.add_comment(10, "u", "B")
    service.add_reply(10, 2, "u", "B1")
    service.add_reply(10, 1, "u", "A1")
    service.add_reply(10, 2, "u", "B2")
    tree = service.get_comments(10)
    assert [[r["content"] for r in c["replies"]] for c in tree] == [["A1"], ["B1", "B2"]]
    assert all(r["comment_id"] == c["id"] for c in tree for r in c["replies"])


def test_default_clock_returns_float_seconds():
    service = impl.CommentService(Posts())
    before = time.time()
    c = service.add_comment(10, "u", "x")
    r = service.add_reply(10, 1, "u", "y")
    after = time.time()
    for created in (c["created_at"], r["created_at"]):
        assert isinstance(created, float)
        assert before <= created <= after


# ---- 快照 ----

def test_returned_values_are_snapshots_that_can_be_mutated_freely():
    service, _ = make()
    c = service.add_comment(10, "u1", "root")
    service.add_reply(10, 1, "u2", "kid")
    expected = service.get_comments(10)

    c["content"] = "hacked"
    c["replies"].append({"id": 99})
    got = service.get_comments(10)
    got[0]["content"] = "hacked"
    got[0]["replies"][0]["content"] = "hacked"
    got[0]["replies"].clear()
    got.clear()
    r = service.add_reply(10, 1, "u3", "second")
    r["content"] = "hacked"

    again = service.get_comments(10)
    assert again[0]["content"] == "root"
    assert [x["content"] for x in again[0]["replies"]] == ["kid", "second"]
    assert again[0]["replies"][0] == expected[0]["replies"][0]


def test_an_old_snapshot_does_not_change_when_the_thread_grows():
    service, _ = make()
    c = service.add_comment(10, "u", "root")
    snap = service.get_comments(10)
    service.add_reply(10, 1, "u", "later")
    service.add_comment(10, "u", "another")
    assert c["replies"] == [] and snap[0]["replies"] == [] and len(snap) == 1
    assert len(service.get_comments(10)) == 2


def test_empty_results_are_fresh_lists():
    service, _ = make()
    first = service.get_comments(10)
    first.append("junk")
    assert service.get_comments(10) == []


# ---- 并发 ----

def run_threads(targets):
    barrier = threading.Barrier(len(targets))
    errors = []

    def wrap(fn):
        def go():
            barrier.wait()
            try:
                fn()
            except BaseException as exc:  # noqa: BLE001
                errors.append(exc)
        return go

    threads = [threading.Thread(target=wrap(fn)) for fn in targets]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=30)
    assert not errors, errors
    assert not any(t.is_alive() for t in threads)


def test_concurrent_comments_get_unique_gapless_ids_in_commit_order():
    service, _ = make()
    workers, each = 16, 40

    def worker(n):
        def go():
            for i in range(each):
                service.add_comment(10, f"u{n}", f"c{n}-{i}")
        return go

    run_threads([worker(n) for n in range(workers)])
    tree = service.get_comments(10)
    ids = [c["id"] for c in tree]
    assert ids == list(range(1, workers * each + 1))
    for n in range(workers):  # 同一线程自己的评论，顺序没有被打乱
        mine = [c["content"] for c in tree if c["user_id"] == f"u{n}"]
        assert mine == [f"c{n}-{i}" for i in range(each)]


def test_concurrent_replies_to_one_comment_keep_unique_ids_and_order():
    service, _ = make()
    service.add_comment(10, "u", "root")
    workers, each = 12, 30

    def worker(n):
        def go():
            for i in range(each):
                service.add_reply(10, 1, f"u{n}", f"r{n}-{i}")
        return go

    run_threads([worker(n) for n in range(workers)])
    replies = service.get_comments(10)[0]["replies"]
    assert [r["id"] for r in replies] == list(range(1, workers * each + 1))


def test_concurrent_writes_on_two_posts_do_not_leak():
    service, _ = make()
    service.add_comment(10, "u", "root-10")
    service.add_comment(20, "u", "root-20")

    def writer(post, comment):
        def go():
            for i in range(60):
                service.add_comment(post, f"p{post}", f"c{i}")
                service.add_reply(post, comment, f"p{post}", f"r{i}")
        return go

    run_threads([writer(10, 1), writer(20, 2), writer(10, 1), writer(20, 2)])
    for post in (10, 20):
        tree = service.get_comments(post)
        assert len(tree) == 121
        assert {c["post_id"] for c in tree} == {post}
        replies = [r for c in tree for r in c["replies"]]
        assert len(replies) == 120
        assert {r["post_id"] for r in replies} == {post}
    ids = [c["id"] for post in (10, 20) for c in service.get_comments(post)]
    assert sorted(ids) == list(range(1, 243))


def test_a_reader_during_writes_always_sees_one_consistent_moment():
    service, _ = make()
    stop = threading.Event()
    problems = []

    def writer():
        try:
            for i in range(150):
                c = service.add_comment(10, "w", f"c{i}")
                service.add_reply(10, c["id"], "w", f"r{i}")
                service.add_reply(10, c["id"], "w", f"s{i}")
        finally:
            stop.set()

    def reader():
        while not stop.is_set():
            tree = service.get_comments(10)
            if [c["id"] for c in tree] != list(range(1, len(tree) + 1)):
                problems.append("comment ids are not a gapless prefix")
            for c in tree:
                ids = [r["id"] for r in c["replies"]]
                if ids != sorted(ids) or len(set(ids)) != len(ids):
                    problems.append("reply ids out of order")
                if any(r["comment_id"] != c["id"] for r in c["replies"]):
                    problems.append("reply under the wrong comment")
            # 写线程每条评论后各追加两条回复：只有最后一条评论可以暂时回复不满
            if any(len(c["replies"]) != 2 for c in tree[:-1]):
                problems.append("an earlier thread is incomplete")
            tree.clear()

    old = sys.getswitchinterval()
    sys.setswitchinterval(1e-6)  # 让线程切换更频繁，把偶发的交错放大
    try:
        run_threads([writer, reader, reader, reader])
    finally:
        sys.setswitchinterval(old)
    assert not problems, problems[:3]
    final = service.get_comments(10)
    assert len(final) == 150 and all(len(c["replies"]) == 2 for c in final)
