# minihttp — a tiny stdlib HTTP client

`minihttp` is a small HTTP client library shaped after the public surface of
[`requests`](https://requests.readthedocs.io/): a `Session` that builds a `Request`, turns it into
a wire-ready `PreparedRequest` (resolved URL, final headers, a body with a computed
`Content-Length`), sends it through an `HTTPAdapter`, retries on a configurable list of status
codes with exponential backoff, and hands back a `Response`. It exists as a bug-squash fixture —
the shape (request/response models, a body-length prober, a chunk-splitting helper, a retry
policy) mirrors real `requests` closely enough that its actual historical bugs port over directly.

## Layout
```
src/minihttp/
  length.py      super_len(o): best-effort byte length of a request body, for objects that
                  don't all expose their size the same way (bytes vs. an open file vs. a
                  seekable-but-otherwise-opaque stream like io.BytesIO)
  multipart.py    iter_slices(data, slice_length): split bytes/str into fixed-size pieces;
                  encode_multipart_formdata(fields, files): builds a multipart/form-data body
  retry.py        Retry(total, backoff_factor, status_forcelist): pure retry/backoff policy
  models.py       Request / PreparedRequest (.prepare_url/.prepare_headers/.prepare_body) /
                  Response (.text/.json()/.iter_content())
  adapters.py     HTTPAdapter: sends a PreparedRequest over a real http.client connection
  sessions.py     Session: owns default headers + Retry + adapter; .get()/.post()/.request()
                  drive the retry loop
tests/
  test_minihttp.py   the suite (run it, don't rewrite it — see "if you're stuck" below)
  conftest.py        sys.path setup + a `local_server` fixture: a real background HTTP server
                      on a loopback port, used by the two integration-style tests at the bottom
```

## Running the tests
```
python -m pytest tests
```
Most tests pass as shipped. Two do not — see the issue below.

## The issue (as filed against this repo)

**Bug report 1 — large file uploads come out empty (or truncated) on the wire**

> Repro:
> ```python
> import io
> from minihttp.models import Request
>
> data = io.BytesIO(b"hello world")
> prepared = Request("POST", "http://example.invalid/upload", data=data).prepare()
> print(prepared.headers["Content-Length"])   # "11" — correct!
> print(prepared.body.read())                 # b"" — !?
> ```
> `Content-Length` comes out right, but the body that actually gets sent is empty. Confirmed this
> against a real local server too: it reports receiving a `Content-Length: 11` header and then
> zero bytes of body before the socket goes idle.
>
> Expected: `prepared.body.read()` returns the same 11 bytes that `Content-Length` claims.
>
> Actual: it returns nothing, for any `data=` passed as a fresh `io.BytesIO` (or any other plain
> seekable stream — a wrapped file object, a custom buffer, anything that has `.tell()`/`.seek()`
> but not `__len__` or `.len` or a usable `.fileno()`). Plain `bytes`, a `dict` (form-urlencoded),
> and `json=` are all unaffected — only this one family of body type is broken.

**Bug report 2 — `response.iter_content()` (no arguments) crashes instead of returning the body**

> Repro:
> ```python
> from minihttp.models import Response
>
> resp = Response(200, {}, b"hello world")
> list(resp.iter_content())
> ```
> ```
> TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'
> ```
> Calling `iter_content(4)` with an explicit chunk size works fine and returns the expected
> 4-byte pieces. It's specifically the no-argument call — which the docstring says should hand
> back the whole body as a single chunk — that blows up.

If you get stuck: both bugs are narrowly scoped (one missing side-effect in an existing function;
one missing early check in an existing function) — if your fix touches more than a handful of
lines, or you find yourself rewriting `super_len`'s dispatch order or `iter_slices`'s general
shape, you've drifted from the actual bug into a redesign. Come back to the failing assertion and
follow the traceback.
