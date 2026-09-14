"""Thin stdlib-only HTTP GET client, wrapped so it can be awaited from asyncio code.

`urllib.request.urlopen` is a blocking call -- there is no way to `await` it directly. Instead,
`fetch_url` hands it to the event loop's default thread-pool executor and awaits *that*: the
`await` is the point where this coroutine gives up its turn and lets other coroutines run on the
event loop's own thread while the blocking network call happens on a worker thread elsewhere.
"""

from __future__ import annotations

import asyncio
import json
import urllib.error
import urllib.request


class FetchError(Exception):
    """Raised for any failed GET: a network-level error, or an HTTP status >= 400."""


def _blocking_get(url: str, timeout: float) -> bytes:
    """The actual (blocking) network call. Runs on a worker thread, never on the event loop
    thread -- see `fetch_url` for how it gets there."""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return resp.read()
    except urllib.error.HTTPError as exc:
        raise FetchError(f"GET {url} -> HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise FetchError(f"GET {url} -> {exc.reason}") from exc


async def fetch_url(url: str, timeout: float = 5.0) -> bytes:
    """Fetch `url` and return its response body as bytes. Raises `FetchError` on any network
    failure or non-2xx/3xx status."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _blocking_get, url, timeout)


async def fetch_json(url: str, timeout: float = 5.0):
    """Convenience wrapper: fetch `url` and parse its body as JSON. Raises `FetchError` for the
    same reasons as `fetch_url`, plus `json.JSONDecodeError` if the body isn't valid JSON."""
    body = await fetch_url(url, timeout=timeout)
    return json.loads(body)
