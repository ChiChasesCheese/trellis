"""ScreenShelf 片单服务的测试：覆盖六条产品规则；同一套测试跑参考解（IMPL=solution）和待修复的起始代码（IMPL=starter）。"""

import importlib
import os
import random
import threading

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))
ServiceError = impl.ServiceError


@pytest.fixture
def svc():
    service = impl.WatchlistService(":memory:")
    yield service
    service.close()


@pytest.fixture
def db_path(tmp_path):
    return str(tmp_path / "shelf.db")


def fails(status, code, fn, *args):
    with pytest.raises(ServiceError) as caught:
        fn(*args)
    assert (caught.value.status, caught.value.code) == (status, code)


def new_list(service, user="ann", name="Sunday picks"):
    return service.create(user, name)[1]["id"]


# ---- 规则 1：名字与电影 id ----------------------------------------------------------------

def test_names_are_stripped_before_storing(svc):
    status, made = svc.create("ann", "   Rainy day \t")
    assert (status, made["name"]) == (201, "Rainy day")
    assert svc.get("ann", made["id"])["name"] == "Rainy day"
    assert svc.rename("ann", made["id"], "  Sunny  ")[1]["name"] == "Sunny"


@pytest.mark.parametrize("bad", ["", "   ", "\n\t", "x" * 81, "  " + "y" * 81 + "  ", None, 7, ["a"], b"abc"])
def test_invalid_names_are_rejected_on_create_and_rename(svc, bad):
    fails(400, "invalid_name", svc.create, "ann", bad)
    list_id = new_list(svc)
    fails(400, "invalid_name", svc.rename, "ann", list_id, bad)
    assert svc.get("ann", list_id)["name"] == "Sunday picks"


def test_name_length_counts_characters_after_strip(svc):
    assert svc.create("ann", "  " + "z" * 80 + "  ")[1]["name"] == "z" * 80
    assert svc.create("ann", "片" * 80)[0] == 201
    fails(400, "invalid_name", svc.create, "ann", "片" * 81)
    assert svc.create("ann", "a")[0] == 201


@pytest.mark.parametrize("bad", [0, -4, 2**31, True, False, 3.0, "8", None, [1]])
def test_invalid_movie_ids(svc, bad):
    list_id = new_list(svc)
    fails(400, "invalid_movie", svc.add_movie, "ann", list_id, bad)
    fails(400, "invalid_movie", svc.remove_movie, "ann", list_id, bad)
    assert svc.get("ann", list_id)["movies"] == []


def test_movie_id_bounds_are_inclusive(svc):
    list_id = new_list(svc)
    assert svc.add_movie("ann", list_id, 1)[0] == 201
    assert svc.add_movie("ann", list_id, 2147483647)[0] == 201
    assert svc.get("ann", list_id)["movies"] == [1, 2147483647]


# ---- 规则 2：创建、读取、改名 -------------------------------------------------------------

def test_readme_style_walkthrough(svc):
    status, made = svc.create("ann", "Late shows")
    assert status == 201
    assert made == {"id": 1, "owner": "ann", "name": "Late shows", "movies": []}
    status, after = svc.add_movie("ann", made["id"], 31)
    assert (status, after["movies"]) == (201, [31])
    again_status, again = svc.add_movie("ann", made["id"], 31)
    assert (again_status, again) == (200, after)


def test_ids_start_at_one_and_are_never_reused(svc):
    first, second = new_list(svc), new_list(svc)
    assert (first, second) == (1, 2)
    assert svc.delete("ann", second) == (204, None)
    assert new_list(svc) == 3


def test_duplicate_names_are_allowed_and_get_distinct_ids(svc):
    a, b = new_list(svc, "ann", "Same"), new_list(svc, "ann", "Same")
    assert a != b
    assert svc.get("ann", a)["name"] == svc.get("ann", b)["name"] == "Same"


def test_get_returns_unique_movies_in_ascending_order(svc):
    list_id = new_list(svc)
    for movie in (30, 10, 20, 10):
        svc.add_movie("ann", list_id, movie)
    assert svc.get("ann", list_id)["movies"] == [10, 20, 30]


def test_rename_returns_the_updated_list(svc):
    list_id = new_list(svc)
    svc.add_movie("ann", list_id, 5)
    assert svc.rename("ann", list_id, "Renamed") == (
        200,
        {"id": list_id, "owner": "ann", "name": "Renamed", "movies": [5]},
    )


def test_returned_data_is_detached(svc):
    list_id = new_list(svc)
    _, added = svc.add_movie("ann", list_id, 9)
    added["movies"].append(99)
    added["name"] = "hacked"
    fetched = svc.get("ann", list_id)
    fetched["movies"].clear()
    assert svc.get("ann", list_id) == {"id": list_id, "owner": "ann", "name": "Sunday picks", "movies": [9]}


# ---- 规则 3：归属与校验顺序 ---------------------------------------------------------------

def test_missing_and_foreign_lists_look_the_same_for_every_operation(svc):
    mine = new_list(svc, "ann")
    svc.add_movie("ann", mine, 7)
    calls = [
        (svc.get, ()), (svc.rename, ("new name",)), (svc.delete, ()),
        (svc.add_movie, (8,)), (svc.remove_movie, (7,)),
    ]
    for fn, extra in calls:
        fails(404, "list_not_found", fn, "ben", mine, *extra)  # 别人的
        fails(404, "list_not_found", fn, "ben", 999, *extra)  # 不存在
    assert svc.get("ann", mine) == {"id": mine, "owner": "ann", "name": "Sunday picks", "movies": [7]}


def test_user_ids_are_not_normalised(svc):
    mine = new_list(svc, "Ann")
    fails(404, "list_not_found", svc.get, "ann", mine)
    fails(404, "list_not_found", svc.get, "Ann ", mine)
    assert svc.get("Ann", mine)["owner"] == "Ann"


def test_validation_comes_before_ownership(svc):
    mine = new_list(svc, "ann")
    fails(400, "invalid_name", svc.rename, "ben", mine, "  ")
    fails(400, "invalid_name", svc.rename, "ben", 999, "")
    fails(400, "invalid_movie", svc.add_movie, "ben", mine, 0)
    fails(400, "invalid_movie", svc.remove_movie, "ben", 999, True)


def test_list_is_checked_before_movie_membership(svc):
    mine = new_list(svc, "ann")
    svc.add_movie("ann", mine, 7)
    fails(404, "list_not_found", svc.remove_movie, "ben", mine, 7)
    fails(404, "movie_not_found", svc.remove_movie, "ann", mine, 8)


def test_rejected_operations_change_nothing(svc):
    mine = new_list(svc, "ann")
    svc.add_movie("ann", mine, 4)
    before_count = svc.membership_count
    fails(404, "list_not_found", svc.add_movie, "ben", mine, 5)
    fails(404, "list_not_found", svc.rename, "ben", mine, "stolen")
    fails(404, "list_not_found", svc.delete, "ben", mine)
    fails(404, "movie_not_found", svc.remove_movie, "ann", mine, 6)
    fails(400, "invalid_name", svc.rename, "ann", mine, "")
    assert svc.membership_count == before_count
    assert svc.get("ann", mine) == {"id": mine, "owner": "ann", "name": "Sunday picks", "movies": [4]}


# ---- 规则 4：成员与删除 -------------------------------------------------------------------

def test_first_add_is_201_and_repeat_is_200_with_the_same_list(svc):
    list_id = new_list(svc)
    status, first = svc.add_movie("ann", list_id, 12)
    again_status, again = svc.add_movie("ann", list_id, 12)
    assert (status, again_status) == (201, 200)
    assert again == first and again["movies"] == [12]
    assert svc.membership_count == 1


def test_membership_is_scoped_to_one_list(svc):
    a, b = new_list(svc, "ann", "A"), new_list(svc, "ann", "B")
    assert svc.add_movie("ann", a, 3)[0] == 201
    assert svc.add_movie("ann", b, 3)[0] == 201  # 同一部电影放进另一张单子仍是新增
    svc.remove_movie("ann", a, 3)
    assert svc.get("ann", a)["movies"] == [] and svc.get("ann", b)["movies"] == [3]


def test_remove_movie_removes_only_that_movie(svc):
    list_id = new_list(svc)
    for movie in (1, 2, 3):
        svc.add_movie("ann", list_id, movie)
    assert svc.remove_movie("ann", list_id, 2) == (204, None)
    assert svc.get("ann", list_id)["movies"] == [1, 3]
    fails(404, "movie_not_found", svc.remove_movie, "ann", list_id, 2)
    fails(404, "movie_not_found", svc.remove_movie, "ann", list_id, 99)
    assert svc.get("ann", list_id)["movies"] == [1, 3]


def test_delete_removes_only_the_requested_list_and_its_members(svc):
    target, sibling = new_list(svc, "ann", "T"), new_list(svc, "ann", "S")
    other = new_list(svc, "ben", "O")
    for list_id, movies in ((target, (1, 2)), (sibling, (3,)), (other, (4, 5))):
        for movie in movies:
            svc.add_movie("ann" if list_id != other else "ben", list_id, movie)
    assert svc.membership_count == 5
    assert svc.delete("ann", target) == (204, None)
    assert svc.membership_count == 3  # 目标的两条成员被带走，其他的原样
    assert svc.get("ann", sibling)["movies"] == [3]
    assert svc.get("ben", other)["movies"] == [4, 5]
    fails(404, "list_not_found", svc.get, "ann", target)
    fails(404, "list_not_found", svc.delete, "ann", target)


# ---- 规则 5：持久化与连接 -----------------------------------------------------------------

def test_second_instance_sees_every_committed_change(db_path):
    first, second = impl.WatchlistService(db_path), impl.WatchlistService(db_path)
    try:
        list_id = first.create("ann", "  Persisted ")[1]["id"]
        assert second.get("ann", list_id) == {"id": list_id, "owner": "ann", "name": "Persisted", "movies": []}
        first.add_movie("ann", list_id, 6)
        first.add_movie("ann", list_id, 8)
        assert second.get("ann", list_id)["movies"] == [6, 8]
        second.remove_movie("ann", list_id, 6)
        first.rename("ann", list_id, "Renamed")
        assert first.get("ann", list_id) == second.get("ann", list_id) == {
            "id": list_id, "owner": "ann", "name": "Renamed", "movies": [8],
        }
        second.delete("ann", list_id)
        fails(404, "list_not_found", first.get, "ann", list_id)
    finally:
        first.close()
        second.close()


def test_data_survives_close_and_reopen_and_ids_continue(db_path):
    service = impl.WatchlistService(db_path)
    kept = service.create("ann", "Kept")[1]["id"]
    service.add_movie("ann", kept, 11)
    gone = new_list(service, "ann", "Gone")
    service.delete("ann", gone)
    service.close()
    reopened = impl.WatchlistService(db_path)
    try:
        assert reopened.get("ann", kept)["movies"] == [11]
        fails(404, "list_not_found", reopened.get, "ann", gone)
        assert new_list(reopened, "ann", "Next") == gone + 1
    finally:
        reopened.close()


def test_separate_databases_are_isolated(tmp_path):
    one, two = impl.WatchlistService(str(tmp_path / "a.db")), impl.WatchlistService(str(tmp_path / "b.db"))
    memory_a, memory_b = impl.WatchlistService(":memory:"), impl.WatchlistService(":memory:")
    try:
        new_list(one)
        fails(404, "list_not_found", two.get, "ann", 1)
        new_list(memory_a)
        fails(404, "list_not_found", memory_b.get, "ann", 1)
    finally:
        for service in (one, two, memory_a, memory_b):
            service.close()


def test_close_can_be_called_twice(db_path):
    service = impl.WatchlistService(db_path)
    new_list(service)
    service.close()
    service.close()


# ---- 规则 5：串行化 -----------------------------------------------------------------------

def run_threads(count, work):
    barrier = threading.Barrier(count)
    results, errors = [], []

    def worker(index):
        barrier.wait()
        try:
            results.append(work(index))
        except Exception as exc:  # 记录下来，由断言报告
            errors.append(exc)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(count)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return results, errors


def test_same_movie_added_concurrently_inserts_exactly_once(db_path):
    service = impl.WatchlistService(db_path)
    try:
        list_id = new_list(service)
        results, errors = run_threads(8, lambda _: service.add_movie("ann", list_id, 77)[0])
        assert not errors
        assert sorted(results) == [200] * 7 + [201]
        assert service.get("ann", list_id)["movies"] == [77]
    finally:
        service.close()


def test_distinct_writes_from_many_threads_all_land(db_path):
    service = impl.WatchlistService(db_path)
    try:
        list_id = new_list(service)
        _, errors = run_threads(10, lambda i: service.add_movie("ann", list_id, 100 + i))
        assert not errors
        assert service.get("ann", list_id)["movies"] == list(range(100, 110))
        ids, errors = run_threads(10, lambda i: service.create("ben", f"list {i}")[1]["id"])
        assert not errors and len(set(ids)) == 10
    finally:
        service.close()


def test_two_instances_racing_on_one_file_still_insert_once(db_path):
    first, second = impl.WatchlistService(db_path), impl.WatchlistService(db_path)
    try:
        list_id = new_list(first)
        services = (first, second)
        results, errors = run_threads(8, lambda i: services[i % 2].add_movie("ann", list_id, 55)[0])
        assert not errors
        assert sorted(results) == [200] * 7 + [201]
    finally:
        first.close()
        second.close()


# ---- 对拍：同一串随机操作，服务与一个纯字典模型必须给出同样的结果 -------------------------------

def model_step(model, op, user, list_id, arg):
    """模型：{id: [owner, name, set(movies)]}；返回 (状态, 片单或 None) 或抛出错误码。"""
    entry = model.get(list_id)
    if op == "add" or op == "remove":
        if not (type(arg) is int and 1 <= arg <= 2147483647):
            return ("err", 400, "invalid_movie")
    if entry is None or entry[0] != user:
        return ("err", 404, "list_not_found")
    if op == "get":
        return (200, sorted(entry[2]))
    if op == "add":
        fresh = arg not in entry[2]
        entry[2].add(arg)
        return (201 if fresh else 200, sorted(entry[2]))
    if op == "remove":
        if arg not in entry[2]:
            return ("err", 404, "movie_not_found")
        entry[2].discard(arg)
        return (204, None)
    del model[list_id]
    return (204, None)


@pytest.mark.parametrize("seed", range(6))
def test_random_operations_match_a_plain_dict_model(seed):
    rng = random.Random(seed)
    service = impl.WatchlistService(":memory:")
    model = {}
    next_id = 1
    try:
        for _ in range(300):
            user = rng.choice(["ann", "ben", "cy"])
            if not model or rng.random() < 0.15:
                made = service.create(user, f"list {next_id}")[1]
                model[made["id"]] = [user, made["name"], set()]
                assert made["id"] == next_id
                next_id += 1
                continue
            list_id = rng.choice(list(model) + [next_id + 5])
            op = rng.choice(["get", "add", "add", "remove", "delete"])
            arg = rng.choice([1, 2, 3, 4, 5, 0, True])
            expected = model_step(model, op, user, list_id, arg)
            try:
                if op == "get":
                    got = (200, service.get(user, list_id)["movies"])
                elif op == "add":
                    status, row = service.add_movie(user, list_id, arg)
                    got = (status, row["movies"])
                elif op == "remove":
                    got = service.remove_movie(user, list_id, arg)
                else:
                    got = service.delete(user, list_id)
            except ServiceError as failure:
                got = ("err", failure.status, failure.code)
            assert got == expected
        assert service.membership_count == sum(len(entry[2]) for entry in model.values())
    finally:
        service.close()


# ---- 规则 6：HTTP 适配器 ------------------------------------------------------------------

def test_http_requires_a_user_header(svc):
    for user in (None, "", "   ", 5):
        assert impl.dispatch(svc, "POST", "/watchlists", user, {"name": "x"}) == (401, {"error": "unauthorized"})
    assert impl.dispatch(svc, "GET", "/nowhere", None) == (401, {"error": "unauthorized"})  # 401 先于 404


def test_http_full_flow(svc):
    status, made = impl.dispatch(svc, "POST", "/watchlists", "ann", {"name": " Tonight "})
    assert (status, made["name"]) == (201, "Tonight")
    base = f"/watchlists/{made['id']}"
    assert impl.dispatch(svc, "POST", base + "/movies", "ann", {"movie_id": 14})[0] == 201
    assert impl.dispatch(svc, "POST", base + "/movies", "ann", {"movie_id": 14})[0] == 200
    assert impl.dispatch(svc, "GET", base, "ann") == (
        200, {"id": made["id"], "owner": "ann", "name": "Tonight", "movies": [14]},
    )
    assert impl.dispatch(svc, "PATCH", base, "ann", {"name": "Late"})[1]["name"] == "Late"
    assert impl.dispatch(svc, "DELETE", base + "/movies/14", "ann") == (204, None)
    assert impl.dispatch(svc, "DELETE", base + "/movies/14", "ann") == (404, {"error": "movie_not_found"})
    assert impl.dispatch(svc, "DELETE", base, "ann") == (204, None)
    assert impl.dispatch(svc, "GET", base, "ann") == (404, {"error": "list_not_found"})


def test_http_other_users_get_not_found_and_service_errors_become_bodies(svc):
    list_id = new_list(svc, "ann")
    base = f"/watchlists/{list_id}"
    assert impl.dispatch(svc, "GET", base, "ben") == (404, {"error": "list_not_found"})
    assert impl.dispatch(svc, "PATCH", base, "ben", {"name": "x"}) == (404, {"error": "list_not_found"})
    assert impl.dispatch(svc, "POST", "/watchlists", "ann", {"name": "  "}) == (400, {"error": "invalid_name"})
    assert impl.dispatch(svc, "POST", base + "/movies", "ann", {"movie_id": True}) == (400, {"error": "invalid_movie"})
    assert impl.dispatch(svc, "DELETE", base + "/movies/2147483648", "ann") == (400, {"error": "invalid_movie"})


def test_http_route_method_and_body_errors(svc):
    list_id = new_list(svc, "ann")
    base = f"/watchlists/{list_id}"
    for path in ("/", "/watchlist", "/watchlists/0", "/watchlists/007", "/watchlists/abc", base + "/movies/x", base + "/film"):
        assert impl.dispatch(svc, "GET", path, "ann") == (404, {"error": "not_found"}), path
    too_big = "/watchlists/" + str(2**63)
    assert impl.dispatch(svc, "GET", too_big, "ann") == (404, {"error": "not_found"})
    assert impl.dispatch(svc, "GET", "/watchlists/" + "9" * 5000, "ann") == (404, {"error": "not_found"})
    assert impl.dispatch(svc, "GET", "/watchlists/" + str(2**63 - 1), "ann") == (404, {"error": "list_not_found"})
    for method, path in (("GET", "/watchlists"), ("PUT", base), ("POST", base), ("GET", base + "/movies"),
                         ("DELETE", base + "/movies"), ("GET", base + "/movies/3"), ("POST", base + "/movies/3")):
        assert impl.dispatch(svc, method, path, "ann", {}) == (405, {"error": "method_not_allowed"}), (method, path)
    for body in (None, {}, [], "x", {"name": "a", "extra": 1}, {"title": "a"}):
        assert impl.dispatch(svc, "POST", "/watchlists", "ann", body) == (400, {"error": "invalid_input"}), body
        assert impl.dispatch(svc, "PATCH", base, "ann", body) == (400, {"error": "invalid_input"}), body
    for body in (None, {}, {"movie_id": 1, "x": 2}, {"id": 1}):
        assert impl.dispatch(svc, "POST", base + "/movies", "ann", body) == (400, {"error": "invalid_input"}), body
