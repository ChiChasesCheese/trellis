import json
import random
import string
import sys

import pytest


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example_command_stream(impl):
    out = impl.part1(['PARSE {"a": 1, "b": [1,2,3]}', 'PARSE {"a":1,}'])
    assert out == ['{"a":1,"b":[1,2,3]}', "INVALID"]


@pytest.mark.part1
def test_minify_basic_shapes(impl):
    assert impl.minify("{}") == "{}"
    assert impl.minify("[]") == "[]"
    assert impl.minify('"hello"') == '"hello"'
    assert impl.minify("123") == "123"
    assert impl.minify("true") == "true"
    assert impl.minify("false") == "false"
    assert impl.minify("null") == "null"


@pytest.mark.part1
def test_numbers_kept_verbatim_not_reformatted(impl):
    assert impl.minify("1.50e+2") == "1.50e+2"
    assert impl.minify("1E+10") == "1E+10"
    assert impl.minify("-0") == "-0"
    assert impl.minify("0.5") == "0.5"


@pytest.mark.part1
@pytest.mark.edge
@pytest.mark.parametrize("bad", ["01", "1.", "1e", "--1", ".5", "1.e5", "+1"])
def test_invalid_number_grammar(impl, bad):
    with pytest.raises(ValueError):
        impl.parse(bad)


@pytest.mark.part1
@pytest.mark.edge
def test_string_escapes_decode_correctly(impl):
    assert impl.parse(r'"tab\ttab"') == ("str", "tab\ttab")
    assert impl.parse(r'"nl\nnl"') == ("str", "nl\nnl")
    assert impl.parse(r'"slash\/ok"') == ("str", "slash/ok")
    assert impl.parse('"\\u0041"') == ("str", "A")  # basic \u escape
    assert impl.parse('"literal😀emoji"') == ("str", "literal\U0001F600emoji")  # raw UTF-8, no escape
    assert impl.parse('"\\ud83d\\ude00"') == ("str", "\U0001F600")  # surrogate pair -> one emoji


@pytest.mark.part1
@pytest.mark.edge
def test_canonical_reescape_rule(impl):
    # '/' is never escaped in output, control chars use short forms, non-ASCII stays literal
    assert impl.minify(r'"slash\/ok"') == '"slash/ok"'
    assert impl.minify(r'"tab\ttab"') == r'"tab\ttab"'
    assert impl.minify('"café"') == '"café"'


@pytest.mark.part1
@pytest.mark.edge
def test_unpaired_surrogate_is_invalid(impl):
    with pytest.raises(ValueError):
        impl.parse(r'"\ud800"')


@pytest.mark.part1
@pytest.mark.edge
def test_unescaped_control_character_is_invalid(impl):
    with pytest.raises(ValueError):
        impl.parse('"line1\nline2"')  # a LITERAL newline inside the string, not \n


@pytest.mark.part1
@pytest.mark.edge
def test_bare_nan_and_infinity_are_invalid(impl):
    for bad in ["NaN", "Infinity", "-Infinity"]:
        with pytest.raises(ValueError):
            impl.parse(bad)


@pytest.mark.part1
@pytest.mark.edge
def test_trailing_comma_invalid_in_object_and_array(impl):
    with pytest.raises(ValueError):
        impl.parse('{"a":1,}')
    with pytest.raises(ValueError):
        impl.parse("[1,2,]")


@pytest.mark.part1
@pytest.mark.edge
def test_missing_colon_or_comma_invalid(impl):
    with pytest.raises(ValueError):
        impl.parse('{"a" 1}')
    with pytest.raises(ValueError):
        impl.parse("[1 2]")


@pytest.mark.part1
@pytest.mark.edge
def test_trailing_garbage_after_value_invalid(impl):
    with pytest.raises(ValueError):
        impl.parse('{"a":1}{"b":2}')
    with pytest.raises(ValueError):
        impl.parse("1 2")


@pytest.mark.part1
@pytest.mark.edge
def test_empty_and_whitespace_only_input_invalid(impl):
    with pytest.raises(ValueError):
        impl.parse("")
    with pytest.raises(ValueError):
        impl.parse("   \n\t  ")


@pytest.mark.part1
@pytest.mark.edge
def test_surrounding_whitespace_allowed(impl):
    assert impl.minify('  { "a" : 1 }  ') == '{"a":1}'


# ------------------------------------------------------------------------ Part 2 (iterative depth)
@pytest.mark.part2
@pytest.mark.perf
def test_deeply_nested_array_no_recursion(impl):
    n = 100_000
    text = "[" * n + "1" + "]" * n
    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(150)
    try:
        out = impl.minify(text)
    finally:
        sys.setrecursionlimit(old_limit)
    assert out == text


@pytest.mark.part2
@pytest.mark.perf
def test_deeply_nested_object_no_recursion(impl):
    n = 20_000
    text = '{"a":' * n + "1" + "}" * n
    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(150)
    try:
        out = impl.minify(text)
    finally:
        sys.setrecursionlimit(old_limit)
    assert out == text


@pytest.mark.part2
@pytest.mark.perf
def test_perf_large_flat_array_via_script(run_script):
    values = ",".join(str(i) for i in range(50_000))
    text = f"[{values}]"
    r = run_script(f"PART 2\nPARSE {text}\n", timeout=15)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ Part 3 (dup keys, path)
@pytest.mark.part3
def test_worked_example_dup_and_path(impl):
    out = impl.part3(
        [
            'PARSE_DUP last {"a":1,"a":2}',
            'PARSE_DUP error {"a":1,"a":2}',
            'PATH a.b[2].c {"a":{"b":[1,2,{"c":3}]}}',
            'PATH a.z {"a":1}',
            "PATH a bad json",
        ]
    )
    assert out == ['{"a":2}', "DUPLICATE", "3", "NOTFOUND", "INVALID"]


@pytest.mark.part3
@pytest.mark.edge
def test_duplicate_key_last_wins_keeps_first_position(impl):
    value = impl.parse('{"a":1,"b":2,"a":3}', on_duplicate_key="last")
    assert impl.serialize(value) == '{"a":3,"b":2}'


@pytest.mark.part3
@pytest.mark.edge
def test_duplicate_key_error_policy_raises(impl):
    with pytest.raises(ValueError):
        impl.parse('{"a":1,"a":2}', on_duplicate_key="error")


@pytest.mark.part3
@pytest.mark.edge
def test_no_duplicate_keys_both_policies_agree(impl):
    v1 = impl.parse('{"a":1,"b":2}', on_duplicate_key="last")
    v2 = impl.parse('{"a":1,"b":2}', on_duplicate_key="error")
    assert impl.serialize(v1) == impl.serialize(v2) == '{"a":1,"b":2}'


@pytest.mark.part3
@pytest.mark.edge
def test_query_path_object_and_array_composition(impl):
    doc = impl.parse('{"a":{"b":[1,2,{"c":3}]}}')
    assert impl.query_path(doc, "a.b[2].c") == "3"
    assert impl.query_path(doc, "a.b[0]") == "1"
    assert impl.query_path(doc, "") == '{"a":{"b":[1,2,{"c":3}]}}'


@pytest.mark.part3
@pytest.mark.edge
def test_query_path_missing_key_raises_keyerror(impl):
    doc = impl.parse('{"a":1}')
    with pytest.raises(KeyError):
        impl.query_path(doc, "z")


@pytest.mark.part3
@pytest.mark.edge
def test_query_path_index_out_of_range_raises_indexerror(impl):
    doc = impl.parse("[1,2,3]")
    with pytest.raises(IndexError):
        impl.query_path(doc, "[10]")


@pytest.mark.part3
@pytest.mark.edge
def test_query_path_type_mismatch_raises_valueerror(impl):
    doc = impl.parse('{"a":1}')
    with pytest.raises(ValueError):
        impl.query_path(doc, "a.b")  # a is a number, cannot descend with a key
    doc2 = impl.parse("[1,2,3]")
    with pytest.raises(ValueError):
        impl.query_path(doc2, "x")  # top-level is an array, cannot look up a key


# ------------------------------------------------------------------------ cross-check vs stdlib json
def _random_json_value(rng: random.Random, depth: int = 0):
    if depth >= 3:
        choices = ["int", "float", "str", "bool", "null"]
    else:
        choices = ["int", "float", "str", "bool", "null", "list", "dict"]
    kind = rng.choice(choices)
    if kind == "int":
        return rng.randint(-10_000, 10_000)
    if kind == "float":
        return round(rng.uniform(-1000, 1000), rng.randint(0, 6))
    if kind == "str":
        alphabet = string.ascii_letters + string.digits + " \t\n\"\\/:,{}[]" + "café日本語"
        return "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 12)))
    if kind == "bool":
        return rng.choice([True, False])
    if kind == "null":
        return None
    if kind == "list":
        return [_random_json_value(rng, depth + 1) for _ in range(rng.randint(0, 4))]
    # dict
    return {
        f"k{rng.randint(0, 20)}": _random_json_value(rng, depth + 1) for _ in range(rng.randint(0, 4))
    }


@pytest.mark.part1
def test_random_cross_check_validity_and_value_against_stdlib_json(impl):
    """Generate random Python objects, dump them with the stdlib json module (which never
    produces NaN/Infinity or lone surrogates for these inputs), then confirm our parser accepts
    the text and, after round-tripping through Python's json.loads on both sides, produces the
    same logical value. Known, documented divergences from json.loads (bare NaN/Infinity, lone
    surrogate \\u escapes) are exercised separately above, not here."""
    rng = random.Random(0)
    for _ in range(200):
        obj = _random_json_value(rng)
        text = json.dumps(obj)
        minified = impl.minify(text)
        assert json.loads(minified) == obj


@pytest.mark.part1
@pytest.mark.edge
def test_random_cross_check_invalid_mutations_are_rejected(impl):
    """Take valid JSON text and apply small mutations that should make it invalid (drop a
    closing bracket, inject a trailing comma); our parser must reject every one, matching
    json.loads."""
    rng = random.Random(1)
    valid_docs = [
        '{"a":1,"b":[1,2,3]}',
        "[1,2,3]",
        '{"nested":{"x":1}}',
        '"just a string"',
        "42",
    ]
    mutations = [
        lambda t: t[:-1],  # drop last character (often a closing bracket/quote)
        lambda t: t + ",",  # trailing garbage
        lambda t: t.replace(":", "", 1) if ":" in t else t + "x",
        lambda t: t[1:] if t else t,  # drop first character
    ]
    for doc in valid_docs:
        for mutate in mutations:
            mutated = mutate(doc)
            try:
                json.loads(mutated)
                continue  # mutation happened to still be valid JSON; skip (not a useful case)
            except (ValueError, json.JSONDecodeError):
                pass
            with pytest.raises(ValueError):
                impl.parse(mutated)


# ------------------------------------------------------------------------ fmt / io
@pytest.mark.part1
@pytest.mark.fmt
def test_output_has_no_extraneous_whitespace(impl):
    out = impl.minify('{ "a" : [ 1 , 2 ] , "b" : { "c" : 3 } }')
    assert " " not in out
    assert out == '{"a":[1,2],"b":{"c":3}}'


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script('PART 1\nPARSE {"a": 1, "b": [1,2,3]}\nPARSE {"a":1,}\n')
    assert r.returncode == 0, r.stderr
    assert r.stdout == '{"a":1,"b":[1,2,3]}\nINVALID\n'


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_part3(run_script):
    r = run_script(
        'PART 3\nPARSE_DUP last {"a":1,"a":2}\nPARSE_DUP error {"a":1,"a":2}\n'
        'PATH a.b[2].c {"a":{"b":[1,2,{"c":3}]}}\n'
    )
    assert r.returncode == 0, r.stderr
    assert r.stdout == '{"a":2}\nDUPLICATE\n3\n'
