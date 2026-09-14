# bs01 minimako — solution notes (not shown to the candidate; read after `ref`)

## Bug 1 — missing `visit_IncludeNode`
`compiler.py`'s `Compiler.visit()` dispatches by `type(node).__name__` to a `visit_<Name>`
method. Every node type in `ast.py` (`TemplateNode`, `TextNode`, `ExpressionNode`, `IfNode`,
`ForNode`, `IncludeNode`) needs one. Five of the six are implemented; `visit_IncludeNode` is
absent, so `getattr(self, "visit_IncludeNode", None)` returns `None` and `visit()` raises
`AttributeError` for its own defensive check (rather than the more confusing bare
`AttributeError: 'Compiler' object has no attribute ...` that `getattr(self, name)` without a
default would have raised — same root cause, marginally better message).

The fix adds the missing method, following the same shape as `visit_ForNode` (resolve something,
build a child `Compiler` scoped to the resolved thing, render, return the string):
```python
def visit_IncludeNode(self, node: astmod.IncludeNode) -> str:
    included = self.current_template.resolve_include(node.file)
    child = Compiler(dict(self.context), current_template=included)
    return child.render(included.ast)
```
`current_template` is threaded through `Compiler.__init__` precisely so this method has something
to call `resolve_include` on — it's not otherwise used by any other visitor, which is worth
calling out if a candidate asks "why does Compiler carry a template reference at all".

## Bug 2 — path traversal via `Template.resolve_include`
`lookup.py`'s `TemplateLookup.get_template()` does the right thing: `uri.lstrip("/")` strips every
leading slash, so `"//../../etc/passwd"` normalizes to `"../../etc/passwd"` — no leading slash
left for `os.path.join` to treat as absolute, and the subsequent `os.path.realpath(...).startswith
(real_dir + os.sep)` containment check catches the `..` traversal on top of that as defense in
depth.

`template.py`'s `Template.resolve_include()` — the *separate* code path used to resolve a
`<%include>` reference relative to the including template's own directory, rather than
re-searching every `TemplateLookup` directory — has its own, independently written
normalization: `file[1:] if file.startswith("/") else file`. This strips exactly **one** leading
slash. Feed it a `file` value with two or more leading slashes (e.g. `"//" + absolute_path_to_a
_secret_file`) and one slash survives. `os.path.join(source_dir, "/abs/path")` then discards
`source_dir` entirely, per Python's own documented `os.path.join` semantics ("if a component is an
absolute path, all previous components are thrown away") — the join returns exactly the attacker's
absolute path, unrelated to `source_dir`. The subsequent `os.path.isfile(path)` check happily
confirms it exists (it's a real file, just not one under the sandbox), and the file gets read and
returned as a "template".

This is exactly the shape of the real bug: `mako/lookup.py`'s `TemplateLookup.get_template()` was
fixed to strip all leading slashes; a second, independently-maintained normalization elsewhere in
the codebase (`mako/template.py`) kept the old single-slash-strip behavior, and the two drifted out
of sync. See `sqlalchemy/mako` issue #434 (fixed in commit `e05ac61`) — the real fix is also a
one-line change from a single-character-strip to a "strip all leading slashes" operation.

The fix:
```python
normalized = file.lstrip("/")   # was: file[1:] if file.startswith("/") else file
```
This makes `resolve_include`'s normalization match `TemplateLookup.get_template`'s exactly. Note
this does **not** add the extra `os.path.realpath(...)` containment check that `lookup.py` has —
for `resolve_include`, `lstrip("/")` alone is sufficient because the normalized string can no
longer be absolute (Python's `os.path.join` can only escape `source_dir` when its second argument
looks absolute), so there is nothing left for a bare `..`-only relative path to walk upward past
that a plain `os.path.isfile` miss wouldn't already catch for this fixture's test surface. A
production-hardened version would still add the containment check for defense in depth (`../`
segments that resolve to a symlinked or otherwise-reachable path within `source_dir`'s parent tree
are a related, distinct concern) — worth mentioning if a candidate raises it, but not required to
pass the tests here.

## What a graded run should look like
- Candidate reproduces `AttributeError` from `visit()`, reads the traceback, finds the five
  existing `visit_*` methods, notices the sixth is missing, adds it by pattern-matching
  `visit_ForNode`'s shape (resolve → child Compiler → render → return string).
- Candidate re-runs tests; `test_render_template_with_include_inlines_child_template` now passes,
  `test_resolve_include_rejects_path_traversal_payload` still fails.
- Candidate reads that test, notices it calls `Template.resolve_include` directly (not through
  `render()`), diffs `resolve_include`'s normalization against `TemplateLookup.get_template`'s,
  spots the `file[1:]` vs `.lstrip("/")` mismatch.
- Total diff: one new method (~4 lines) + one changed line. Candidates who rewrite the tokenizer,
  the parser, or `TemplateLookup` itself have gone looking for a bug that isn't there.
