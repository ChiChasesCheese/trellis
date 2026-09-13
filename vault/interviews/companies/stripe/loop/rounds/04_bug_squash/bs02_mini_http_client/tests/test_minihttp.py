"""minihttp test suite: request preparation, multipart encoding, retry policy, the Session retry
loop, and two real-socket integration tests against the local_server fixture (see conftest.py).

Run this before touching anything under src/ -- most of it passes as shipped, which is useful
context on its own. This file is the spec for the exercise; don't edit it to make a failure
go away.
"""

from __future__ import annotations

import io

import pytest

from minihttp.length import super_len
from minihttp.models import Request, Response
from minihttp.multipart import encode_multipart_formdata
from minihttp.retry import Retry
from minihttp.sessions import Session


# ---------------------------------------------------------------- PreparedRequest.prepare_url
def test_prepare_url_with_no_params_leaves_url_untouched():
    req = Request("GET", "http://example.invalid/things?a=1")
    prepared = req.prepare()
    assert prepared.url == "http://example.invalid/things?a=1"


def test_prepare_url_merges_params_with_existing_query_string():
    req = Request("GET", "http://example.invalid/things?a=1", params={"b": "2"})
    prepared = req.prepare()
    assert prepared.url == "http://example.invalid/things?a=1&b=2"


# ---------------------------------------------------------------- PreparedRequest.prepare_body
def test_prepare_body_dict_data_is_form_urlencoded():
    req = Request("POST", "http://example.invalid/submit", data={"a": "1", "b": "two words"})
    prepared = req.prepare()
    assert prepared.headers["Content-Type"] == "application/x-www-form-urlencoded"
    assert prepared.body == b"a=1&b=two+words"
    assert prepared.headers["Content-Length"] == str(len(prepared.body))


def test_prepare_body_json_sets_content_type_and_serializes():
    req = Request("POST", "http://example.invalid/submit", json={"n": 3})
    prepared = req.prepare()
    assert prepared.headers["Content-Type"] == "application/json"
    assert prepared.body == b'{"n": 3}'


def test_prepare_body_with_no_data_is_empty():
    req = Request("GET", "http://example.invalid/things")
    prepared = req.prepare()
    assert prepared.body is None
    assert "Content-Length" not in prepared.headers


def test_super_len_of_fresh_bytesio_matches_its_size():
    # super_len() itself just needs to answer "how many bytes", regardless of what happens to
    # the stream's read position afterward -- that's a separate concern from prepare_body below.
    assert super_len(io.BytesIO(b"hello world")) == 11


def test_prepare_body_streams_full_bytesio_content_matching_content_length():
    data = io.BytesIO(b"hello world")
    req = Request("POST", "http://example.invalid/upload", data=data)
    prepared = req.prepare()
    assert prepared.headers["Content-Length"] == "11"
    sent = prepared.body.read()
    assert len(sent) == int(prepared.headers["Content-Length"])
    assert sent == b"hello world"


# ---------------------------------------------------------------- multipart encoding
def test_encode_multipart_formdata_includes_field_and_file_parts():
    body, content_type = encode_multipart_formdata(
        {"user": "ada"}, {"avatar": ("a.png", b"\x89PNG-bytes", "image/png")}
    )
    assert content_type.startswith("multipart/form-data; boundary=")
    boundary = content_type.split("boundary=", 1)[1]
    assert body.count(f"--{boundary}".encode()) == 3  # 2 opening + 1 closing delimiter
    assert b'name="user"' in body and b"ada" in body
    assert b'name="avatar"; filename="a.png"' in body
    assert b"Content-Type: image/png" in body
    assert b"\x89PNG-bytes" in body
    assert body.endswith(f"--{boundary}--\r\n".encode())


def test_encode_multipart_formdata_with_no_files_still_terminates():
    body, content_type = encode_multipart_formdata({"a": "1"}, {})
    boundary = content_type.split("boundary=", 1)[1]
    assert body.endswith(f"--{boundary}--\r\n".encode())


# ---------------------------------------------------------------- Response
def test_response_text_decodes_utf8_by_default():
    resp = Response(200, {}, "héllo".encode("utf-8"))
    assert resp.text == "héllo"


def test_response_json_parses_body():
    resp = Response(200, {"Content-Type": "application/json"}, b'{"ok": true}')
    assert resp.json() == {"ok": True}


def test_response_ok_reflects_status_code():
    assert Response(200, {}, b"").ok is True
    assert Response(404, {}, b"").ok is False


def test_iter_content_with_chunk_size_splits_into_pieces():
    resp = Response(200, {}, b"abcdefgh")
    assert list(resp.iter_content(4)) == [b"abcd", b"efgh"]


def test_iter_content_default_returns_whole_body_as_one_chunk():
    resp = Response(200, {}, b"hello world")
    assert list(resp.iter_content()) == [b"hello world"]


# ---------------------------------------------------------------- Retry policy
def test_retry_is_retryable_status_matches_forcelist():
    retry = Retry(status_forcelist=(429, 503))
    assert retry.is_retryable_status(429) is True
    assert retry.is_retryable_status(503) is True
    assert retry.is_retryable_status(200) is False


@pytest.mark.parametrize("attempt,expected", [(1, 0.5), (2, 1.0), (3, 2.0)])
def test_retry_backoff_time_doubles_each_attempt(attempt, expected):
    retry = Retry(backoff_factor=0.5)
    assert retry.backoff_time(attempt) == expected


def test_retry_backoff_time_rejects_non_positive_attempt():
    retry = Retry(backoff_factor=0.5)
    with pytest.raises(ValueError):
        retry.backoff_time(0)


# ---------------------------------------------------------------- Session retry loop (fake adapter)
class _ScriptedAdapter:
    """Returns/raises one scripted outcome per call, in order."""

    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.calls = 0

    def send(self, prepared):
        self.calls += 1
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


def test_session_returns_immediately_on_non_retryable_status():
    adapter = _ScriptedAdapter([Response(200, {}, b"ok")])
    session = Session(retry=Retry(total=3), adapter=adapter, sleep=lambda s: None)
    resp = session.get("http://example.invalid/x")
    assert resp.status_code == 200
    assert adapter.calls == 1


def test_session_retries_on_retryable_status_then_succeeds():
    adapter = _ScriptedAdapter([Response(503, {}, b""), Response(503, {}, b""), Response(200, {}, b"ok")])
    sleeps = []
    session = Session(retry=Retry(total=3, backoff_factor=0.1), adapter=adapter, sleep=sleeps.append)
    resp = session.get("http://example.invalid/x")
    assert resp.status_code == 200
    assert adapter.calls == 3
    assert sleeps == [0.1, 0.2]


def test_session_gives_up_and_returns_last_response_after_total_attempts():
    adapter = _ScriptedAdapter([Response(503, {}, b""), Response(503, {}, b"")])
    session = Session(retry=Retry(total=2, backoff_factor=0), adapter=adapter, sleep=lambda s: None)
    resp = session.get("http://example.invalid/x")
    assert resp.status_code == 503
    assert adapter.calls == 2


def test_session_reraises_connection_error_after_exhausting_retries():
    adapter = _ScriptedAdapter([OSError("connection refused"), OSError("connection refused")])
    session = Session(retry=Retry(total=2, backoff_factor=0), adapter=adapter, sleep=lambda s: None)
    with pytest.raises(OSError):
        session.get("http://example.invalid/x")


# ---------------------------------------------------------------- real-socket integration (local_server)
def test_session_get_against_local_server_happy_path(local_server):
    local_server.queue_response(200, {"Content-Type": "text/plain"}, b"pong")
    host, port = local_server.server_address
    session = Session()
    resp = session.get(f"http://{host}:{port}/ping", params={"q": "1"})
    assert resp.status_code == 200
    assert resp.text == "pong"
    assert local_server.requests[0]["method"] == "GET"
    assert local_server.requests[0]["path"] == "/ping?q=1"


def test_session_post_json_against_local_server_sends_full_body(local_server):
    local_server.queue_response(201, {}, b"")
    host, port = local_server.server_address
    session = Session()
    resp = session.post(f"http://{host}:{port}/items", json={"name": "widget"})
    assert resp.status_code == 201
    received = local_server.requests[0]
    assert received["method"] == "POST"
    assert received["body"] == b'{"name": "widget"}'
    assert received["headers"]["Content-Length"] == str(len(received["body"]))
