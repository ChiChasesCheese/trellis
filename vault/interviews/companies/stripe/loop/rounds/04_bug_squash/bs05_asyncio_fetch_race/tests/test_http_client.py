"""http_client tests: a single GET against the local test server, success and failure paths."""

import asyncio

from fetchrace.http_client import FetchError, fetch_json, fetch_url


def test_fetch_url_returns_response_body(http_server):
    async def scenario():
        return await fetch_url(f"{http_server}/ok/42")

    assert asyncio.run(scenario()) == b"ok:42"


def test_fetch_json_parses_the_response_body(http_server):
    async def scenario():
        return await fetch_json(f"{http_server}/json/42")

    assert asyncio.run(scenario()) == {"id": "42"}


def test_fetch_url_raises_fetch_error_on_500(http_server):
    async def scenario():
        return await fetch_url(f"{http_server}/always-fail")

    try:
        asyncio.run(scenario())
    except FetchError:
        pass
    else:
        raise AssertionError("expected FetchError for a 500 response")


def test_fetch_url_raises_fetch_error_on_connection_failure():
    async def scenario():
        # nothing listens on this port
        return await fetch_url("http://127.0.0.1:1", timeout=0.5)

    try:
        asyncio.run(scenario())
    except FetchError:
        pass
    else:
        raise AssertionError("expected FetchError when nothing is listening")
