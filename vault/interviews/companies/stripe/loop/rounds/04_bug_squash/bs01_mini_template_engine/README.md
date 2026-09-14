# minimako — a tiny Mako-style template engine

`minimako` is a small template engine modelled on [Mako](https://www.makotemplates.org/)'s core
mini-language: `${expr}` interpolation, `% if` / `% for` control lines, and `<%include
file="..."/>` for composing templates out of smaller files. It exists as a bug-squash fixture —
the shape (lexer → AST → visitor-pattern renderer, plus a `TemplateLookup` that maps a URI to a
file on disk) mirrors real Mako closely enough that its actual historical bugs port over directly.

## Layout
```
src/minimako/
  lexer.py      tokenizer: ${expr}, % if/% for/% endif/% endfor, <%include file="..."/>
  ast.py        AST node types (TextNode, ExpressionNode, IfNode, ForNode, IncludeNode,
                 TemplateNode) + the recursive-descent-over-tokens parser that builds them
  compiler.py   Compiler: renders an AST by dispatching visit_<NodeType> (visitor pattern)
  lookup.py     TemplateLookup(directories): the sanctioned uri -> Template loader
  template.py   Template(text, uri=None, lookup=None, source_dir=None): parses + renders;
                 also resolves this template's own <%include> targets
tests/
  test_minimako.py   the suite (run it, don't rewrite it — see "if you're stuck" below)
```

## Running the tests
```
python -m pytest tests -q
```
Most tests pass as shipped. Two do not — see the issue below.

## The issue (as filed against this repo)

**Bug report 1 — `<%include>` crashes the whole render**

> Repro:
> ```python
> from minimako.lookup import TemplateLookup
> lookup = TemplateLookup(["templates/"])
> tmpl = lookup.get_template("page.html")   # page.html contains <%include file="footer.html"/>
> tmpl.render()
> ```
> Expected: the rendered page, with `footer.html`'s own rendered output spliced in where the
> `<%include>` tag was.
>
> Actual:
> ```
> AttributeError: Compiler has no visitor for node type 'IncludeNode' (expected a method named
> 'visit_IncludeNode')
> ```
> Every other tag type (`${...}`, `% if`, `% for`) renders fine. Only templates that use
> `<%include>` blow up, and they blow up 100% of the time, not intermittently.

**Bug report 2 — a crafted `file="..."` value in `<%include>` can read files outside the
template directory**

> Our security review flagged that `Template.resolve_include()` (used to resolve a `<%include
> file="..."/>` reference relative to the including template's own directory) does not reject a
> `file` value like `"//../../etc/something"` — a URI with **more than one** leading slash. We
> already have this check right in `TemplateLookup.get_template()` (the top-level "load a
> template by URI" entrypoint, used for the very first template in a render), which normalizes by
> stripping *every* leading slash before joining against a search directory and confirming the
> result stays inside it. `resolve_include()` is a separate code path — it's how a template
> resolves `<%include>` references *within itself*, relative to its own file's directory rather
> than by re-searching every `TemplateLookup` directory — and it looks like it grew its own,
> weaker normalization that doesn't match.
>
> Expected: `resolve_include()` rejects (or safely contains) a `file` value with multiple leading
> slashes the same way `TemplateLookup.get_template()` does.
>
> Actual: it accepts such values and can end up reading a file completely outside the template's
> own source directory.

If you get stuck: both bugs are narrowly scoped (one missing method; one wrong string operation
in an existing method) — if your fix touches more than a handful of lines, or you find yourself
rewriting the visitor dispatch mechanism or the URI-normalization design, you've drifted from the
actual bug into a redesign. Come back to the failing assertion and follow the traceback.
