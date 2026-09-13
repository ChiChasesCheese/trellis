"""Where a PreparedRequest actually goes out over the wire and comes back as a Response.

This is the one module that touches sockets (via the stdlib `http.client`). Everything else in
this package (models, retry, multipart, length) is adapter-agnostic on purpose, so it can be unit
tested without a real server. `HTTPAdapter` is the only implementation; a test suite that wants to
intercept requests without a network can swap in its own object here as long as it has a matching
`.send(prepared_request) -> Response` method -- `Session` doesn't care which it gets.
"""

from __future__ import annotations

import http.client
from urllib.parse import urlsplit

from .models import Response


class HTTPAdapter:
    """Sends a PreparedRequest over a real `http.client.HTTPConnection` and wraps the reply."""

    def __init__(self, timeout: float = 10.0):
        self.timeout = timeout

    def send(self, prepared) -> Response:
        parts = urlsplit(prepared.url)
        conn_cls = http.client.HTTPSConnection if parts.scheme == "https" else http.client.HTTPConnection
        target = parts.netloc
        path = parts.path or "/"
        if parts.query:
            path = f"{path}?{parts.query}"

        body = prepared.body
        if body is not None and hasattr(body, "read"):
            body = body.read()

        conn = conn_cls(target, timeout=self.timeout)
        try:
            conn.request(prepared.method, path, body=body, headers=prepared.headers)
            raw = conn.getresponse()
            content = raw.read()
            headers = dict(raw.getheaders())
            return Response(raw.status, headers, content, url=prepared.url)
        finally:
            conn.close()
