"""minimako test suite: lexer, parser, renderer, TemplateLookup, and Template.resolve_include.

Run this before touching anything under src/ -- most of it passes as shipped, which is useful
context on its own. This file is the spec for the exercise; don't edit it to make a failure
go away.
"""

import pytest

from minimako.ast import IfNode, ForNode, parse_text
from minimako.lexer import tokenize
from minimako.lookup import TemplateLookup
from minimako.template import Template


# ---------------------------------------------------------------- lexer / parser
def test_tokenize_plain_text():
    assert tokenize("hello world") == [("text", "hello world")]


def test_tokenize_expression_and_include_tokens():
    tokens = tokenize('Hi ${name}! <%include file="footer.html"/>')
    assert ("expr", "name") in tokens
    assert ("include", "footer.html") in tokens


def test_parse_if_for_nesting_structure():
    tmpl = parse_text("% if cond\nA\n% for x in items\nB\n% endfor\n% endif\n")
    assert len(tmpl.body) == 1
    if_node = tmpl.body[0]
    assert isinstance(if_node, IfNode) and if_node.cond == "cond"
    assert any(isinstance(n, ForNode) for n in if_node.body)


def test_parser_raises_on_unclosed_if_block():
    with pytest.raises(ValueError):
        parse_text("% if cond\ntext\n")


# ---------------------------------------------------------------- rendering: text / expr / if / for
def test_render_plain_text():
    assert Template("hello world").render() == "hello world"


def test_render_expression_interpolation():
    assert Template("Hello, ${name}!").render(name="Ada") == "Hello, Ada!"


def test_render_if_true_branch():
    t = Template("% if show\nvisible\n% endif\n")
    assert t.render(show=True) == "visible\n"


def test_render_if_false_branch_is_empty():
    t = Template("% if show\nvisible\n% endif\nafter")
    assert t.render(show=False) == "after"


def test_render_for_loop_multiple_items():
    t = Template("% for x in items\n${x},\n% endfor\n")
    assert t.render(items=[1, 2, 3]) == "1,\n2,\n3,\n"


def test_for_loop_variable_does_not_leak_outside_loop():
    t = Template("% for x in items\n${x}\n% endfor\nafter:${x}")
    with pytest.raises(NameError):
        t.render(items=[1, 2])


def test_expression_eval_is_sandboxed_no_builtins():
    with pytest.raises(NameError):
        Template("${open}").render()


# ---------------------------------------------------------------- TemplateLookup (safe by design)
def test_lookup_loads_template_from_directory(tmp_path):
    (tmp_path / "hello.html").write_text("Hi ${name}!")
    lookup = TemplateLookup([str(tmp_path)])
    assert lookup.get_template("hello.html").render(name="Ada") == "Hi Ada!"


def test_lookup_missing_file_raises_lookup_error(tmp_path):
    lookup = TemplateLookup([str(tmp_path)])
    with pytest.raises(LookupError):
        lookup.get_template("nope.html")


def test_lookup_get_template_blocks_double_slash_traversal_at_top_level(tmp_path):
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    secret = tmp_path / "secret.txt"
    secret.write_text("TOP SECRET")
    lookup = TemplateLookup([str(templates_dir)])
    payload = "/" + str(secret)  # e.g. "//tmp/.../secret.txt"
    with pytest.raises(LookupError):
        lookup.get_template(payload)


# ---------------------------------------------------------------- Template.resolve_include (normal use)
def test_resolve_include_relative_and_single_slash_still_work(tmp_path):
    (tmp_path / "partial.html").write_text("PARTIAL")
    main = Template("main text", uri="main.html", source_dir=str(tmp_path))
    assert main.resolve_include("partial.html").render() == "PARTIAL"
    assert main.resolve_include("/partial.html").render() == "PARTIAL"


# ---------------------------------------------------------------- Template.render() + <%include>
def test_render_template_with_include_inlines_child_template(tmp_path):
    (tmp_path / "footer.html").write_text("Footer text")
    (tmp_path / "main.html").write_text('Header\n<%include file="footer.html"/>\nEnd')
    lookup = TemplateLookup([str(tmp_path)])
    tmpl = lookup.get_template("main.html")
    assert tmpl.render() == "Header\nFooter text\nEnd"


# ---------------------------------------------------------------- Template.resolve_include (traversal guard)
def test_resolve_include_rejects_path_traversal_payload(tmp_path):
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    secret = tmp_path / "outside_secret.txt"
    secret.write_text("TOP SECRET")
    main = Template("main text", uri="main.html", source_dir=str(templates_dir))
    payload = "/" + str(secret)  # e.g. "//tmp/.../outside_secret.txt"
    with pytest.raises(LookupError):
        main.resolve_include(payload)
