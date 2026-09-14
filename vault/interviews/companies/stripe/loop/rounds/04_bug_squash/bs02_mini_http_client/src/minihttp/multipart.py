"""Two independent pieces of body-chunking logic that both happen to live here:

`iter_slices()` -- cut a bytes/str object into fixed-size pieces. Used by `Response.iter_content()`
(models.py) to hand a downloaded response body back to the caller in chunks instead of one giant
blob, and by `encode_multipart_formdata()` below to fold a big file field into a part without ever
holding two full copies of it in memory at once.

`encode_multipart_formdata()` -- the `multipart/form-data` body builder for the `files=` argument
to a request: one MIME part per field, joined by a random boundary, terminated per RFC 2388.
"""

from __future__ import annotations

import binascii
import os


def iter_slices(data: bytes | str, slice_length: int | None = None):
    """Yield `data` in pieces of at most `slice_length` bytes/chars each, left to right.

    `slice_length=None` (the default) means "one slice, the whole thing" -- callers that already
    have a natural chunk size in mind (streaming a response to a caller-chosen `chunk_size`, say)
    pass it explicitly; callers that just want "give me this back as an iterable" rely on the
    default.
    """
    pos = 0
    while pos < len(data):
        yield data[pos : pos + slice_length]
        pos += slice_length


def _boundary() -> str:
    return "minihttp-boundary-" + binascii.hexlify(os.urandom(12)).decode("ascii")


def _field_part(boundary: str, name: str, value: str) -> bytes:
    return (
        f"--{boundary}\r\n" f'Content-Disposition: form-data; name="{name}"\r\n\r\n' f"{value}\r\n"
    ).encode("utf-8")


def _file_part(boundary: str, name: str, filename: str, content: bytes, content_type: str) -> bytes:
    header = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode("utf-8")
    # Rebuild the payload chunk by chunk (rather than one `content` slice) so a very large upload
    # never needs a second full-sized copy sitting next to the original in memory.
    body = b"".join(iter_slices(content, 64 * 1024))
    return header + body + b"\r\n"


def encode_multipart_formdata(fields: dict, files: dict) -> tuple[bytes, str]:
    """Build a `multipart/form-data` body from plain fields plus file fields.

    `fields` is `{name: str_value}`. `files` is `{name: (filename, bytes_content, content_type)}`.
    Returns `(body_bytes, content_type_header_value)` -- the header value already carries the
    boundary the body was built with, so callers just set it as-is.
    """
    boundary = _boundary()
    parts = [_field_part(boundary, name, value) for name, value in fields.items()]
    parts += [
        _file_part(boundary, name, filename, content, content_type)
        for name, (filename, content, content_type) in files.items()
    ]
    parts.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"
