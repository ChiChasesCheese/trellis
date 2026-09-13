"""miniyaml test suite: lexer, scalar coercion, the indentation-based parser, and the CSV bridge.

Run this before touching anything under src/ -- most of it passes as shipped, which is useful
context on its own. This file is the spec for the exercise; don't edit it to make a failure
go away.
"""

from __future__ import annotations

from miniyaml.csvio import collect_fieldnames, from_csv_text, to_csv_text
from miniyaml.lexer import tokenize
from miniyaml.parser import Parser, parse_text
from miniyaml.scalars import coerce_scalar, scalar_to_text


# ---------------------------------------------------------------- lexer
def test_tokenize_plain_map_entry():
    (line,) = tokenize("name: Alice")
    assert (line.indent, line.kind, line.key, line.value) == (0, "map_entry", "name", "Alice")


def test_tokenize_map_entry_with_no_inline_value():
    (line,) = tokenize("children:")
    assert (line.key, line.value) == ("children", None)


def test_tokenize_scalar_list_item():
    (line,) = tokenize("- widget")
    assert line.kind == "list_item"
    assert line.list_item_kind == "scalar"
    assert line.value == "widget"


def test_tokenize_mapping_inline_list_item():
    (line,) = tokenize("  - host: a.example.com")
    assert line.indent == 2
    assert line.list_item_kind == "mapping_inline"
    assert (line.key, line.value) == ("host", "a.example.com")


def test_tokenize_skips_blank_lines_and_comments():
    lines = tokenize("a: 1\n\n# a comment\nb: 2\n")
    assert [line.key for line in lines] == ["a", "b"]


# ---------------------------------------------------------------- scalars
def test_coerce_scalar_int_and_float():
    assert coerce_scalar("42") == 42
    assert coerce_scalar("3.5") == 3.5


def test_coerce_scalar_bool_and_null():
    assert coerce_scalar("true") is True
    assert coerce_scalar("false") is False
    assert coerce_scalar("null") is None
    assert coerce_scalar("~") is None


def test_coerce_scalar_quoted_string_is_unwrapped_verbatim():
    assert coerce_scalar('"42"') == "42"
    assert coerce_scalar("'true'") == "true"


def test_coerce_scalar_plain_unquoted_string_passes_through():
    assert coerce_scalar("us-east") == "us-east"


def test_scalar_to_text_round_trips_types():
    assert scalar_to_text(True) == "true"
    assert scalar_to_text(False) == "false"
    assert scalar_to_text(None) == ""
    assert scalar_to_text(7) == "7"


# ---------------------------------------------------------------- parser: flat & nested mappings
def test_parse_flat_mapping():
    assert parse_text("name: Alice\nage: 30\nactive: true\n") == {
        "name": "Alice",
        "age": 30,
        "active": True,
    }


def test_parse_nested_mapping_two_levels():
    doc = "a:\n  b:\n    c: 1\n    d: 2\n  e: 3\nf: 4\n"
    assert parse_text(doc) == {"a": {"b": {"c": 1, "d": 2}, "e": 3}, "f": 4}


def test_parse_empty_document_is_empty_mapping():
    assert parse_text("") == {}
    assert parse_text("\n\n# just a comment\n") == {}


# ---------------------------------------------------------------- parser: lists
def test_parse_top_level_scalar_list():
    assert parse_text("- red\n- green\n- blue\n") == ["red", "green", "blue"]


def test_parse_scalar_list_nested_under_a_key():
    doc = "tags:\n  - urgent\n  - billing\nowner: ops\n"
    assert parse_text(doc) == {"tags": ["urgent", "billing"], "owner": "ops"}


def test_parse_list_of_single_key_mappings():
    # each item's mapping has exactly one key -- the compact "- key: value" form with no
    # continuation lines, so there's nothing for a second line to align to.
    doc = "- id: 1\n- id: 2\n- id: 3\n"
    assert parse_text(doc) == [{"id": 1}, {"id": 2}, {"id": 3}]


def test_parse_top_level_list_of_multi_key_mappings():
    doc = "- name: Alice\n  age: 30\n  active: true\n- name: Bob\n  age: 25\n  active: false\n"
    assert parse_text(doc) == [
        {"name": "Alice", "age": 30, "active": True},
        {"name": "Bob", "age": 25, "active": False},
    ]


# ---------------------------------------------------------------- parser: instance reuse
def test_fresh_parser_instance_per_call_is_unaffected_by_reuse_bugs():
    first = Parser().parse("a: 1\nb: 2\nc: 3\n")
    second = Parser().parse("x: 9\n")
    assert first == {"a": 1, "b": 2, "c": 3}
    assert second == {"x": 9}


def test_parser_reused_across_calls_does_not_leak_state():
    p = Parser()
    first = p.parse("a: 1\nb: 2\nc: 3\n")
    second = p.parse("x: 9\n")
    assert first == {"a": 1, "b": 2, "c": 3}
    assert second == {"x": 9}


# ---------------------------------------------------------------- CSV bridge
def test_collect_fieldnames_is_first_seen_order_across_records():
    records = [{"a": 1, "b": 2}, {"b": 3, "c": 4}]
    assert collect_fieldnames(records) == ["a", "b", "c"]


def test_to_csv_text_produces_header_and_rows():
    records = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
    text = to_csv_text(records)
    assert text.splitlines() == ["name,age", "Alice,30", "Bob,25"]


def test_to_csv_text_fills_missing_columns_with_empty_cell():
    records = [{"a": 1, "b": 2}, {"a": 3}]
    text = to_csv_text(records)
    assert text.splitlines() == ["a,b", "1,2", "3,"]


def test_from_csv_text_coerces_cell_types():
    text = "name,age,active\nAlice,30,true\nBob,25,false\n"
    assert from_csv_text(text) == [
        {"name": "Alice", "age": 30, "active": True},
        {"name": "Bob", "age": 25, "active": False},
    ]


def test_csv_round_trip_preserves_records():
    records = [
        {"id": 1, "label": "widget", "active": True},
        {"id": 2, "label": "gadget", "active": False},
    ]
    assert from_csv_text(to_csv_text(records)) == records


# ---------------------------------------------------------------- end to end: YAML -> CSV
def test_yaml_document_of_single_key_records_converts_to_csv():
    doc = "- id: 1\n- id: 2\n"
    records = parse_text(doc)
    assert to_csv_text(records).splitlines() == ["id", "1", "2"]
