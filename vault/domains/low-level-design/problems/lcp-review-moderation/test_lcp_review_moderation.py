import importlib
import os
import threading
import time

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))
ReviewService = impl.ReviewService
ServiceError = impl.ServiceError

BAD = "scam"


class Recorder:
    """记录每次被问到的内容；内容里含 BAD 就拒绝。"""

    def __init__(self, pause=0.0):
        self.seen = []
        self.pause = pause  # 并发测试里让审核器慢一点：没有锁的实现会在这段时间里被别的线程插进来
        self._lock = threading.Lock()

    def __call__(self, text):
        with self._lock:
            self.seen.append(text)
        if self.pause:
            time.sleep(self.pause)
        return BAD not in text


def failure(call, *args):
    with pytest.raises(ServiceError) as caught:
        call(*args)
    return caught.value.status, caught.value.code


def make(pause=0.0):
    checker = Recorder(pause)
    return ReviewService(checker), checker


def block(service, user="mira"):
    """让一个用户连续被拒三次，返回封禁后的状态。"""
    for _ in range(3):
        assert failure(service.create, user, BAD) == (422, "content_rejected")
    return service.user_state(user)


# ---- 规则 1：输入 ----

@pytest.mark.parametrize("bad", ["", "   ", "\t\n", "\u001c\u001f", "　 ", None, 7, b"x", ["x"]])
def test_invalid_user_or_content_is_rejected_everywhere_and_never_reaches_checker(bad):
    service, checker = make()
    first = service.create("mira", "fine")
    assert failure(service.create, bad, "fine") == (400, "invalid_input")
    assert failure(service.create, "mira", bad) == (400, "invalid_input")
    assert failure(service.edit, first["id"], bad, "fine") == (400, "invalid_input")
    assert failure(service.edit, first["id"], "mira", bad) == (400, "invalid_input")
    assert failure(service.user_state, bad) == (400, "invalid_input")
    assert checker.seen == ["fine"]
    assert service.user_state("mira") == {"strikes": 0, "flagged": False}


def test_content_and_user_keep_their_surrounding_whitespace_and_checker_gets_exact_text():
    service, checker = make()
    row = service.create(" Noah ", "\tLoud FAN \n")
    assert row == {"id": 1, "user": " Noah ", "content": "\tLoud FAN \n", "version": 1}
    assert checker.seen == ["\tLoud FAN \n"]
    assert service.user_state("Noah") == {"strikes": 0, "flagged": False}  # 没有 strip 归一
    assert failure(service.edit, 1, "Noah", "x") == (403, "forbidden")


def test_checker_sees_mixed_case_unchanged_and_exactly_once_per_valid_write():
    service, checker = make()
    row = service.create("mira", "Great Item")
    service.edit(row["id"], "mira", "MiXeD Case")
    # 审核器区分大小写：原样的 "SCAM" 它放行；被改成小写再交给它就会被拒，所以这一行能抓到改写内容的缺陷
    assert service.create("mira", "SCAM")["id"] == 2
    assert failure(service.create, "mira", "a scam") == (422, "content_rejected")
    assert checker.seen == ["Great Item", "MiXeD Case", "SCAM", "a scam"]
    assert service.user_state("mira")["strikes"] == 1


# ---- 规则 2：新建与读取 ----

def test_example_flow_create_edit_reject():
    service, _ = make()
    row = service.create("mira", "Solid battery")
    assert service.edit(row["id"], "mira", "Solid battery, loud fan")["version"] == 2
    assert failure(service.create, "mira", "a scam") == (422, "content_rejected")
    assert service.user_state("mira")["strikes"] == 1
    assert service.get(row["id"]) == {"id": 1, "user": "mira", "content": "Solid battery, loud fan", "version": 2}


def test_ids_are_consecutive_and_failed_writes_never_consume_one():
    boom = {"on": False}

    def checker(text):
        if boom["on"]:
            raise RuntimeError("down")
        return BAD not in text

    service = ReviewService(checker)
    assert service.create("a", "one")["id"] == 1
    assert failure(service.create, "a", BAD) == (422, "content_rejected")
    assert failure(service.create, "", "x") == (400, "invalid_input")
    boom["on"] = True
    assert failure(service.create, "a", "two") == (503, "checker_unavailable")
    boom["on"] = False
    assert service.create("a", "two")["id"] == 2
    assert [service.create("b", f"r{i}")["id"] for i in range(3)] == [3, 4, 5]


def test_get_missing_and_snapshots_are_detached():
    service, _ = make()
    assert failure(service.get, 99) == (404, "review_not_found")
    created = service.create("mira", "fine")
    created["content"] = "tampered"
    fetched = service.get(1)
    fetched["version"] = 50
    edited = service.edit(1, "mira", "second")
    edited["user"] = "someone else"
    state = service.user_state("mira")
    state["strikes"] = 9
    assert service.get(1) == {"id": 1, "user": "mira", "content": "second", "version": 2}
    assert service.user_state("mira") == {"strikes": 0, "flagged": False}


# ---- 规则 3：拒绝与违规数 ----

def test_rejection_adds_exactly_one_strike_and_saves_nothing():
    service, _ = make()
    assert service.user_state("mira") == {"strikes": 0, "flagged": False}
    assert failure(service.create, "mira", BAD) == (422, "content_rejected")
    assert service.user_state("mira") == {"strikes": 1, "flagged": False}
    assert failure(service.get, 1) == (404, "review_not_found")
    assert service.create("mira", "clean")["id"] == 1
    assert failure(service.create, "mira", BAD) == (422, "content_rejected")
    assert service.user_state("mira") == {"strikes": 2, "flagged": False}  # 干净的写入没有清零


def test_rejected_edit_keeps_content_and_version_and_counts_as_a_strike():
    service, _ = make()
    row = service.create("mira", "clean")
    service.edit(row["id"], "mira", "cleaner")
    assert failure(service.edit, row["id"], "mira", BAD) == (422, "content_rejected")
    assert service.get(row["id"]) == {"id": 1, "user": "mira", "content": "cleaner", "version": 2}
    assert service.user_state("mira")["strikes"] == 1


def test_users_and_instances_are_isolated():
    one, _ = make()
    two, _ = make()
    assert block(one)["flagged"] is True
    assert one.create("noah", "fine")["id"] == 1
    assert one.user_state("noah") == {"strikes": 0, "flagged": False}
    assert two.user_state("mira") == {"strikes": 0, "flagged": False}
    assert two.create("mira", "fine")["id"] == 1


# ---- 规则 4：封禁 ----

def test_third_rejection_still_reports_rejected_and_then_everything_is_blocked():
    service, checker = make()
    mine = service.create("mira", "keep me")
    assert failure(service.create, "mira", BAD) == (422, "content_rejected")
    assert failure(service.edit, mine["id"], "mira", BAD) == (422, "content_rejected")
    assert service.user_state("mira") == {"strikes": 2, "flagged": False}
    assert failure(service.create, "mira", BAD) == (422, "content_rejected")
    assert service.user_state("mira") == {"strikes": 3, "flagged": True}
    asked = len(checker.seen)
    for _ in range(2):
        assert failure(service.create, "mira", "perfectly clean") == (403, "user_blocked")
        assert failure(service.edit, mine["id"], "mira", "perfectly clean") == (403, "user_blocked")
        assert failure(service.create, "mira", BAD) == (403, "user_blocked")
    assert len(checker.seen) == asked  # 封禁之后审核器一次也没被问
    assert service.user_state("mira") == {"strikes": 3, "flagged": True}  # 违规数不再增加
    assert service.get(mine["id"])["content"] == "keep me"  # 读取不受封禁影响
    assert service.create("noah", "hello")["id"] == 2


# ---- 规则 5：顺序 ----

def test_create_order_input_then_block_then_checker():
    service, checker = make()
    block(service)
    asked = len(checker.seen)
    assert failure(service.create, "mira", "  ") == (400, "invalid_input")
    assert failure(service.create, "mira", BAD) == (403, "user_blocked")
    assert len(checker.seen) == asked


def test_edit_order_input_then_existence_then_owner_then_block_then_checker():
    service, checker = make()
    theirs = service.create("noah", "noah's review")
    block(service)
    asked = len(checker.seen)
    assert failure(service.edit, 99, "mira", " ") == (400, "invalid_input")  # 输入先于存在
    assert failure(service.edit, 99, "mira", "x") == (404, "review_not_found")  # 存在先于归属与封禁
    assert failure(service.edit, theirs["id"], "mira", "x") == (403, "forbidden")  # 归属先于封禁
    assert len(checker.seen) == asked
    mine = service.create("noah", "second")
    assert failure(service.edit, mine["id"], "noah", BAD) == (422, "content_rejected")  # 没被封的作者走到审核器


def test_forbidden_edit_neither_asks_the_checker_nor_costs_a_strike():
    service, checker = make()
    row = service.create("noah", "mine")
    assert failure(service.edit, row["id"], "mira", BAD) == (403, "forbidden")
    assert checker.seen == ["mine"]
    assert service.user_state("mira")["strikes"] == 0


# ---- 规则 6：编辑 ----

def test_edit_keeps_id_and_author_and_bumps_version_even_for_identical_content():
    service, _ = make()
    row = service.create("mira", "same")
    first = service.edit(row["id"], "mira", "same")
    second = service.edit(row["id"], "mira", "new text")
    assert first == {"id": 1, "user": "mira", "content": "same", "version": 2}
    assert second == {"id": 1, "user": "mira", "content": "new text", "version": 3}
    assert service.get(1) == second


# ---- 规则 7：审核器出错 ----

def test_checker_failure_changes_nothing_and_is_not_a_strike():
    state = {"mode": "ok"}

    def checker(text):
        if state["mode"] == "down":
            raise TimeoutError("checker timed out")
        return BAD not in text

    service = ReviewService(checker)
    row = service.create("mira", "before")
    state["mode"] = "down"
    for _ in range(5):  # 次数再多也不会封人
        assert failure(service.create, "mira", "fresh") == (503, "checker_unavailable")
        assert failure(service.edit, row["id"], "mira", "after") == (503, "checker_unavailable")
    assert service.get(row["id"]) == {"id": 1, "user": "mira", "content": "before", "version": 1}
    assert service.user_state("mira") == {"strikes": 0, "flagged": False}
    state["mode"] = "ok"
    assert service.create("mira", "fresh")["id"] == 2


def test_only_exception_is_translated_base_exception_passes_through():
    def checker(text):
        raise KeyboardInterrupt

    service = ReviewService(checker)
    with pytest.raises(KeyboardInterrupt):
        service.create("mira", "x")
    # 异常穿过去之后，锁已经释放，服务还能用
    assert service.user_state("mira") == {"strikes": 0, "flagged": False}


def test_failure_does_not_poison_a_block_already_in_force():
    state = {"down": False}

    def checker(text):
        if state["down"]:
            raise RuntimeError("down")
        return False

    service = ReviewService(checker)
    block(service)
    state["down"] = True
    assert failure(service.create, "mira", "x") == (403, "user_blocked")  # 封禁先于审核器，所以不是 503


def test_checker_may_read_the_service_while_it_runs():
    holder = {}

    def checker(text):
        holder["seen"] = holder["service"].user_state("mira")  # 在锁里回头读自己
        return True

    service = ReviewService(checker)
    holder["service"] = service
    assert service.create("mira", "fine")["id"] == 1
    assert holder["seen"] == {"strikes": 0, "flagged": False}


# ---- 规则 8：并发 ----

def run_together(count, work):
    barrier = threading.Barrier(count)
    outcomes = [None] * count

    def runner(slot):
        barrier.wait()
        try:
            outcomes[slot] = ("ok", work(slot))
        except ServiceError as error:
            outcomes[slot] = ("err", error.status, error.code)

    threads = [threading.Thread(target=runner, args=(i,)) for i in range(count)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=20)
        assert not thread.is_alive()
    return outcomes


def test_concurrent_rejections_give_exactly_three_rejections_and_three_checker_calls():
    service, checker = make(pause=0.005)
    outcomes = run_together(16, lambda slot: service.create("mira", f"{BAD} {slot}"))
    codes = sorted(o[2] for o in outcomes)
    assert codes == ["content_rejected"] * 3 + ["user_blocked"] * 13
    assert len(checker.seen) == 3
    assert service.user_state("mira") == {"strikes": 3, "flagged": True}


def test_concurrent_creates_by_many_users_hand_out_each_id_once():
    service, _ = make(pause=0.005)
    outcomes = run_together(24, lambda slot: service.create(f"user-{slot}", f"review {slot}")["id"])
    assert sorted(o[1] for o in outcomes) == list(range(1, 25))
    assert {service.get(i)["user"] for i in range(1, 25)} == {f"user-{i}" for i in range(24)}


def test_concurrent_edits_of_one_review_lose_no_version():
    service, _ = make(pause=0.005)
    row = service.create("mira", "start")
    outcomes = run_together(20, lambda slot: service.edit(row["id"], "mira", f"edit {slot}")["version"])
    assert sorted(o[1] for o in outcomes) == list(range(2, 22))
    assert service.get(row["id"])["version"] == 21


def test_concurrent_rejected_edits_and_creates_by_one_user_still_stop_at_three():
    service, checker = make(pause=0.005)
    row = service.create("mira", "keep")

    def work(slot):
        if slot % 2:
            return service.edit(row["id"], "mira", BAD)
        return service.create("mira", BAD)

    outcomes = run_together(10, work)
    assert sorted(o[2] for o in outcomes) == ["content_rejected"] * 3 + ["user_blocked"] * 7
    assert len(checker.seen) == 4  # 第一次的干净新建加上三次被拒
    assert service.get(row["id"])["content"] == "keep"
