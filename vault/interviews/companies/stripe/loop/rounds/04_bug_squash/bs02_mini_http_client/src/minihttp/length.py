"""Figuring out how many bytes a request body is, without necessarily reading all of it.

`Session.request()` needs a `Content-Length` header before it hands the body to an adapter to
send. The body can be plain `bytes` (trivial: `len()` works), or it can be *any* file-like object
someone passes in (an open file, an `io.BytesIO`, a custom stream) -- those don't all expose their
size the same way, so `super_len()` tries a few strategies in order and falls back to "unknown"
(`None`) if none of them apply. This mirrors the same probing job `requests.utils.super_len()`
does for the same reason.
"""

from __future__ import annotations

import io
import os


def super_len(o: object) -> int | None:
    """Best-effort byte length of a request body `o`.

    Handles, in order: anything with `__len__` (bytes, str, lists of chunks), anything with a
    `.len` attribute (some libraries expose remaining length that way), an open file (via
    `os.fstat` on its file descriptor), and finally anything seekable (`.tell()` + `.seek()`) such
    as `io.BytesIO`, which has none of the above.

    Returns `None` if none of the above apply (the caller then has to fall back to chunked
    transfer, since it genuinely doesn't know the size up front).
    """
    if hasattr(o, "__len__"):
        return len(o)

    if hasattr(o, "len"):
        return o.len

    if hasattr(o, "fileno"):
        try:
            fileno = o.fileno()
        except (io.UnsupportedOperation, AttributeError):
            pass
        else:
            return os.fstat(fileno).st_size

    if hasattr(o, "tell") and hasattr(o, "seek"):
        current_position = o.tell()
        o.seek(0, os.SEEK_END)
        end_position = o.tell()
        return end_position - current_position

    return None
