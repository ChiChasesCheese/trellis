# bs02 minihttp — solution notes (not shown to the candidate; read after `ref`)

## Bug 1 — `super_len()` doesn't restore the stream position it moved

`length.py`'s `super_len(o)` needs a length for any seekable-but-otherwise-opaque body (an
`io.BytesIO`, a wrapped file, anything with `.tell()`/`.seek()` but no `__len__`/`.len`/usable
`.fileno()`). The only way to measure such an object is to seek to its end and see what position
that is:
```python
current_position = o.tell()
o.seek(0, os.SEEK_END)
end_position = o.tell()
return end_position - current_position
```
This correctly computes the length — `test_super_len_of_fresh_bytesio_matches_its_size` passes —
but it leaves the stream's read position sitting at the *end* of the data. `prepare_body()`
(models.py) stores this same object, unread, as `self.body` so the adapter can stream it later
(`adapters.py`'s `HTTPAdapter.send()` does `body = body.read()` right before handing it to
`http.client`). By the time that `.read()` call happens, the stream is already parked at EOF, so
it returns `b""` — an empty body — even though `Content-Length` was computed correctly and already
sent. The header and the actual bytes on the wire disagree; a real server sees `Content-Length: 11`
followed by zero bytes and hangs waiting for a body that never comes (or, depending on the server,
treats it as a malformed/incomplete request).

The fix restores the position after measuring, exactly like a well-behaved "peek at the length"
operation should:
```python
current_position = o.tell()
o.seek(0, os.SEEK_END)
end_position = o.tell()
o.seek(current_position)          # <-- restore it
return end_position - current_position
```
This is the real historical bug: `requests` issue
[#2589](https://github.com/psf/requests/issues/2589) — a `BytesIO`-like body with no `.name`/
`__len__` got its length measured (or mismeasured) in a way that left the stream in the wrong
state for the subsequent read, causing truncated/failed uploads. The real `requests.utils.
super_len()` fix seeks back to `current_position or 0` after measuring, for exactly this reason
("to support partially read file-like objects").

## Bug 2 — `iter_slices()` doesn't handle its own documented default

`multipart.py`'s `iter_slices(data, slice_length=None)` docstring says `slice_length=None` means
"one slice, the whole thing" — that's the whole point of the default. But the body never checks
for `None`; it goes straight to:
```python
pos = 0
while pos < len(data):
    yield data[pos : pos + slice_length]
    pos += slice_length
```
`pos + slice_length` with `slice_length=None` raises `TypeError: unsupported operand type(s) for
+: 'int' and 'NoneType'` on the very first iteration (Python evaluates `pos + slice_length` to
build the slice's stop index before it can even try `data[pos:...]`), so the generator raises
immediately instead of yielding the single "whole thing" chunk its own docstring promises.

`Response.iter_content(chunk_size=None)` (models.py) is the one call site that relies on the
default: `resp.iter_content()` with no arguments is supposed to hand back the whole body as one
chunk, and does call `iter_slices(self._content, chunk_size)` with `chunk_size` still `None`. Any
explicit chunk size (`resp.iter_content(4)`) bypasses the bug entirely, which is why only the
no-argument call fails.

The fix adds the check the docstring already promised:
```python
if not slice_length or slice_length <= 0:
    slice_length = len(data)
```
This is the real historical bug: `requests` issue
[#3369](https://github.com/psf/requests/issues/3369) — `iter_slices(iterator, slice_length=None)`
had no guard for `slice_length is None`, so a caller relying on the documented default hit a bare
`TypeError` instead of getting the iterator they asked for. Same shape here: a one-line missing
guard on a parameter whose whole reason for existing is "the caller might not pass this".

## What a graded run should look like
- Candidate runs `pytest tests`, sees 2 failures out of 25.
- `test_prepare_body_streams_full_bytesio_content_matching_content_length` fails with
  `assert 0 == 11` (`len(b'') != 11`). Following `prepared.body.read()` back to `prepare_body()`
  shows the body is stored unread; following the `Content-Length` computation back to `super_len()`
  shows it seeks to measure length but never seeks back. Fix: one added line, `o.seek
  (current_position)`.
- `test_iter_content_default_returns_whole_body_as_one_chunk` fails with a `TypeError` raised from
  inside `iter_slices` (visible directly in the traceback — no guessing needed about which
  function to look at). Reading the docstring right above the crash site names the exact promised
  behavior (`None` means "one slice") that the code doesn't implement. Fix: one added guard line.
- Total diff: two files, two small additions, no restructuring. A candidate who starts rewriting
  `super_len`'s dispatch order (the `__len__`/`.len`/`fileno`/seek branches) or `iter_slices`'s
  general chunking loop has gone looking for a bug that isn't there — both bugs are single missing
  lines in otherwise-correct functions.
