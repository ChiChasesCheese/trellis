# bs03 miniyaml (mini YAML subset + CSV bridge) -- report

## Summary
A ~230-line indentation-sensitive YAML-subset parser (`lexer.py` -> `parser.py`'s
recursive-descent-over-indentation `Parser`, plus `scalars.py`'s type coercion and `csvio.py`'s
list-of-records <-> CSV bridge), with two independent, real-pattern bugs injected: an off-by-one
indentation constant that drops a list item's continuation keys (and silently truncates the rest
of the document behind it), and a parser instance that doesn't reset its line cursor between
`.parse()` calls, so reusing one `Parser` for a second document silently returns the wrong result.
Both map directly to the two bug shapes `LOOP_GUIDE.md` SS4 names as典型 for this round
("off-by-one" and "跨调用残留的状态") and to the general bug-squash library family named for
statically-typed indentation-sensitive parsers (Java `SnakeYAML`) in
`catalog/discovery/2026-09/rounds_material.md` 块 1.

## Sources & confidence
High for "off-by-one indentation" and "跨调用残留状态" as two of the four named典型 bug shapes for
this round: `loop/LOOP_GUIDE.md` SS4 ("四类典型 bug（背下来，进场先按这四类猜）：逻辑错误 · off-by-one
· 符号反转 · 跨调用残留的状态（该重置没重置） · 排序里用错 comparator"), itself sourced from
leonstaff.com 2026-08-13 (see `catalog/discovery/2026-09/rounds_material.md` 块 1.2/4.1). High for
"the bug-squash library set for JVM/indentation-sensitive parsing is SnakeYAML": `LOOP_GUIDE.md`
SS4's per-language library table ("Java `SnakeYAML`") and `rounds_material.md` 块 1.1's row 4-5
discussion of the sibling `sqlalchemy/mako` path-normalization bug family (used for bs01) as the
comparable "two independently-written pieces of logic that quietly drift apart" shape this
fixture's bug 1 borrows structurally (a constant that should track a fixed relationship -- here,
"how many columns does '- ' take up" -- computed once, slightly wrong, and never revisited).
Medium for the specific "off-by-one is exactly `+1` instead of `+2`, in the list-item continuation
path specifically" and the specific "no reset in `parse()`" bug 2 shape -- no single source names
a SnakeYAML issue number with this exact signature (unlike bs01's Mako path bug or bs02's
`requests` bugs, this round's material did not surface a specific first-hand SnakeYAML issue link
to cite by number); this repo's two bugs are constructed to match the *named bug categories* from
`LOOP_GUIDE.md` SS4 precisely, rather than reproducing one specific numbered upstream issue.

## Bugs injected
1. **`parser.py`: `_parse_list_block()`'s `content_indent = indent + 1` should be `indent + 2`.**
   A list item's compact form (`"- name: Alice"`) puts its first key two columns past the item's
   own indent (one for `-`, one for the space); a continuation line for the same item's mapping
   (`"  age: 30"`) is written at that same column. Computing the expected column as `indent + 1`
   instead of `indent + 2` makes `_parse_map_block()` reject every continuation line as
   not-matching-this-block, so it returns an empty dict without advancing the cursor -- the
   unconsumed line then breaks the *enclosing* list block's own loop too, silently truncating
   everything from that point in the document onward. Single-key list items (`- id: 1`, no
   continuation line to look for) and arbitrarily-deep plain nested mappings (no lists involved,
   where the child indent is always read from the actual next line rather than computed from a
   fixed offset) are both unaffected -- the bug is narrowly scoped to "a list item whose mapping
   has more than one key". Real-pattern match: `LOOP_GUIDE.md` SS4's "off-by-one" category.
2. **`parser.py`: `Parser.parse()` re-tokenizes `self.lines` on every call but never resets
   `self.pos` back to `0`.** A `Parser` used for exactly one `.parse()` call is unaffected (`pos`
   starts at its `__init__` value, `0`, which happens to already be correct). Reusing the same
   instance for a second, unrelated document leaves `self.pos` wherever the *first* document's
   parse left it; since that's almost always past the end of a second, shorter document's line
   list, `_parse_block()`'s own bounds check fires immediately and returns `{}` without reading a
   single line of the new document -- a silent wrong-but-plausible-looking result, not a crash.
   `parse_text()` (the convenience one-shot function) is unaffected, since it always constructs a
   fresh `Parser()`. Real-pattern match: `LOOP_GUIDE.md` SS4's "跨调用残留的状态（该重置没重置）"
   category, applied to a parser's line cursor rather than (as the guide's own phrasing suggests
   for a more typical case) a buffer or accumulator field.

## Debugging path (from a failing assertion to the fix)
- Run `pytest tests`: 2 of 25 fail.
- `test_parse_top_level_list_of_multi_key_mappings` fails with a clean list/dict diff --
  `[{'name': 'Alice'}]` instead of two full two-key records -- no exception, no traceback to chase.
  The immediately preceding, passing `test_parse_list_of_single_key_mappings` and
  `test_parse_nested_mapping_two_levels` narrow the search fast: single-key list items work fine,
  and arbitrarily deep *plain* nesting (no lists) works fine at every depth, so the bug is
  specific to "a list item's mapping has a second key written below it". Reading
  `_parse_list_block()` and counting columns on a worked example (`"- name: Alice"` -- the "n" of
  "name" is at column 2) against `content_indent = indent + 1` exposes the off-by-one directly.
- `test_parser_reused_across_calls_does_not_leak_state` fails with `{}` instead of `{"x": 9}`,
  again no exception. The adjacent, passing `test_fresh_parser_instance_per_call_is_unaffected_by_
  reuse_bugs` (identical documents, but each parsed by its own fresh `Parser()`) isolates the bug
  to instance *reuse* specifically -- the documents and expected results are the same in both
  tests, only "how many `Parser` objects are involved" differs. Diffing `Parser.__init__` (sets
  `self.pos = 0`) against `Parser.parse()` (never touches `self.pos` again) shows the missing
  reset.
- Total diff: one changed constant, one added line. Both bugs surface as wrong-value assertions,
  not exceptions -- there is no traceback to follow "up" from; the debugging move here is
  differential (comparing a passing test's inputs/code path against a failing one's) rather than
  traceback-following, which is itself worth noticing and naming out loud during the round.

## Minimal fix
`solution/FIX.patch` -- 1 file, +2/-1 lines. Verified: `git apply solution/FIX.patch` against a
clean copy -> all 25 tests pass.

## Real library correspondence
- Bug 1 (off-by-one indentation): no single upstream issue number cited (see confidence note
  above); the bug *category* is named directly in `LOOP_GUIDE.md` SS4 as one of the four to prepare
  for, and its shape -- a small integer constant standing in for "how wide is this syntactic
  marker" that's slightly wrong -- mirrors the general class of indentation/marker-width bugs
  real indentation-sensitive parsers (SnakeYAML, PyYAML, Python's own tokenizer) have shipped
  historically, without claiming a specific commit.
- Bug 2 (residual cross-call state): same -- named directly in `LOOP_GUIDE.md` SS4
  ("跨调用残留的状态（该重置没重置）"), general shape (a stateful object's field not reset at the
  start of the method that's supposed to start fresh) rather than a cited upstream issue.

## 面试官评分看什么
- Ran the tests first, read both failing diffs, didn't start editing code blind.
- For bug 1: used the *passing* neighboring tests (single-key list items; deep plain nesting) to
  narrow the search space before touching `parser.py`, rather than reading the whole file top to
  bottom looking for something suspicious.
- For bug 1 specifically: actually counted columns on a worked example (`"- name: Alice"`) to
  verify the correct constant is `2`, not just changed `1` to some other number that happened to
  make the test pass.
- For bug 2: used the *passing* `test_fresh_parser_instance_per_call_is_unaffected_by_reuse_bugs`
  test (same documents, different Parser-object usage pattern) to isolate "this is about instance
  reuse, not about the documents" before looking at `Parser.__init__`/`parse()`.
- Fix size stays proportional (one constant, one line) -- a candidate who starts introducing an
  explicit indent-stack data structure, or reworking `Line`/`tokenize()`, has gone looking for a
  bug that isn't there.
- Notices that both bugs are *silent* (wrong output, not a crash) rather than the more forgiving
  "the traceback tells you exactly where to look" shape bs01/bs02 lean on more -- worth naming
  explicitly, since debugging a wrong-but-plausible result requires deliberately constructing a
  smaller/simpler repro and comparing against a known-good case, not just reading a stack trace.

## 常见跑偏
- Fixing bug 1 by special-casing "if this is the second-or-later key of a list item's mapping,
  look for a different indent" instead of correcting the one wrong constant -- functionally
  equivalent in the tests provided, but a much larger and more fragile change than the actual bug
  warrants.
- Fixing bug 2 by having `parse_text()` (rather than `Parser.parse()` itself) reset state, or by
  telling callers "just construct a new `Parser()` each time" -- doesn't fix the actual defect
  (`Parser.parse()` failing to be independent of prior calls on the same instance), just works
  around it for the one call site the fixture happens to also provide.
- Editing `test_miniyaml.py` to relax the assertions (e.g. accepting the truncated list, or
  dropping the reuse test) instead of fixing `src/miniyaml/` -- the tests are the spec here;
  changing them defeats the exercise.
- Rewriting `_parse_list_block`/`_parse_map_block` into an iterative, explicit-stack-based parser
  to "fix this properly" -- over-scoped; the existing recursive-descent design is correct, it just
  has one wrong constant in it.

## Test inventory
25 tests, plain pytest (no `partN` markers -- bug-squash rounds are single-scenario). 23 pass as
shipped; 2 fail, each isolating one bug (`test_parse_top_level_list_of_multi_key_mappings` ->
bug 1; `test_parser_reused_across_calls_does_not_leak_state` -> bug 2). Both failures are
wrong-value assertions, not exceptions -- deliberately, to give this round a different debugging
texture from bs01/bs02 (traceback-following isn't the applicable technique here; differential
comparison against a passing neighbor test is). After `git apply solution/FIX.patch`: 25/25 pass.

## Skills exercised
S13 recursive-descent-over-tokens parsing (indentation depth as the recursion driver, mirroring
bs01's token-stream parser) · S17 CSV/tabular data modeling with a schema discovered from the data
itself (`collect_fieldnames`) rather than declared up front · S20 root-causing a *silent*
wrong-value failure via differential comparison against a passing neighbor test, as distinct from
S20's usual traceback-following form · S22 object/instance-state lifecycle reasoning (what a
constructor initializes vs. what a "start fresh" method must re-initialize itself) · S24
real-open-source-bug-*category* matching (off-by-one indentation; residual cross-call state) as
named directly in this round's own prep material, rather than one specific numbered upstream issue
