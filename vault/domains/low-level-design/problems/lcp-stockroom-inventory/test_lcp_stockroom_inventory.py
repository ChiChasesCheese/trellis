import importlib
import json
import os
import threading
from decimal import Decimal

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))
Response = impl.Response


def make():
    return impl.InventoryService(impl.initialize_items())


def err(status, code):
    return Response(status, {"error": code})


def create(service, user="alice", sku="BOOK-1", name="Book", quantity=3):
    response = service.handle("POST", "/items", user, {"sku": sku, "name": name, "quantity": quantity})
    assert response.status == 201, response
    return response.body


def path_of(item):
    return "/items/" + item["id"]


def patch(service, item, user="alice", **body):
    return service.handle("PATCH", path_of(item), user, body)


def run_threads(count, work):
    """count 个线程在屏障处同时起跑，返回各自的结果。"""
    barrier = threading.Barrier(count)
    results = [None] * count

    def worker(index):
        barrier.wait()
        results[index] = work(index)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(count)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return results


# ---- 端到端的例子与身份、路由 ----

def test_create_then_read_back_roundtrip():
    service = make()
    reply = service.handle("POST", "/items", "dana", {"sku": "TOOL-9", "name": "Hammer", "quantity": 7})
    assert reply.status == 201
    stored = reply.body
    assert set(stored) == {"id", "owner", "sku", "name", "quantity", "version"}
    assert (stored["owner"], stored["quantity"], stored["version"]) == ("dana", 7, 1)
    assert service.handle("GET", "/items/" + stored["id"], "dana").body == stored


@pytest.mark.parametrize("user", [None, "", "   ", "\t\n", "\u00a0\ufeff\u3000", 7, ["alice"]])
def test_bad_identity_is_401_before_route_id_and_method(user):
    service = make()
    for method, path in [("GET", "/items"), ("POST", "/items"), ("GET", "/nope"), ("GET", "/items/zz"), ("PUT", "/items")]:
        assert service.handle(method, path, user, {}) == err(401, "unauthorized")


def test_identity_is_kept_exactly_including_spaces():
    service = make()
    padded = create(service, user=" alice ", sku="PAD")
    assert padded["owner"] == " alice "
    assert service.handle("GET", path_of(padded), "alice") == err(404, "item_not_found")
    assert service.handle("GET", path_of(padded), " alice ").body == padded


@pytest.mark.parametrize("path", ["/", "/item", "/items/", "/items/abc/def", "/other/1", "items", "/items//"])
def test_unknown_paths_are_404(path):
    assert make().handle("GET", path, "alice") == err(404, "not_found")


@pytest.mark.parametrize("item_id", ["abc", "g" * 24, "a" * 23, "a" * 25, "a" * 23 + "\n", "é" * 24])
def test_malformed_id_is_400_for_every_method_even_unsupported_ones(item_id):
    service = make()
    for method in ("GET", "PATCH", "DELETE", "POST", "PUT"):
        assert service.handle(method, "/items/" + item_id, "alice", {}) == err(400, "invalid_id")


def test_unsupported_methods_are_405_after_id_validation():
    service = make()
    item = create(service)
    for method, path in [("PUT", "/items"), ("DELETE", "/items"), ("PATCH", "/items"), ("POST", path_of(item)),
                         ("PUT", path_of(item)), ("HEAD", "/items")]:
        assert service.handle(method, path, "alice", {}) == err(405, "method_not_allowed")


def test_ids_are_lowercase_and_accepted_in_either_case():
    service = make()
    item = create(service)
    assert len(item["id"]) == 24 and item["id"] == item["id"].lower()
    assert all(c in "0123456789abcdef" for c in item["id"])
    upper = service.handle("GET", "/items/" + item["id"].upper(), "alice")
    assert upper.status == 200 and upper.body == item
    assert service.handle("DELETE", "/items/" + item["id"].upper(), "alice") == Response(204, None)
    assert service.handle("GET", path_of(item), "alice").status == 404


# ---- 创建 ----

@pytest.mark.parametrize(
    "body",
    [None, [], "x", 5, {}, {"sku": "A", "name": "n"}, {"sku": "A", "quantity": 1},
     {"name": "n", "quantity": 1}, {"sku": "A", "name": "n", "quantity": 1, "owner": "bob"},
     {"sku": "A", "name": "n", "quantity": 1, "id": "a" * 24}, {"sku": "A", "name": "n", "quantity": 1, "version": 5}],
)
def test_create_needs_exactly_three_fields(body):
    service = make()
    assert service.handle("POST", "/items", "alice", body) == err(400, "invalid_input")
    assert service.handle("GET", "/items", "alice").body == []


@pytest.mark.parametrize("sku", ["", "abc", "A B", "A_B", "A" * 25, "ABC\n", "ÅB", None, 7, ["A"], b"A"])
def test_bad_sku_is_rejected(sku):
    assert make().handle("POST", "/items", "alice", {"sku": sku, "name": "n", "quantity": 1}) == err(400, "invalid_input")


@pytest.mark.parametrize("sku", ["A", "0", "-", "A-1-B", "Z" * 24])
def test_good_sku_is_accepted(sku):
    assert create(make(), sku=sku)["sku"] == sku


@pytest.mark.parametrize(
    "quantity",
    [-1, 1000001, "3", True, False, None, 2.5, Decimal("2.5"), float("nan"), float("inf"), Decimal("NaN"), [3], 10**30],
)
def test_bad_quantity_is_rejected_not_defaulted_to_zero(quantity):
    service = make()
    assert service.handle("POST", "/items", "alice", {"sku": "A", "name": "n", "quantity": quantity}) == err(400, "invalid_input")
    assert service.handle("GET", "/items", "alice").body == []


@pytest.mark.parametrize("quantity", [0, 1000000, 3.0, Decimal("3"), Decimal("3.000"), Decimal("1E+3")])
def test_integral_numbers_are_accepted_and_stored_as_ints(quantity):
    item = create(make(), quantity=quantity)
    assert item["quantity"] == int(quantity) and type(item["quantity"]) is int and type(item["version"]) is int


@pytest.mark.parametrize("name", [None, 5, ["n"], "", "   ", "\ufeff", "\u2028\u3000", "a" * 81, "😀" * 41, "a" * 79 + "😀"])
def test_bad_name_is_rejected(name):
    assert make().handle("POST", "/items", "alice", {"sku": "A", "name": name, "quantity": 1}) == err(400, "invalid_input")


def test_name_length_counts_utf16_units_after_trimming():
    service = make()
    assert create(service, sku="A", name="a" * 80)["name"] == "a" * 80
    assert create(service, sku="B", name="😀" * 40)["name"] == "😀" * 40  # 每个占两个码元，共 80
    assert create(service, sku="C", name="  " + "b" * 80 + "\u3000")["name"] == "b" * 80  # 空白不算长度
    assert create(service, sku="D", name="é")["name"] == "é"


def test_name_is_trimmed_with_ecmascript_whitespace_only():
    service = make()
    assert create(service, sku="A", name="\u00a0\ufeff x y \u2029")["name"] == "x y"
    # \x85 与 \x1f 不在 ECMAScript 空白里：Python 的 str.strip() 会剥，这里不能剥
    assert create(service, sku="B", name="\x85z\x1f")["name"] == "\x85z\x1f"


def test_lone_surrogate_in_name_is_bad_input_not_a_crash():
    service = make()
    assert service.handle("POST", "/items", "alice", {"sku": "A", "name": "x\ud800", "quantity": 1}) == err(400, "invalid_input")
    item = create(service, sku="B")
    assert patch(service, item, version=1, name="\udfff") == err(400, "invalid_input")
    assert service.handle("GET", path_of(item), "alice").body == item


def test_create_is_persisted_and_returns_what_was_stored():
    service = make()
    body = {"sku": "BOOK-1", "name": " Book ", "quantity": 3}
    created = service.handle("POST", "/items", "alice", body)
    assert body == {"sku": "BOOK-1", "name": " Book ", "quantity": 3}  # 请求体原样，没被改写
    assert created.body["name"] == "Book" and created.body["version"] == 1
    assert service.handle("GET", path_of(created.body), "alice").body == created.body
    assert service.handle("GET", "/items", "alice").body == [created.body]
    again = service.handle("POST", "/items", "bob", body)
    assert again.body["id"] != created.body["id"]


def test_every_response_body_is_json_serializable_with_plain_ints():
    service = make()
    item = create(service, quantity=Decimal("7"))
    responses = [
        service.handle("GET", "/items", "alice"), service.handle("GET", path_of(item), "alice"),
        patch(service, item, version=Decimal("1"), quantity=Decimal("9")), patch(service, item, version=1, quantity=1),
        service.handle("GET", "/items/" + "0" * 24, "alice"),
    ]
    for response in responses:
        json.dumps(response.body)
    assert responses[2].body["quantity"] == 9 and type(responses[2].body["quantity"]) is int


# ---- 读与删：按所有者限定 ----

def test_list_is_scoped_to_the_owner_and_sorted_by_sku():
    service = make()
    skus = ["B", "A-2", "A1", "A", "10", "Z-9"]
    for sku in skus:
        create(service, sku=sku)
    create(service, user="bob", sku="AAA")
    listed = service.handle("GET", "/items", "alice")
    assert listed.status == 200
    assert [item["sku"] for item in listed.body] == sorted(skus)
    assert {item["owner"] for item in listed.body} == {"alice"}
    assert service.handle("GET", "/items", "nobody") == Response(200, [])


def test_other_users_items_are_invisible_and_untouched():
    service = make()
    item = create(service)
    path = path_of(item)
    assert service.handle("GET", path, "bob") == err(404, "item_not_found")
    assert service.handle("DELETE", path, "bob") == err(404, "item_not_found")
    assert service.handle("PATCH", path, "bob", {"version": 1, "name": "Mine"}) == err(404, "item_not_found")
    assert service.handle("PATCH", path, "bob", {"version": 99, "name": "Mine"}) == err(404, "item_not_found")
    assert service.handle("GET", path, "alice").body == item  # 一个字段、版本号都没动


def test_delete_returns_204_once_then_404_and_frees_the_sku():
    service = make()
    item = create(service)
    assert service.handle("DELETE", path_of(item), "alice") == Response(204, None)
    assert service.handle("DELETE", path_of(item), "alice") == err(404, "item_not_found")
    assert service.handle("GET", path_of(item), "alice") == err(404, "item_not_found")
    assert create(service)["id"] != item["id"]  # 同一个 sku 可以重新建


# ---- 更新 ----

def test_update_returns_the_new_document_and_bumps_the_version():
    service = make()
    item = create(service)
    updated = patch(service, item, version=1, name="  New  ", quantity=0)
    assert updated.status == 200
    assert updated.body == {**item, "name": "New", "quantity": 0, "version": 2}
    assert service.handle("GET", path_of(item), "alice").body == updated.body
    only_name = patch(service, item, version=2, name="Other")
    assert only_name.body == {**updated.body, "name": "Other", "version": 3}
    only_quantity = patch(service, item, version=3, quantity=9)
    assert only_quantity.body == {**only_name.body, "quantity": 9, "version": 4}


def test_unchanged_values_still_bump_the_version():
    service = make()
    item = create(service)
    same = patch(service, item, version=1, name="Book", quantity=3)
    assert same.body == {**item, "version": 2}


def test_version_accepts_integral_float_and_decimal():
    service = make()
    item = create(service)
    assert patch(service, item, version=1.0, quantity=1).body["version"] == 2
    assert patch(service, item, version=Decimal("2"), quantity=2).body["version"] == 3


@pytest.mark.parametrize("version", [None, 0, -1, True, "1", 1.5, Decimal("1.5"), float("nan"), 9223372036854775807, [1]])
def test_bad_version_is_400(version):
    service = make()
    item = create(service)
    assert patch(service, item, version=version, quantity=5) == err(400, "invalid_input")
    assert service.handle("GET", path_of(item), "alice").body == item


@pytest.mark.parametrize(
    "body",
    [None, [], "x", {}, {"version": 1}, {"quantity": 5}, {"name": "n"},
     {"version": 1, "sku": "NEW"}, {"version": 1, "owner": "bob", "quantity": 1}, {"version": 1, "id": "a" * 24, "quantity": 1},
     {"version": 1, "name": "   "}, {"version": 1, "name": 5}, {"version": 1, "name": "a" * 81},
     {"version": 1, "quantity": -1}, {"version": 1, "quantity": 1000001}, {"version": 1, "quantity": True},
     {"version": 1, "quantity": 2.5}, {"version": 1, "name": "ok", "quantity": "5"}],
)
def test_bad_update_body_is_400_and_leaves_the_item_alone(body):
    service = make()
    item = create(service)
    assert service.handle("PATCH", path_of(item), "alice", body) == err(400, "invalid_input")
    assert service.handle("GET", path_of(item), "alice").body == item


def test_update_checks_input_then_item_then_version():
    service = make()
    item = create(service)
    missing = "/items/" + "0" * 24
    assert service.handle("PATCH", missing, "alice", {"version": 1, "quantity": -1}) == err(400, "invalid_input")
    assert service.handle("PATCH", missing, "alice", {"version": 1, "quantity": 1}) == err(404, "item_not_found")
    assert patch(service, item, version=7, quantity=1) == err(409, "version_conflict")
    assert patch(service, item, user="bob", version=7, quantity=-1) == err(400, "invalid_input")
    assert patch(service, item, user="bob", version=7, quantity=1) == err(404, "item_not_found")


def test_failed_updates_change_nothing_not_even_the_version():
    service = make()
    item = create(service)
    assert patch(service, item, version=2, name="X", quantity=9) == err(409, "version_conflict")
    assert patch(service, item, version=1, name="X", quantity=2000000) == err(400, "invalid_input")
    assert service.handle("GET", path_of(item), "alice").body == item
    assert patch(service, item, version=1, name="X").body["version"] == 2  # 版本 1 仍然有效


def test_update_never_touches_owner_sku_or_id():
    service = make()
    item = create(service)
    updated = patch(service, item, version=1, name="Z", quantity=1).body
    assert (updated["id"], updated["owner"], updated["sku"]) == (item["id"], "alice", "BOOK-1")


# ---- 唯一与存储错误 ----

def test_duplicate_sku_is_409_without_a_new_document():
    service = make()
    first = create(service, sku="DUP", name="First")
    duplicate = service.handle("POST", "/items", "alice", {"sku": "DUP", "name": "Second", "quantity": 9})
    assert duplicate == err(409, "sku_conflict")
    assert service.handle("GET", "/items", "alice").body == [first]
    assert create(service, user="bob", sku="DUP")["owner"] == "bob"  # 别的所有者可以用
    assert service.handle("POST", "/items", "alice", {"sku": "DUP", "name": "", "quantity": 1}) == err(400, "invalid_input")


def broken(error, operation, collection=None):
    """让集合的 operation 这一个操作抛出指定的存储错误（其余照常）。"""
    collection = collection or impl.initialize_items()

    def fail(*_args, **_kwargs):
        raise error

    setattr(collection, operation, fail)
    return collection


@pytest.mark.parametrize(
    "error, expected",
    [(impl.DuplicateKeyError("E11000 secret index"), err(409, "sku_conflict")),
     (impl.SchemaViolation("Document failed validation"), err(400, "invalid_input")),
     (impl.StoreError("connection refused to db-7:27017"), err(503, "storage_unavailable"))],
)
def test_storage_errors_map_by_code_without_leaking_details(error, expected):
    for operation, method, path, body in [
        ("insert", "POST", "/items", {"sku": "A", "name": "n", "quantity": 1}),
        ("find", "GET", "/items", None),
        ("find_one", "GET", "/items/" + "a" * 24, None),
        ("delete_one", "DELETE", "/items/" + "a" * 24, None),
        ("find_one_and_update", "PATCH", "/items/" + "a" * 24, {"version": 1, "quantity": 1}),
    ]:
        service = impl.InventoryService(broken(error, operation))
        response = service.handle(method, path, "alice", body)
        assert response == expected, operation
        assert set(response.body) == {"error"}


def test_a_storage_failure_on_create_leaves_nothing_behind():
    collection = impl.initialize_items()
    service = impl.InventoryService(broken(impl.StoreError("down"), "insert", collection))
    assert service.handle("POST", "/items", "alice", {"sku": "A", "name": "n", "quantity": 1}) == err(503, "storage_unavailable")
    del collection.insert  # 故障排除
    assert service.handle("GET", "/items", "alice").body == []
    assert create(service, sku="A")["version"] == 1


# ---- 并发 ----

def test_concurrent_patches_on_one_version_succeed_exactly_once():
    service = make()
    item = create(service)
    results = run_threads(16, lambda i: patch(service, item, version=1, quantity=i))
    assert sorted(r.status for r in results) == [200] + [409] * 15
    final = service.handle("GET", path_of(item), "alice").body
    winner = next(r for r in results if r.status == 200)
    assert final == winner.body and final["version"] == 2


def test_separate_service_instances_on_one_database_also_allow_one_winner(tmp_path):
    database = str(tmp_path / "stock.db")
    first = impl.InventoryService(impl.initialize_items(database))
    item = create(first)
    services = [impl.InventoryService(impl.initialize_items(database)) for _ in range(4)]
    results = run_threads(12, lambda i: patch(services[i % 4], item, version=1, name=f"N{i}"))
    assert sorted(r.status for r in results) == [200] + [409] * 11
    assert first.handle("GET", path_of(item), "alice").body["version"] == 2


def test_concurrent_creates_of_one_sku_yield_one_item():
    service = make()
    results = run_threads(16, lambda i: service.handle("POST", "/items", "alice", {"sku": "RACE", "name": f"n{i}", "quantity": i}))
    assert sorted(r.status for r in results) == [201] + [409] * 15
    assert len(service.handle("GET", "/items", "alice").body) == 1


def test_concurrent_creates_of_different_skus_lose_nothing():
    service = make()
    results = run_threads(20, lambda i: service.handle("POST", "/items", f"user{i % 2}", {"sku": f"S{i}", "name": "n", "quantity": i}))
    assert all(r.status == 201 for r in results)
    assert sum(len(service.handle("GET", "/items", f"user{u}").body) for u in (0, 1)) == 20


def test_concurrent_version_chain_never_skips_or_repeats_a_version():
    service = make()
    item = create(service, quantity=0)

    def climb(_index):
        won = 0
        for _ in range(25):
            current = service.handle("GET", path_of(item), "alice").body
            response = patch(service, item, version=current["version"], quantity=current["quantity"] + 1)
            won += response.status == 200
        return won

    wins = sum(run_threads(6, climb))
    final = service.handle("GET", path_of(item), "alice").body
    assert final["version"] == 1 + wins and final["quantity"] == wins  # 每次成功恰好加一，没有丢更新
