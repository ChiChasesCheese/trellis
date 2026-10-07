import base64

from conftest import load_uploads, upload
from filevault import metrics
from filevault.api.testing import TestClient


def test_upload_returns_record(client):
    resp = upload(client, "a.txt", b"hello", "text/plain")
    assert resp.status_code == 201
    body = resp.json
    assert body["filename"] == "a.txt" and body["size"] == 5 and body["content_type"] == "text/plain"
    assert "blob_path" not in body and "owner" not in body


def test_download_returns_bytes_and_type(client):
    file_id = upload(client, "a.bin", b"\x00\x01\x02", "application/octet-stream").json["id"]
    resp = client.get(f"/files/{file_id}/content")
    assert resp.status_code == 200
    assert resp.body == b"\x00\x01\x02"
    assert resp.headers["Content-Type"] == "application/octet-stream"


def test_metadata_endpoint(client):
    file_id = upload(client, "a.txt", b"hi").json["id"]
    assert client.get(f"/files/{file_id}").json["filename"] == "a.txt"


def test_delete_removes_file(client, app):
    file_id = upload(client, "a.txt", b"hi").json["id"]
    assert client.delete(f"/files/{file_id}").status_code == 204
    assert client.get(f"/files/{file_id}").status_code == 404
    assert app.store.paths() == []


def test_other_users_cannot_see_or_delete(app, client):
    file_id = upload(client, "secret.txt", b"mine").json["id"]
    bob = TestClient(app.wsgi, user="bob")
    assert bob.get(f"/files/{file_id}").status_code == 404
    assert bob.get(f"/files/{file_id}/content").status_code == 404
    assert bob.delete(f"/files/{file_id}").status_code == 404
    assert bob.get("/files").json["items"] == []
    assert client.get(f"/files/{file_id}").status_code == 200


def test_missing_user_header_is_401(app):
    assert TestClient(app.wsgi).get("/files").status_code == 401
    assert TestClient(app.wsgi, user="no spaces allowed").get("/files").status_code == 401


def test_bad_bodies_are_400_with_the_error_shape(client):
    for body in ({}, {"filename": "a"}, {"filename": "a", "content_base64": "%%%"}):
        resp = client.post("/files", body)
        assert resp.status_code == 400
        assert resp.json["error"]["code"] == "bad_request"
    assert client.post("/files", {"filename": "a/b", "content_base64": ""}).status_code == 400


def test_upload_over_max_size_is_413(app):
    small = TestClient(app.wsgi, user="alice")
    big = b"x" * (app.settings.max_upload_bytes + 1)
    resp = upload(small, "big.bin", big)
    assert resp.status_code == 413
    assert resp.json["error"]["details"]["limit"] == app.settings.max_upload_bytes


def test_unknown_route_and_method(client):
    assert client.get("/nope").status_code == 404
    assert client.request("PUT", "/files").status_code == 405


def test_list_paginates_newest_first(client, clock):
    ids = []
    for i in range(5):
        ids.append(upload(client, f"f{i}.txt", b"x").json["id"])
        clock.tick(seconds=1)
    first = client.get("/files", {"limit": 2}).json
    assert [i["id"] for i in first["items"]] == ids[::-1][:2]
    second = client.get("/files", {"limit": 2, "cursor": first["next_cursor"]}).json
    assert [i["id"] for i in second["items"]] == ids[::-1][2:4]
    last = client.get("/files", {"limit": 2, "cursor": second["next_cursor"]}).json
    assert [i["id"] for i in last["items"]] == ids[:1] and last["next_cursor"] is None


def test_list_rejects_bad_limit_and_cursor(client):
    assert client.get("/files", {"limit": 0}).status_code == 400
    assert client.get("/files", {"limit": "abc"}).status_code == 400
    resp = client.get("/files", {"cursor": "garbage"})
    assert resp.status_code == 400 and resp.json["error"]["details"]["field"] == "cursor"


def test_fixture_uploads_round_trip(app):
    clients: dict[str, TestClient] = {}
    for item in load_uploads():
        c = clients.setdefault(item["user"], TestClient(app.wsgi, user=item["user"]))
        assert upload(c, item["filename"], item["text"].encode(), item["content_type"]).status_code == 201
    assert len(clients["alice"].get("/files").json["items"]) == 6
    assert len(clients["bob"].get("/files").json["items"]) == 2
    assert metrics.snapshot()["uploads_total"] == 9


def test_upload_counts_metric(client):
    upload(client, "a.txt", b"1")
    upload(client, "b.txt", b"2")
    assert metrics.get("uploads_total") == 2


def test_content_is_base64_on_the_wire(client):
    payload = base64.b64encode(b"abc").decode()
    resp = client.post("/files", {"filename": "a", "content_base64": payload})
    assert resp.status_code == 201 and resp.json["content_type"] == "application/octet-stream"


def test_health_needs_no_user(app):
    resp = TestClient(app.wsgi).get("/health")
    assert resp.status_code == 200 and resp.json["status"] == "ok"


def test_invalid_content_type_is_400_naming_the_field(client):
    resp = upload(client, "a.txt", b"x", "not a media type")
    assert resp.status_code == 400
    assert resp.json["error"]["details"]["field"] == "content_type"


def test_unicode_filename_round_trips(client):
    file_id = upload(client, "报告 'final' (2).pdf", b"x", "application/pdf").json["id"]
    assert client.get(f"/files/{file_id}").json["filename"] == "报告 'final' (2).pdf"


def test_delete_twice_is_404(client):
    file_id = upload(client, "a.txt", b"x").json["id"]
    assert client.delete(f"/files/{file_id}").status_code == 204
    assert client.delete(f"/files/{file_id}").status_code == 404


def test_listing_is_per_user(app, client):
    upload(client, "mine.txt", b"x")
    bob = TestClient(app.wsgi, user="bob")
    upload(bob, "bobs.txt", b"y")
    assert [i["filename"] for i in client.get("/files").json["items"]] == ["mine.txt"]
    assert [i["filename"] for i in bob.get("/files").json["items"]] == ["bobs.txt"]


def test_same_content_twice_gives_two_records(client):
    a = upload(client, "a.txt", b"same").json
    b = upload(client, "b.txt", b"same").json
    assert a["id"] != b["id"]
    assert len(client.get("/files").json["items"]) == 2


def test_empty_upload_downloads_empty(client):
    file_id = upload(client, "empty", b"").json["id"]
    resp = client.get(f"/files/{file_id}/content")
    assert resp.status_code == 200 and resp.body == b""


def test_body_must_be_a_json_object(client):
    resp = client.request("POST", "/files", json_body=["not", "an", "object"])
    assert resp.status_code == 400


def test_dedup_is_invisible_through_the_api(app, client):
    bob = TestClient(app.wsgi, user="bob")
    a = upload(client, "a.txt", b"shared").json
    b = upload(bob, "bobs-name.txt", b"shared").json
    assert client.get(f"/files/{a['id']}/content").body == b"shared"
    assert bob.get(f"/files/{b['id']}/content").body == b"shared"
    assert client.get(f"/files/{b['id']}").status_code == 404
    assert len(app.store.paths()) == 1
    assert client.delete(f"/files/{a['id']}").status_code == 204
    assert bob.get(f"/files/{b['id']}/content").body == b"shared"


# ---- search and filters

def _seed(app, clock):
    """Five files for alice on consecutive days; returns {filename: id}."""
    c = TestClient(app.wsgi, user="alice")
    rows = [
        ("q3-report.pdf", b"x" * 100, "application/pdf"),
        ("Q3-Report-final.PDF", b"y" * 300, "application/pdf"),
        ("notes.txt", b"z" * 10, "text/plain"),
        ("x' OR '1'='1.pdf", b"i" * 50, "application/pdf"),
        ("100%_done.txt", b"p" * 20, "text/plain"),
    ]
    ids = {}
    for name, data, ctype in rows:
        ids[name] = upload(c, name, data, ctype).json["id"]
        clock.tick(days=1)
    return c, ids


def _names(resp):
    assert resp.status_code == 200, resp.json
    return sorted(i["filename"] for i in resp.json["items"])


def test_q_is_a_case_insensitive_substring(app, clock):
    c, _ = _seed(app, clock)
    assert _names(c.get("/files", {"q": "REPORT"})) == ["Q3-Report-final.PDF", "q3-report.pdf"]
    assert _names(c.get("/files", {"q": "q3-report.p"})) == ["q3-report.pdf"]


def test_wildcards_in_q_are_literal(app, clock):
    c, _ = _seed(app, clock)
    assert _names(c.get("/files", {"q": "%"})) == ["100%_done.txt"]
    assert _names(c.get("/files", {"q": "_"})) == ["100%_done.txt"]


def test_injection_filename_is_just_a_string(app, clock):
    c, _ = _seed(app, clock)
    assert _names(c.get("/files", {"q": "' OR '1'='1"})) == ["x' OR '1'='1.pdf"]
    assert _names(c.get("/files", {"q": "nothing like this' --"})) == []


def test_type_filter(app, clock):
    c, _ = _seed(app, clock)
    assert len(_names(c.get("/files", {"type": "application/pdf"}))) == 3
    assert _names(c.get("/files", {"type": "text/plain"})) == ["100%_done.txt", "notes.txt"]


def test_size_bounds_are_inclusive(app, clock):
    c, _ = _seed(app, clock)
    assert _names(c.get("/files", {"min_size": 50, "max_size": 100})) == ["q3-report.pdf", "x' OR '1'='1.pdf"]
    assert _names(c.get("/files", {"min_size": 301})) == []


def test_date_range(app, clock):
    c, _ = _seed(app, clock)
    # uploads happened at 2026-09-01T12:00 + k days
    got = _names(c.get("/files", {"from": "2026-09-02T00:00:00Z", "to": "2026-09-03T23:59:59Z"}))
    assert got == ["Q3-Report-final.PDF", "notes.txt"]


def test_filters_combine(app, clock):
    c, _ = _seed(app, clock)
    assert _names(c.get("/files", {"q": "report", "type": "application/pdf", "min_size": 200})) == [
        "Q3-Report-final.PDF"
    ]


def test_filters_paginate_without_gaps(app, clock):
    c, _ = _seed(app, clock)
    seen, cursor = [], None
    while True:
        params = {"type": "application/pdf", "limit": 2}
        if cursor:
            params["cursor"] = cursor
        page = c.get("/files", params).json
        seen += [i["filename"] for i in page["items"]]
        cursor = page["next_cursor"]
        if cursor is None:
            break
    assert sorted(seen) == ["Q3-Report-final.PDF", "q3-report.pdf", "x' OR '1'='1.pdf"]


def test_search_never_crosses_users(app, clock):
    c, _ = _seed(app, clock)
    bob = TestClient(app.wsgi, user="bob")
    upload(bob, "q3-report.pdf", b"bob's", "application/pdf")
    assert _names(bob.get("/files", {"q": "report"})) == ["q3-report.pdf"]
    assert len(_names(c.get("/files", {"q": "report"}))) == 2


def test_bad_filter_values_are_400_naming_the_parameter(client):
    for params, field in [
        ({"min_size": "abc"}, "min_size"),
        ({"max_size": "-5"}, "max_size"),
        ({"from": "last week"}, "from"),
        ({"to": "2026-99-99"}, "to"),
    ]:
        resp = client.get("/files", params)
        assert resp.status_code == 400
        assert resp.json["error"]["details"]["field"] == field


# ---- quota, stats, rate limit

def _small_quota_app(tmp_path, clock, **env):
    from filevault.app import create_app

    return create_app(tmp_path / "q", clock=clock, env={k.upper(): str(v) for k, v in env.items()})


def test_quota_boundary(tmp_path, clock):
    app = _small_quota_app(tmp_path, clock, filevault_quota_bytes_per_user=100)
    try:
        c = TestClient(app.wsgi, user="alice")
        assert upload(c, "a", b"x" * 60).status_code == 201
        assert upload(c, "b", b"y" * 40).status_code == 201  # exactly the quota
        resp = upload(c, "c", b"z")
        assert resp.status_code == 413
        assert resp.json["error"]["code"] == "quota_exceeded"
        assert resp.json["error"]["details"] == {"used": 100, "quota": 100, "remaining": 0}
    finally:
        app.close()


def test_deleting_restores_quota(tmp_path, clock):
    app = _small_quota_app(tmp_path, clock, filevault_quota_bytes_per_user=10)
    try:
        c = TestClient(app.wsgi, user="alice")
        first = upload(c, "a", b"0123456789").json["id"]
        assert upload(c, "b", b"1").status_code == 413
        c.delete(f"/files/{first}")
        assert upload(c, "b", b"1").status_code == 201
    finally:
        app.close()


def test_duplicates_count_against_each_users_quota(tmp_path, clock):
    app = _small_quota_app(tmp_path, clock, filevault_quota_bytes_per_user=10)
    try:
        c = TestClient(app.wsgi, user="alice")
        assert upload(c, "a", b"12345678").status_code == 201
        assert upload(c, "b", b"12345678").status_code == 413  # same bytes, still 16 > 10 logically
        bob = TestClient(app.wsgi, user="bob")
        assert upload(bob, "a", b"12345678").status_code == 201  # bob's allowance is his own
    finally:
        app.close()


def test_my_stats(app, client):
    upload(client, "a", b"x" * 30)
    upload(client, "b", b"y" * 12)
    assert client.get("/stats").json == {
        "used_bytes": 42,
        "quota_bytes": 10 * 1024 * 1024,
        "remaining_bytes": 10 * 1024 * 1024 - 42,
        "file_count": 2,
    }


def test_admin_stats_show_dedup_savings(app, client):
    bob = TestClient(app.wsgi, user="bob")
    upload(client, "a", b"x" * 1000)
    upload(bob, "a", b"x" * 1000)
    upload(client, "other", b"y" * 500)
    stats = TestClient(app.wsgi, user="admin").get("/admin/stats").json
    assert stats["logical_bytes"] == 2500
    assert stats["physical_bytes"] == 1500
    assert stats["saved_bytes"] == 1000
    assert stats["savings_ratio"] == 0.4
    assert stats["file_count"] == 3


def test_admin_stats_are_admin_only(app, client):
    assert client.get("/admin/stats").status_code == 403


def test_rate_limit_returns_429_with_retry_after(tmp_path, clock):
    app = _small_quota_app(tmp_path, clock, filevault_rate_limit_per_sec=1)
    try:
        c = TestClient(app.wsgi, user="alice")
        assert upload(c, "a", b"1").status_code == 201
        resp = upload(c, "b", b"2")
        assert resp.status_code == 429
        assert int(resp.headers["Retry-After"]) >= 1
        assert resp.json["error"]["code"] == "rate_limited"
        assert upload(TestClient(app.wsgi, user="bob"), "a", b"1").status_code == 201
        assert c.get("/files").status_code == 200  # reads are not limited
    finally:
        app.close()
