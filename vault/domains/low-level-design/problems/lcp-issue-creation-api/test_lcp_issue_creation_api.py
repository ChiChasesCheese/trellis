import importlib
import os
import threading

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))
ServiceError = impl.ServiceError


def make():
    return impl.IssueService({"demo": ["alice", "bob"], "other": ["alice"], "empty": []})


def fails(expected_status, code, fn, *args, **kwargs):
    """调用必须抛 ServiceError(expected_status, code)。"""
    with pytest.raises(ServiceError) as info:
        fn(*args, **kwargs)
    assert (info.value.status, info.value.code) == (expected_status, code)


def new(service, title="Bug", user="alice", project="demo", key=None, **extra):
    status, issue = service.create(user, project, {"title": title, **extra}, key)
    assert status == 201
    return issue


# ---- README 里的例子 ----

def test_readme_example():
    service = impl.IssueService({"demo": ["alice"]})
    status, issue = service.create("alice", "demo", {"title": " Fix login "}, "retry-1")
    assert status == 201
    assert issue == {"id": 1, "project": "demo", "creator": "alice", "title": "Fix login",
                     "description": "", "status": "open", "version": 1}
    assert service.create("alice", "demo", {"title": "Fix login"}, "retry-1") == (200, issue)
    updated = service.transition("alice", "demo", 1, "closed", 1)
    assert updated == {**issue, "status": "closed", "version": 2}


# ---- 第 1 条：授权先于一切 ----

@pytest.mark.parametrize("user", [None, "", "   ", "\t\n", 7, ["alice"]])
def test_bad_user_is_401_on_every_method(user):
    service = make()
    fails(401, "unauthorized", service.create, user, "demo", {"title": "x"})
    fails(401, "unauthorized", service.get, user, "demo", 1)
    fails(401, "unauthorized", service.transition, user, "demo", 1, "closed", 1)
    fails(401, "unauthorized", service.list, user, "demo")


def test_unknown_project_and_nonmember_are_404_not_403():
    service = make()
    for project, user in [("nope", "alice"), ("other", "bob"), ("empty", "alice"), (None, "alice"), (["demo"], "alice")]:
        fails(404, "project_not_found", service.create, user, project, {"title": "x"})
        fails(404, "project_not_found", service.get, user, project, 1)
        fails(404, "project_not_found", service.transition, user, project, 1, "closed", 1)
        fails(404, "project_not_found", service.list, user, project)


def test_authorization_beats_validation():
    service = make()
    fails(401, "unauthorized", service.create, "", "demo", "not a dict", "")
    fails(404, "project_not_found", service.create, "bob", "other", "not a dict", "")
    fails(404, "project_not_found", service.transition, "bob", "other", 99, "weird", "weird")
    fails(404, "project_not_found", service.list, "bob", "other", "weird", -1, 0)


def test_membership_is_copied_at_construction():
    members = {"demo": ["alice"]}
    service = impl.IssueService(members)
    members["demo"].append("mallory")
    members["new"] = ["alice"]
    fails(404, "project_not_found", service.create, "mallory", "demo", {"title": "x"})
    fails(404, "project_not_found", service.create, "alice", "new", {"title": "x"})


def test_members_share_issues_across_users():
    service = make()
    issue = new(service, user="alice")
    assert service.get("bob", "demo", issue["id"]) == issue
    assert service.transition("bob", "demo", issue["id"], "closed", 1)["status"] == "closed"
    assert service.get("alice", "demo", issue["id"])["creator"] == "alice"


# ---- 第 2、3 条：创建的输入与结果 ----

def test_create_result_and_trimmed_title():
    service = make()
    status, issue = service.create("bob", "demo", {"title": "　 Fix  login \n", "description": "  keep  \n"})
    assert status == 201
    assert issue == {"id": 1, "project": "demo", "creator": "bob", "title": "Fix  login",
                     "description": "  keep  \n", "status": "open", "version": 1}
    assert service.get("alice", "demo", 1) == issue


@pytest.mark.parametrize("payload", [
    None, [], "title", 5, {}, {"description": "x"}, {"title": 5}, {"title": None}, {"title": ["a"]},
    {"title": ""}, {"title": "  \t "}, {"title": "x" * 121}, {"title": "  " + "x" * 121 + "  "},
    {"title": "ok", "description": 5}, {"title": "ok", "description": None},
    {"title": "ok", "description": "d" * 2001}, {"title": "ok", "extra": 1}, {"title": "ok", 1: 2},
])
def test_invalid_payloads_are_400(payload):
    fails(400, "invalid_input", make().create, "alice", "demo", payload)


def test_length_boundaries_are_inclusive():
    service = make()
    assert new(service, title="x" * 120)["title"] == "x" * 120
    assert new(service, title="  " + "y" * 120 + "  ")["title"] == "y" * 120
    assert new(service, title="z", description="d" * 2000)["description"] == "d" * 2000
    assert new(service, title="w", description="")["description"] == ""


@pytest.mark.parametrize("key", ["", "k" * 65, 5, b"k", ["k"], True])
def test_invalid_keys_are_400(key):
    fails(400, "invalid_input", make().create, "alice", "demo", {"title": "x"}, key)


def test_key_length_boundaries_and_whitespace_is_significant():
    service = make()
    assert service.create("alice", "demo", {"title": "x"}, "k" * 64)[0] == 201
    assert service.create("alice", "demo", {"title": "x"}, "k")[0] == 201
    assert service.create("alice", "demo", {"title": "x"}, " k")[0] == 201   # 与 "k" 不同
    assert service.create("alice", "demo", {"title": "x"}, "k ")[0] == 201   # 与 "k" 不同
    assert service.create("alice", "demo", {"title": "x"}, "k")[0] == 200


# ---- 第 3 条：id、失败不留痕、返回快照 ----

def test_ids_are_global_across_projects_and_users():
    service = make()
    assert new(service, project="demo")["id"] == 1
    assert new(service, project="other")["id"] == 2
    assert new(service, user="bob", project="demo")["id"] == 3


def test_failed_creates_and_replays_do_not_consume_ids():
    service = make()
    assert new(service, key="a")["id"] == 1
    fails(400, "invalid_input", service.create, "alice", "demo", {"title": ""}, "b")
    fails(409, "idempotency_conflict", service.create, "alice", "demo", {"title": "other"}, "a")
    assert service.create("alice", "demo", {"title": "Bug"}, "a")[0] == 200
    fails(404, "project_not_found", service.create, "alice", "nope", {"title": "x"})
    assert new(service)["id"] == 2
    # 失败的请求没有占用键："b" 之后仍可用来创建
    assert service.create("alice", "demo", {"title": "fresh"}, "b") == (201, {**service.get("alice", "demo", 3)})


def test_without_a_key_every_request_creates_a_new_issue():
    service = make()
    assert [new(service)["id"] for _ in range(3)] == [1, 2, 3]
    assert len(service.list("alice", "demo")) == 3


def test_get_is_scoped_to_project_and_detached():
    service = make()
    issue = new(service, project="demo")
    fails(404, "issue_not_found", service.get, "alice", "other", issue["id"])
    fails(404, "issue_not_found", service.get, "alice", "demo", 999)
    fails(404, "issue_not_found", service.get, "alice", "demo", 0)
    fails(404, "issue_not_found", service.get, "alice", "demo", True)   # True == 1，但不是 id
    fails(404, "issue_not_found", service.get, "alice", "demo", "1")
    fails(404, "issue_not_found", service.transition, "alice", "other", issue["id"], "closed", 1)


def test_inputs_and_results_are_isolated():
    service = make()
    payload = {"title": "Bug", "description": "d"}
    _, issue = service.create("alice", "demo", payload, "k")
    payload["title"] = "mutated"
    issue["title"] = "mutated"
    issue["status"] = "closed"
    assert service.get("alice", "demo", 1)["title"] == "Bug"
    assert service.get("alice", "demo", 1)["status"] == "open"
    fetched = service.get("alice", "demo", 1)
    fetched["version"] = 99
    listed = service.list("alice", "demo")
    listed[0]["title"] = "mutated"
    listed.clear()
    assert service.get("alice", "demo", 1) == {"id": 1, "project": "demo", "creator": "alice", "title": "Bug",
                                                "description": "d", "status": "open", "version": 1}
    assert service.create("alice", "demo", {"title": "Bug", "description": "d"}, "k")[0] == 200


# ---- 第 4 条：幂等 ----

def test_replay_returns_the_current_issue_even_after_status_changes():
    service = make()
    issue = new(service, key="r")
    service.transition("bob", "demo", issue["id"], "closed", 1)
    status, again = service.create("alice", "demo", {"title": "Bug"}, "r")
    assert (status, again["status"], again["version"], again["id"]) == (200, "closed", 2, 1)
    assert len(service.list("alice", "demo")) == 1


def test_replay_compares_the_canonical_payload():
    service = make()
    new(service, title="Fix login", key="r", description="")
    assert service.create("alice", "demo", {"title": "  Fix login  "}, "r")[0] == 200
    assert service.create("alice", "demo", {"title": "Fix login", "description": ""}, "r")[0] == 200
    fails(409, "idempotency_conflict", service.create, "alice", "demo", {"title": "Fix login", "description": " "}, "r")
    fails(409, "idempotency_conflict", service.create, "alice", "demo", {"title": "fix login"}, "r")


def test_idempotency_scope_is_user_project_key():
    service = make()
    first = new(service, user="alice", project="demo", key="same")
    second = new(service, user="bob", project="demo", key="same")
    third = new(service, user="alice", project="other", key="same")
    assert len({first["id"], second["id"], third["id"]}) == 3
    assert service.create("bob", "demo", {"title": "Bug"}, "same") == (200, second)
    fails(409, "idempotency_conflict", service.create, "bob", "demo", {"title": "x"}, "same")


def test_invalid_payload_with_a_used_key_is_400_not_409():
    service = make()
    new(service, key="r")
    fails(400, "invalid_input", service.create, "alice", "demo", {"title": " "}, "r")
    fails(400, "invalid_input", service.create, "alice", "demo", {"title": "Bug", "x": 1}, "r")


# ---- 第 5 条：状态与版本 ----

def test_transition_changes_status_once_per_change_and_returns_the_issue():
    service = make()
    issue = new(service)
    closed = service.transition("alice", "demo", issue["id"], "closed", 1)
    assert closed == {**issue, "status": "closed", "version": 2}
    same = service.transition("alice", "demo", issue["id"], "closed", 2)
    assert same == closed                                  # 状态没变：版本不变
    reopened = service.transition("bob", "demo", issue["id"], "open", 2)
    assert (reopened["status"], reopened["version"]) == ("open", 3)
    assert service.get("alice", "demo", issue["id"]) == reopened


def test_version_must_match_even_for_a_same_status_request():
    service = make()
    issue = new(service)
    fails(409, "version_conflict", service.transition, "alice", "demo", issue["id"], "open", 2)
    fails(409, "version_conflict", service.transition, "alice", "demo", issue["id"], "closed", 7)
    service.transition("alice", "demo", issue["id"], "closed", 1)
    fails(409, "version_conflict", service.transition, "alice", "demo", issue["id"], "closed", 1)
    fails(409, "version_conflict", service.transition, "alice", "demo", issue["id"], "open", 1)
    assert service.get("alice", "demo", issue["id"])["version"] == 2    # 失败不改任何东西


@pytest.mark.parametrize("status,version", [
    ("done", 1), ("OPEN", 1), ("", 1), (None, 1), (1, 1), (["open"], 1),
    ("closed", 0), ("closed", -1), ("closed", 1.0), ("closed", "1"), ("closed", True), ("closed", None),
])
def test_invalid_status_or_version_is_400(status, version):
    service = make()
    issue = new(service)
    fails(400, "invalid_input", service.transition, "alice", "demo", issue["id"], status, version)
    assert service.get("alice", "demo", issue["id"])["version"] == 1


def test_lookup_comes_before_value_validation_in_transition():
    service = make()
    fails(404, "issue_not_found", service.transition, "alice", "demo", 42, "garbage", "garbage")


# ---- 第 6 条：列表 ----

def test_list_filters_orders_and_limits():
    service = make()
    for index in range(1, 8):
        new(service, title=f"t{index}", project="demo" if index % 2 else "other")   # 奇数 id 在 demo
    new(service, project="demo")                                                     # id 8
    service.transition("alice", "demo", 3, "closed", 1)
    service.transition("alice", "demo", 7, "closed", 1)
    ids = lambda rows: [row["id"] for row in rows]
    assert ids(service.list("alice", "demo")) == [1, 3, 5, 7, 8]
    assert ids(service.list("alice", "demo", status="open")) == [1, 5, 8]
    assert ids(service.list("alice", "demo", status="closed")) == [3, 7]
    assert ids(service.list("alice", "other")) == [2, 4, 6]
    assert ids(service.list("alice", "demo", after_id=3)) == [5, 7, 8]
    assert ids(service.list("alice", "demo", after_id=4, limit=2)) == [5, 7]
    assert ids(service.list("alice", "demo", status="open", after_id=1, limit=1)) == [5]
    assert service.list("alice", "demo", after_id=8) == []
    assert service.list("alice", "demo", after_id=10**12) == []


def test_filter_applies_before_the_limit():
    service = make()
    for _ in range(6):
        new(service)
    for issue_id in (1, 2, 3, 4):
        service.transition("alice", "demo", issue_id, "closed", 1)
    assert [row["id"] for row in service.list("alice", "demo", status="open", limit=2)] == [5, 6]


def test_paging_with_the_last_id_visits_every_issue_once():
    service = make()
    for _ in range(25):
        new(service)
    seen, cursor = [], 0
    while page := service.list("alice", "demo", after_id=cursor, limit=10):
        seen += [row["id"] for row in page]
        cursor = page[-1]["id"]
    assert seen == list(range(1, 26))


def test_cursor_paging_survives_a_close_between_pages():
    service = make()
    for _ in range(5):
        new(service)
    first = service.list("alice", "demo", status="open", limit=2)
    service.transition("alice", "demo", 1, "closed", 1)
    second = service.list("alice", "demo", status="open", after_id=first[-1]["id"], limit=2)
    assert [row["id"] for row in first] == [1, 2]
    assert [row["id"] for row in second] == [3, 4]  # offset=2 would give [4, 5] and skip 3


@pytest.mark.parametrize("kwargs", [
    {"status": "done"}, {"status": ""}, {"status": 1}, {"status": ["open"]},
    {"after_id": -1}, {"after_id": True}, {"after_id": "0"}, {"after_id": 1.5}, {"after_id": None},
    {"limit": 0}, {"limit": 101}, {"limit": -5}, {"limit": True}, {"limit": "20"}, {"limit": 2.0}, {"limit": None},
])
def test_invalid_list_arguments_are_400(kwargs):
    fails(400, "invalid_input", make().list, "alice", "demo", **kwargs)


def test_list_limit_boundaries_are_inclusive():
    service = make()
    for _ in range(105):
        new(service)
    assert len(service.list("alice", "demo", limit=1)) == 1
    assert len(service.list("alice", "demo", limit=100)) == 100
    assert len(service.list("alice", "demo")) == 20
    assert service.list("alice", "demo", after_id=0, status=None, limit=100)[0]["id"] == 1


# ---- 并发 ----

def race(workers, job):
    """用屏障让所有线程同时开跑，收集每个线程的结果或异常。"""
    barrier = threading.Barrier(workers)
    results = [None] * workers

    def run(index):
        barrier.wait()
        try:
            results[index] = job(index)
        except ServiceError as error:
            results[index] = (error.status, error.code)

    threads = [threading.Thread(target=run, args=(i,)) for i in range(workers)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return results


def test_concurrent_identical_creates_make_exactly_one_issue():
    service = make()
    results = race(64, lambda _: service.create("alice", "demo", {"title": "Bug"}, "retry"))
    assert sorted(status for status, _ in results).count(201) == 1
    assert sorted(status for status, _ in results).count(200) == 63
    assert len({body["id"] for _, body in results}) == 1
    assert len(service.list("alice", "demo")) == 1
    assert new(service)["id"] == 2


def test_concurrent_creates_without_keys_get_dense_unique_ids():
    service = make()
    results = race(64, lambda i: service.create("alice", "demo", {"title": f"t{i}"}))
    assert sorted(body["id"] for _, body in results) == list(range(1, 65))
    assert [row["id"] for row in service.list("alice", "demo", limit=100)] == list(range(1, 65))


def test_concurrent_conflicting_payloads_under_one_key_admit_one_winner():
    service = make()
    results = race(32, lambda i: service.create("alice", "demo", {"title": f"t{i % 2}"}, "k"))
    statuses = [r[0] for r in results]
    assert statuses.count(201) == 1
    assert set(statuses) <= {201, 200, 409}
    assert len(service.list("alice", "demo")) == 1


def test_concurrent_transitions_at_one_version_change_the_status_once():
    service = make()
    issue = new(service)
    results = race(48, lambda i: service.transition("bob" if i % 2 else "alice", "demo", 1, "closed", 1))
    wins = [r for r in results if isinstance(r, dict)]
    assert len(wins) == 1                                   # 抢到版本 1 的只有一个
    assert results.count((409, "version_conflict")) == 47   # 其余都看到版本已经是 2
    assert all(w == {**issue, "status": "closed", "version": 2} for w in wins)
    assert service.get("alice", "demo", 1)["version"] == 2


def test_concurrent_opposite_transitions_end_in_one_deterministic_state():
    # 同一版本 1 上，"改成 closed"和"保持 open"同时到达：
    # 先 closed 后 open → open 请求版本过期（409）；先 open 后 closed → 两个都成功。两种顺序的终态相同。
    service = make()
    new(service)
    results = race(2, lambda i: service.transition("alice", "demo", 1, ("closed", "open")[i], 1))
    assert results.count((409, "version_conflict")) <= 1
    assert sum(isinstance(r, dict) for r in results) >= 1
    final = service.get("alice", "demo", 1)
    assert (final["status"], final["version"]) == ("closed", 2)


def test_readers_never_see_a_torn_issue():
    service = make()
    new(service)
    stop = threading.Event()
    torn = []

    def writer():
        version = 1
        while not stop.is_set():
            status = "closed" if version % 2 else "open"
            version = service.transition("alice", "demo", 1, status, version)["version"]

    def reader():
        for _ in range(2000):
            issue = service.get("bob", "demo", 1)
            # 版本为奇数 ⇔ 打开状态（初始 v1 是 open，每次改状态加一）
            if (issue["version"] % 2 == 1) != (issue["status"] == "open"):
                torn.append(issue)

    thread = threading.Thread(target=writer)
    thread.start()
    reader()
    stop.set()
    thread.join()
    assert torn == []
