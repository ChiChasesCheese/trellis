# bs03 miniyaml — solution notes (not shown to the candidate; read after `ref`)

## Bug 1 -- off-by-one indentation for a list item's continuation lines

A list item written in the compact form puts its first key right after the dash:
```
- name: Alice
  age: 30
  active: true
```
`"- name: Alice"` has `indent` (leading spaces before the dash) = 0. The characters "- " are two
columns wide, so "name" itself starts at column 2 -- and that's where `age`/`active` are written
too, so `_parse_map_block()` needs to look for sibling keys at indent **2**, not indent 1.

`parser.py`'s `_parse_list_block()` computes this as:
```python
content_indent = indent + 1
entry.update(self._parse_map_block(content_indent))
```
`indent + 1` is one column short. `_parse_map_block(1)` looks at the next line ("age: 30", whose
real indent is 2), sees `2 != 1`, and returns an empty dict immediately -- `entry` ends up as just
`{"name": "Alice"}`, and **`self.pos` is left pointing at the unconsumed "age: 30" line**, because
`_parse_map_block` only advances `self.pos` for lines it actually accepts into the block.

That unconsumed line is what makes the damage bigger than "one record's two keys go missing":
control returns to `_parse_list_block`'s own loop, which checks `self.lines[self.pos]` again --
still "age: 30", indent 2, kind `map_entry`, which doesn't match `indent==0 and kind=="list_item"`,
so the list block's while loop breaks too, having only consumed the first item's first line. The
list ends up as `[{"name": "Alice"}]`, and everything from "age: 30" onward -- including the
entire second record -- is left completely unconsumed and never parsed at all.

Compact single-key items (`- id: 1`) never hit this: there's no continuation line to look for,
so `_parse_map_block(content_indent)` is called against a line that doesn't exist or belongs to
the *next* item, either way correctly returning `{}` with no side effects. Plain nested mappings
(no lists) never call this code path at all -- `_parse_map_block`'s own recursive nesting (via
`_parse_block`) always computes `child_indent` from the actual next line's real indent, not from
a fixed offset, so it has no off-by-one to get wrong.

The fix is the one-character correction the wrong constant needed all along:
```python
content_indent = indent + 2
```

## Bug 2 -- `Parser.pos` isn't reset at the start of `parse()`

`Parser.__init__` sets `self.pos = 0`, and `_parse_map_block`/`_parse_list_block`/`_parse_block`
all advance `self.pos` as they consume lines. `parse()` re-tokenizes `self.lines` for the new
document on every call:
```python
def parse(self, text: str) -> dict | list:
    self.lines = tokenize(text)
    if not self.lines:
        return {}
    return self._parse_block(self.lines[0].indent)
```
but never resets `self.pos` back to `0`. A single `Parser()` used for exactly one `.parse()` call
works fine (`self.pos` starts at its `__init__` value of `0`, which happens to already be
correct). Reuse the same instance for a second `.parse()` call and `self.pos` is still wherever
the *first* document's parse left it -- past the end of the *second* document's (usually much
shorter) line list, so `_parse_block`'s own bounds check (`self.pos >= len(self.lines)`) fires
immediately and returns `{}` without reading a single line of the new document.

`parse_text()` (the module-level convenience function) is unaffected -- it constructs a brand-new
`Parser()` for every call, so there's nothing to leak. The bug only shows up for code that
deliberately reuses one `Parser` instance across multiple documents (a very natural thing to do if
you're processing a batch of files and want to avoid re-constructing the object each time).

The fix resets the one field that needs it, in the one place a fresh parse begins:
```python
def parse(self, text: str) -> dict | list:
    self.lines = tokenize(text)
    self.pos = 0
    ...
```

## What a graded run should look like
- Candidate runs `pytest tests`, sees 2 failures out of 25.
- `test_parse_top_level_list_of_multi_key_mappings` fails with a clean list/dict diff (no
  exception) -- `[{'name': 'Alice'}]` instead of two full records. The adjacent passing
  `test_parse_list_of_single_key_mappings` and `test_parse_nested_mapping_two_levels` narrow the
  bug down fast: single-key list items work, arbitrarily deep *plain* nesting works, so the bug is
  specifically in how a list item's *continuation* lines get matched up. Reading
  `_parse_list_block`'s `content_indent = indent + 1` next to a worked example on paper (count the
  columns in `"- name: Alice"`) exposes the off-by-one immediately.
- `test_parser_reused_across_calls_does_not_leak_state` fails with `{}` instead of `{"x": 9}`; the
  adjacent passing `test_fresh_parser_instance_per_call_is_unaffected_by_reuse_bugs` (same
  documents, but each parsed by its own fresh `Parser()`) isolates the bug to instance reuse
  specifically, not to anything about the documents themselves. Diffing `__init__` against `parse`
  shows `self.pos` is set in one but not reset in the other.
- Total diff: one changed constant (`1` -> `2`) + one added line (`self.pos = 0`). A candidate who
  starts rewriting the recursive-descent structure, switching to an explicit indent stack, or
  reworking how `Line` records are produced has gone looking for a bug that isn't there -- both
  bugs are narrowly, independently scoped to one expression each.
