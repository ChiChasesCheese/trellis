# bs02 minihttp (mini HTTP client) — report

## Summary
A ~330-line stdlib-only HTTP client (`length.py`/`multipart.py`/`retry.py` → `models.py`'s
Request/PreparedRequest/Response → `adapters.py`'s socket layer → `sessions.py`'s retry loop),
shaped after `requests`' public surface, with two independent, real-pattern bugs injected: a
body-length probe that measures a seekable stream's length correctly but leaves its read position
at EOF (so the body reads back empty), and a chunk-splitting helper that doesn't implement its own
documented `None`-means-"one-chunk" default. Both map directly to real, historical `requests`
issues named in this round's material (`catalog/discovery/2026-09/rounds_material.md` 块 1).

## Sources & confidence
High for "Python bug-squash rounds use `requests`, with `super_len`/body-length bugs specifically
named as candidates": `catalog/discovery/2026-09/rounds_material.md` 块 1.1, rows 1-3 -- `psf/
requests` issues #2589 (2015-05-04, `BytesIO` with no `.name`/`len` mis-measured by `super_len()`,
causing truncated/failed uploads), #3532 (2016-08-23, a performance variant of the same area), and
#3369 (2016-07-01, `iter_slices(iterator, slice_length=None)` with no `None` guard -> bare
`TypeError`) -- all three sourced from `loop/raw/github_repos.md` §2's first-hand GitHub issue
links. `LOOP_GUIDE.md` §4 independently names "requests" as the Python library used for this round
and "off-by-one / 跨调用残留状态" among the four典型 bug shapes to prepare for; bug 1 here (correct
length math, wrong residual stream state left over for the *next* call) is exactly that "state
that should have been reset wasn't" shape, applied to a stream's cursor instead of a parser's
internal field. Medium for this repo's exact module split (`length.py`/`multipart.py`/`retry.py`/
`models.py`/`adapters.py`/`sessions.py` as six files) -- no source specifies real `requests`'
actual file boundaries (real `requests` keeps `super_len` and `iter_slices` both in a single
`utils.py`); this repo's split is a reconstruction chosen to keep each bug in its own small,
independently-readable file, following bs01's precedent of prioritizing clean module boundaries
over exactly mirroring upstream's layout.

## Bugs injected
1. **`length.py`: `super_len()`'s seekable-stream branch never seeks back after measuring.**
   `current_position = o.tell(); o.seek(0, os.SEEK_END); end_position = o.tell(); return
   end_position - current_position` computes the right number but leaves the stream positioned at
   its own end. `models.py`'s `prepare_body()` stores the same (unread) stream object as the
   prepared body so it can be streamed later; by the time `adapters.py`'s `HTTPAdapter.send()`
   calls `.read()` on it, the position is already at EOF, so it reads back `b""`. `Content-Length`
   and the actual bytes sent disagree. Real-pattern match: `psf/requests` issue #2589 (the real fix
   restores position with `o.seek(current_position or 0)` "to support partially read file-like
   objects" -- this fixture's fix is the identical one-line addition).
2. **`multipart.py`: `iter_slices(data, slice_length=None)` never checks for its own documented
   default.** The docstring says `None` means "one slice, the whole thing"; the body goes straight
   to `pos + slice_length` with no guard, raising `TypeError` on the first iteration whenever a
   caller relies on that default. `models.py`'s `Response.iter_content(chunk_size=None)` is the one
   call site that does -- `resp.iter_content()` with no arguments crashes instead of returning the
   whole body as a single chunk; `resp.iter_content(4)` (explicit size) is unaffected. Real-pattern
   match: `psf/requests` issue #3369, nearly verbatim (same signature shape, same missing guard,
   same "works with slice_length" / "crashes without it" split).

## Debugging path (from a failing assertion to the fix)
- Run `pytest tests`: 2 of 25 fail.
- `test_prepare_body_streams_full_bytesio_content_matching_content_length` fails with
  `AssertionError: assert 0 == 11` (`len(b'')` vs. the `Content-Length` header's `11`). The
  preceding, passing `test_super_len_of_fresh_bytesio_matches_its_size` already rules out "the
  length math is wrong" -- it isn't. Reading `prepare_body()` shows the stream object is stored
  unread as `self.body`; reading `super_len()`'s seekable branch shows it seeks to the end to
  measure and never seeks back. Fix: one added line, `o.seek(current_position)`, before the
  `return`.
- `test_iter_content_default_returns_whole_body_as_one_chunk` fails with a `TypeError` whose
  traceback points directly at `iter_slices`'s `data[pos : pos + slice_length]` line -- no
  hypothesis-forming needed, the traceback names the exact line. The docstring immediately above
  it states the promised `None` behavior the code doesn't implement. Fix: one added guard line,
  `if not slice_length or slice_length <= 0: slice_length = len(data)`, before the loop.

## Minimal fix
`solution/FIX.patch` -- 2 files, +3/-0 lines (one added line in `length.py`, two added lines in
`multipart.py`). Verified: `git apply solution/FIX.patch` against a clean copy -> all 25 tests
pass.

## Real library correspondence
- Bug 1: https://github.com/psf/requests/issues/2589 -- `BytesIO`-shaped body with no `.name`/
  `__len__` causing upload truncation; real fix in `requests.utils.super_len()` seeks back to the
  original position after measuring via seek-to-end. The sibling issue #3532 (same code region, a
  performance variant -- `.getvalue()`-copying an object with `.seek()` but no `.len()`) is the
  natural follow-up question for a candidate who fixes this cleanly: "now that it's correct, is it
  efficient for a large stream?" (this fixture's `super_len` never copies the data to measure it,
  so the performance variant doesn't reproduce here -- worth raising as a discussion point, not a
  required fix).
- Bug 2: https://github.com/psf/requests/issues/3369 -- `iter_slices(iterator, slice_length=None)`
  missing a `None`/falsy guard, `TypeError` on first use of the documented default.

## 面试官评分看什么
- Ran the tests first, read the two tracebacks/assertions, didn't start editing code blind.
- For bug 1: noticed the passing `test_super_len_of_fresh_bytesio_matches_its_size` already rules
  out "the length calculation is wrong" -- the interesting question is why a *correct* length and
  an *empty* body coexist, which points straight at a side effect (the stream's position), not the
  arithmetic.
- For bug 2: read the docstring next to the crash site and noticed the code doesn't do what it
  says -- a "the comment and the code disagree" read, not a guess-and-check edit.
- Fix size stays proportional (one line each) -- a candidate who starts rewriting `super_len`'s
  branch order or `iter_slices`'s general loop shape has gone looking for a bug that isn't there.
- Notices that bug 1 is a silent-corruption bug (Content-Length lies about what was actually sent)
  rather than a crash -- worth naming explicitly, since it's the kind of bug that would ship
  unnoticed until a server somewhere started rejecting/hanging on "declared 11 bytes, got 0".

## 常见跑偏
- "Fixing" bug 1 by reading the whole stream into memory up front in `prepare_body()` instead of
  fixing `super_len()`'s missing seek-back -- papers over the real issue (the length-probing side
  effect) and throws away the streaming design for every body type, not just the broken one.
- Fixing bug 2 by giving `iter_content()` a non-`None` default (e.g. `chunk_size=len(content)`)
  instead of fixing `iter_slices()` itself -- `iter_slices` is a general-purpose helper with its
  own documented `None` contract; patching one caller leaves the underlying function still broken
  for any other caller (or test) that relies on the same default.
- Editing `test_minihttp.py` to relax the assertions (e.g. accepting a truncated body, or wrapping
  the `iter_content()` call in `pytest.raises(TypeError)`) instead of fixing `src/minihttp/` --
  the tests are the spec here; changing them defeats the exercise.
- Over-fixing bug 1 by also adding a `try/except` around the whole `super_len` seekable branch --
  not wrong on its own merits, but unrelated to what the failing test actually requires; the fix
  is exactly one line.

## Test inventory
25 tests, plain pytest (no `partN` markers -- bug-squash rounds are single-scenario). 23 pass as
shipped; 2 fail, each isolating one bug
(`test_prepare_body_streams_full_bytesio_content_matching_content_length` -> bug 1;
`test_iter_content_default_returns_whole_body_as_one_chunk` -> bug 2). Two tests
(`test_session_get_against_local_server_happy_path`,
`test_session_post_json_against_local_server_sends_full_body`) exercise a real socket round trip
against a background `http.server` fixture (`local_server` in `conftest.py`) on an OS-assigned
loopback port -- no external network, no fixed port to collide with. After `git apply solution/
FIX.patch`: 25/25 pass.

## Skills exercised
S15 request/response modeling (prepare-then-send pipeline) · S16 stdlib socket-level HTTP
(`http.client`, `http.server`) · S20 root-causing from a traceback/failing assertion rather than
guess-and-check · S21 reasoning about generator evaluation order (why `pos + None` fails on the
*first* iteration, not some later one) · S24 real-open-source-bug pattern matching (`requests`
`super_len`/`iter_slices` bug family)
