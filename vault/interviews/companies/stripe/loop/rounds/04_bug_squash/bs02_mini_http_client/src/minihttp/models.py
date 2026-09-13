"""The data that flows through a request/response cycle: `Request` (what the caller asked for),
`PreparedRequest` (the same thing turned into exactly the bytes that go on the wire: a method, a
URL with its query string, a header dict, and a body), and `Response` (what came back).

`Session.request()` (sessions.py) builds a `Request`, calls `.prepare()` to get a
`PreparedRequest`, and hands that to an adapter (adapters.py) to actually send.
"""

from __future__ import annotations

import json as json_module
from urllib.parse import urlencode, urlsplit, urlunsplit, parse_qsl

from .length import super_len
from .multipart import encode_multipart_formdata, iter_slices


class Request:
    """What the caller wants to send: not yet a URL-with-querystring or a wire-ready body."""

    def __init__(
        self,
        method: str,
        url: str,
        headers: dict | None = None,
        params: dict | None = None,
        data: object = None,
        json: object = None,
        files: dict | None = None,
    ):
        self.method = method.upper()
        self.url = url
        self.headers = dict(headers) if headers else {}
        self.params = params
        self.data = data
        self.json = json
        self.files = files

    def prepare(self) -> "PreparedRequest":
        """Turn this Request into a PreparedRequest: resolved URL, final headers, wire-ready body."""
        p = PreparedRequest()
        p.prepare_method(self.method)
        p.prepare_url(self.url, self.params)
        p.prepare_headers(self.headers)
        p.prepare_body(self.data, self.json, self.files)
        return p


class PreparedRequest:
    """The literal thing an adapter sends: `method`, `url`, `headers`, `body`.

    `body` is either `bytes`/`str`, or -- for a body passed in as a file-like object -- the
    object itself, left unread so the adapter can stream it rather than buffering it here.
    """

    def __init__(self):
        self.method: str | None = None
        self.url: str | None = None
        self.headers: dict = {}
        self.body: object = None

    def prepare_method(self, method: str) -> None:
        self.method = method.upper()

    def prepare_url(self, url: str, params: dict | None) -> None:
        """Merge `params` into `url`'s existing query string (existing params win no conflicts;
        both sets of keys are kept, in "existing query string, then params" order)."""
        if not params:
            self.url = url
            return
        scheme, netloc, path, query, fragment = urlsplit(url)
        pairs = parse_qsl(query, keep_blank_values=True)
        pairs += list(params.items())
        self.url = urlunsplit((scheme, netloc, path, urlencode(pairs), fragment))

    def prepare_headers(self, headers: dict) -> None:
        self.headers = dict(headers)

    def prepare_body(self, data: object, json: object, files: dict | None) -> None:
        """Fill in `self.body` and any headers it implies (`Content-Type`, `Content-Length`).

        Exactly one of `json`, `files`, or a `data` that isn't a plain mapping is expected to
        drive the body; `data` as a `dict` with no `files` is form-urlencoded, matching the
        common "submit an HTML form" case.
        """
        if files:
            fields = data if isinstance(data, dict) else {}
            body, content_type = encode_multipart_formdata(fields, files)
            self.headers.setdefault("Content-Type", content_type)
            self.body = body
            self.headers["Content-Length"] = str(len(body))
            return

        if json is not None:
            body = json_module.dumps(json).encode("utf-8")
            self.headers.setdefault("Content-Type", "application/json")
            self.body = body
            self.headers["Content-Length"] = str(len(body))
            return

        if isinstance(data, dict):
            body = urlencode(data).encode("utf-8")
            self.headers.setdefault("Content-Type", "application/x-www-form-urlencoded")
            self.body = body
            self.headers["Content-Length"] = str(len(body))
            return

        if data is None:
            self.body = None
            return

        # Anything else (bytes, str, or a file-like object) is passed through mostly as-is; we
        # only need to know its length up front so the adapter can set Content-Length before it
        # starts sending. If we can't determine the length, the adapter falls back to
        # chunked transfer instead.
        self.body = data
        length = super_len(data)
        if length is not None:
            self.headers["Content-Length"] = str(length)


class Response:
    """What came back: status, headers, and the body -- either already fully read (`content`) or
    handed back lazily via `iter_content()`.
    """

    def __init__(self, status_code: int, headers: dict, content: bytes, url: str | None = None):
        self.status_code = status_code
        self.headers = dict(headers)
        self._content = content
        self.url = url

    @property
    def ok(self) -> bool:
        return self.status_code < 400

    @property
    def content(self) -> bytes:
        return self._content

    @property
    def text(self) -> str:
        encoding = "utf-8"
        ct = self.headers.get("Content-Type", "")
        if "charset=" in ct:
            encoding = ct.split("charset=", 1)[1].split(";", 1)[0].strip()
        return self._content.decode(encoding)

    def json(self) -> object:
        return json_module.loads(self.text)

    def iter_content(self, chunk_size: int | None = None):
        """Yield the body in pieces of `chunk_size` bytes; `chunk_size=None` means "as one piece"."""
        yield from iter_slices(self._content, chunk_size)
