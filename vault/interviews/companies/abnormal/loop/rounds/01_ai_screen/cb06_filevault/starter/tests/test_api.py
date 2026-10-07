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
