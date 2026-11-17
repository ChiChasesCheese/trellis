import importlib
import io
import itertools
import json
import os
import random
import re

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

INT_MAX, INT_MIN = 2**63 - 1, -(2**63)
BASE = {
    "rating": 5, "value_cents": 0, "account_age_days": 400,
    "days_since_purchase": 7, "opened": False, "final_sale": False,
}


def request(**changes):
    return {**BASE, **changes}


def line(**changes):
    return json.dumps(request(**changes), separators=(",", ":"))


def assert_error(call, code):
    with pytest.raises(ValueError, match=f"^{code}$"):
        call()


def invalid_json(text):
    assert_error(lambda: impl.parse(text), "invalid_json")


def invalid_request(value):
    assert_error(lambda: impl.evaluate(value), "invalid_request")


def run(*lines):
    return list(impl.run(lines))


# ---- 合同里的例子 ----

def test_contract_example():
    out = run((line(rating=4, value_cents=10000, account_age_days=29, days_since_purchase=30) + "\n").encode())
    assert out == ['{"eligible":true,"reason":"eligible","risk":50}']


def test_day_thirty_is_inside_the_window_and_day_thirty_one_is_not():
    assert impl.evaluate(request(days_since_purchase=30)) == impl.Decision(True, "eligible", 0)
    assert impl.evaluate(request(days_since_purchase=31)) == impl.Decision(False, "window_expired", 0)


def test_malformed_object_is_invalid_json():
    invalid_json("{oops}")


# ---- 语法：接受什么 ----

def test_empty_object_and_whitespace_variants():
    assert impl.parse("{}") == {}
    assert impl.parse(" \t\r\n{ \r\n} \t\r\n") == {}
    assert impl.parse('{ "a" \t:\r\n 1 ,\n"b" : true }') == {"a": 1, "b": True}


def test_value_types_and_boolean_stays_boolean():
    parsed = impl.parse('{"i":7,"t":true,"f":false,"s":"x"}')
    assert parsed == {"i": 7, "t": True, "f": False, "s": "x"}
    assert type(parsed["i"]) is int and type(parsed["t"]) is bool and type(parsed["f"]) is bool


@pytest.mark.parametrize("text, expected", [
    ("0", 0), ("-0", 0), ("7", 7), ("-7", -7), ("10", 10),
    (str(INT_MAX), INT_MAX), (str(INT_MIN), INT_MIN),
])
def test_integers_accepted_including_both_signed_limits(text, expected):
    parsed = impl.parse('{"n":' + text + "}")
    assert parsed == {"n": expected} and type(parsed["n"]) is int


def test_string_escapes_decode_and_controls_may_be_escaped():
    parsed = impl.parse(r'{"k":"q\"b\\s\/\b\f\n\r\t"}')
    assert parsed == {"k": 'q"b\\s/\b\f\n\r\t'}
    assert impl.parse('{"a b":" x "}') == {"a b": " x "}
    assert impl.parse('{"~":"' + "".join(chr(c) for c in range(32, 127) if chr(c) not in '"\\') + '"}')


def test_parse_accepts_crlf_inside_its_argument():
    assert impl.parse('{"a":1,\r\n"b":2}\r\n') == {"a": 1, "b": 2}


# ---- 语法：拒绝什么 ----

@pytest.mark.parametrize("text", [
    "", " ", "{", "}", "{oops}", "[]", "[1]", "1", '"s"', "true", "null",
    '{"a"}', '{"a":}', '{"a" 1}', "{a:1}", "{'a':1}", '{"a":1,}', '{,"a":1}', '{"a":1 "b":2}', '{"a":1,,"b":2}',
    '{"a":1', '{"a":1,', '{"a"', '{"a":', '{"a":"x', '{"a":"x"',
    '{"a":[1]}', '{"a":{}}', '{"a":{"b":1}}', '{"a":null}', '{"a":NaN}', '{"a":Infinity}',
    '{"a":True}', '{"a":TRUE}', '{"a":tru}', '{"a":truex}', '{"a":falsey}',
    '{"a":1.5}', '{"a":1.0}', '{"a":1e5}', '{"a":1E5}', '{"a":-1.}', '{"a":.5}', '{"a":-}', '{"a":--1}',
    '{"a":+1}', '{"a":01}', '{"a":-01}', '{"a":00}', '{"a":0x1}', '{"a":1_0}',
    '{"a":"\\u0041"}', '{"a":"\\x41"}', '{"a":"\\a"}', '{"a":"\\\'"}', '{"a":"\\', '{"a":"\\"}',
    '{"a":"tab\there"}', '{"a":"new\nline"}', '{"a":"nul\x00"}', '{"a":"del\x7f"}', '{"a":"é"}', '{"é":1}', '{"a":"\u2028"}',
    '{"a":1}x', '{"a":1} {"b":2}', '{"a":1}}', '{"a":1},', '{"a":1}\x00', '{"a":1}\x0b', '{"a":1}\x0c',
    '\x0b{"a":1}', '\ufeff{"a":1}', '\xa0{"a":1}',
    "{\"a\":'x'}", '{a}', '{"a":"x"} garbage',
])
def test_syntax_rejected(text):
    invalid_json(text)


def test_non_string_argument_is_invalid_json():
    for bad in (None, 5, b"{}", ["{}"]):
        assert_error(lambda bad=bad: impl.parse(bad), "invalid_json")


def test_deep_nesting_is_invalid_json_and_never_a_crash():
    invalid_json('{"a":' + "[" * 200_000 + "]" * 200_000 + "}")
    invalid_json('{"a":' + '{"b":' * 100_000 + "1" + "}" * 100_000 + "}")


def test_unicode_digits_are_not_integers():
    invalid_json('{"a":1٢٣}')  # 阿拉伯-印度数字：int() 认得，语法不认
    invalid_json('{"a":1２}')  # 全角数字
    invalid_json('{"a":٣}')


# ---- 重复键 ----

@pytest.mark.parametrize("text", [
    '{"a":1,"a":2}', '{"a":1,"a":1}', '{"a":1,"b":2,"a":3}', '{"a":true,"a":false}',
    r'{"a/b":1,"a\/b":2}', r'{"a\\":1,"a\\":2}', '{"":1,"":2}',
])
def test_duplicate_decoded_keys_rejected(text):
    invalid_json(text)


def test_keys_that_differ_only_in_case_or_escape_meaning_are_distinct():
    assert impl.parse('{"a":1,"A":2}') == {"a": 1, "A": 2}
    assert impl.parse(r'{"a\\n":1,"a\n":2}') == {"a\\n": 1, "a\n": 2}


# ---- 整数溢出与完整消费 ----

@pytest.mark.parametrize("text", [
    str(INT_MAX + 1), str(INT_MIN - 1), "9223372036854775808", "-9223372036854775809",
    "99999999999999999999", "-99999999999999999999", "10" * 30, "9" * 5000, "-" + "9" * 5000,
    "1" + "0" * 4999,
])
def test_overflow_is_invalid_json_not_zero_and_not_another_error(text):
    invalid_json('{"n":' + text + "}")


def test_leading_zero_run_is_not_a_long_valid_number():
    invalid_json('{"n":' + "0" * 25 + "}")


@pytest.mark.parametrize("tail", ["x", "{}", ",", "}", '"', "0", "1", "[", "true", "\x00", " ,"])
def test_trailing_content_after_a_valid_object_is_rejected(tail):
    invalid_json('{"a":1}' + tail)
    invalid_json('{"a":1} \r\n' + tail)


def test_trailing_whitespace_is_fine():
    assert impl.parse('{"a":1} \t\r\n ') == {"a": 1}


# ---- 请求校验 ----

def test_missing_and_extra_fields_are_invalid_request():
    for key in BASE:
        invalid_request({k: v for k, v in BASE.items() if k != key})
    invalid_request({**BASE, "coupon": "x"})
    invalid_request({**BASE, "extra": 1, "more": 2})
    invalid_request({})
    invalid_request({**{k: v for k, v in BASE.items() if k != "opened"}, "extra": True})


@pytest.mark.parametrize("bad", [None, [], (), "x", 5, True, [("rating", 5)], BASE.items()])
def test_non_dict_request_is_invalid_request(bad):
    invalid_request(bad)


@pytest.mark.parametrize("field", ["rating", "value_cents", "account_age_days", "days_since_purchase"])
@pytest.mark.parametrize("bad", [True, False, 1.0, "1", None, [1], {"v": 1}, b"1"])
def test_integer_fields_refuse_every_other_type_including_bool(field, bad):
    invalid_request(request(**{field: bad}))


@pytest.mark.parametrize("field", ["opened", "final_sale"])
@pytest.mark.parametrize("bad", [0, 1, 1.0, "true", "false", None, [], [True]])
def test_boolean_fields_refuse_every_other_type(field, bad):
    invalid_request(request(**{field: bad}))


@pytest.mark.parametrize("bad", [0, 6, -1, 100, INT_MAX])
def test_rating_range(bad):
    invalid_request(request(rating=bad))


@pytest.mark.parametrize("field", ["value_cents", "account_age_days", "days_since_purchase"])
def test_nonnegative_signed_64_bit_range(field):
    assert impl.evaluate(request(**{field: 0})).risk >= 0
    assert impl.evaluate(request(**{field: INT_MAX})) is not None
    invalid_request(request(**{field: -1}))
    invalid_request(request(**{field: INT_MAX + 1}))
    invalid_request(request(**{field: 10**100}))
    invalid_request(request(**{field: INT_MIN}))


def test_every_field_is_validated_before_any_decision():
    # final_sale 本来会立刻决定；别处的无效字段仍然要先被发现
    invalid_request(request(final_sale=True, rating=0))
    invalid_request(request(final_sale=True, value_cents=-1))
    invalid_request(request(final_sale=True, opened="yes"))
    invalid_request(request(final_sale=True, days_since_purchase=10**30))
    invalid_request({**request(final_sale=True), "x": 1})


def test_evaluate_does_not_modify_the_request():
    original = request(rating=2, value_cents=12_345, opened=True)
    snapshot = dict(original)
    impl.evaluate(original)
    assert original == snapshot


# ---- 风险分与拒绝顺序（期望值由测试里独立写出的表给出）----

def oracle_risk(rating, value, age):
    value_points = 30 if value >= 50_000 else 15 if value >= 10_000 else 0
    age_points = 25 if age < 30 else 10 if age < 180 else 0
    return (5 - rating) * 10 + value_points + age_points


def oracle_decision(rating, value, age, days, opened, final_sale):
    risk = oracle_risk(rating, value, age)
    if final_sale:
        return False, "final_sale", risk
    if days > 30:
        return False, "window_expired", risk
    if opened and value >= 10_000:
        return False, "opened_high_value", risk
    if risk >= 60:
        return False, "high_risk", risk
    return True, "eligible", risk


@pytest.mark.parametrize("value, points", [
    (0, 0), (1, 0), (9_999, 0), (10_000, 15), (10_001, 15), (49_999, 15), (50_000, 30), (50_001, 30), (INT_MAX, 30)])
def test_value_points_at_every_boundary(value, points):
    assert impl.evaluate(request(rating=5, value_cents=value, account_age_days=180)).risk == points


@pytest.mark.parametrize("age, points", [
    (0, 25), (1, 25), (29, 25), (30, 10), (31, 10), (179, 10), (180, 0), (181, 0), (INT_MAX, 0)])
def test_age_points_at_every_boundary(age, points):
    assert impl.evaluate(request(rating=5, account_age_days=age)).risk == points


@pytest.mark.parametrize("rating, points", [(1, 40), (2, 30), (3, 20), (4, 10), (5, 0)])
def test_rating_points(rating, points):
    assert impl.evaluate(request(rating=rating)).risk == points


def test_reason_order_when_several_rules_apply():
    all_bad = dict(rating=1, value_cents=60_000, account_age_days=0, days_since_purchase=99, opened=True, final_sale=True)
    assert impl.evaluate(request(**all_bad)).reason == "final_sale"
    assert impl.evaluate(request(**{**all_bad, "final_sale": False})).reason == "window_expired"
    assert impl.evaluate(request(**{**all_bad, "final_sale": False, "days_since_purchase": 30})).reason == "opened_high_value"
    assert impl.evaluate(request(**{**all_bad, "final_sale": False, "days_since_purchase": 30, "opened": False})).reason == "high_risk"


def test_high_risk_boundary_uses_inputs_that_do_not_move_other_boundaries():
    # 风险 = 20 + 15 + 25 = 60，恰好 reject；金额 49999 没有触发 opened_high_value 的前提（未打开）
    assert impl.evaluate(request(rating=3, value_cents=49_999, account_age_days=0)) == impl.Decision(False, "high_risk", 60)
    # 风险 = 30 + 0 + 25 = 55，仍然 eligible
    assert impl.evaluate(request(rating=2, value_cents=9_999, account_age_days=0)) == impl.Decision(True, "eligible", 55)


def test_opened_high_value_boundary():
    assert impl.evaluate(request(opened=True, value_cents=9_999)).eligible is True
    assert impl.evaluate(request(opened=True, value_cents=10_000)) == impl.Decision(False, "opened_high_value", 15)
    assert impl.evaluate(request(opened=False, value_cents=10_000)).eligible is True


def test_risk_is_reported_for_every_rejection():
    for final, days, opened, rating in itertools.product([True, False], [30, 31], [True, False], [1, 5]):
        got = impl.evaluate(request(final_sale=final, days_since_purchase=days, opened=opened, rating=rating, value_cents=20_000))
        assert got.risk == oracle_risk(rating, 20_000, 180)
        assert got.eligible == (got.reason == "eligible")


def test_whole_grid_against_the_independent_oracle():
    ratings, values = [1, 3, 4, 5], [0, 9_999, 10_000, 49_999, 50_000]
    ages, days_list = [0, 29, 30, 179, 180], [0, 30, 31]
    for rating, value, age, days, opened, final in itertools.product(ratings, values, ages, days_list, [False, True], [False, True]):
        got = impl.evaluate(request(rating=rating, value_cents=value, account_age_days=age,
                                    days_since_purchase=days, opened=opened, final_sale=final))
        assert (got.eligible, got.reason, got.risk) == oracle_decision(rating, value, age, days, opened, final)


def test_decision_is_a_frozen_value():
    got = impl.evaluate(request())
    assert got == impl.Decision(True, "eligible", 0)
    with pytest.raises(Exception):
        got.risk = 5


# ---- 命令行驱动：行、隔离、输出 ----

def test_driver_one_output_line_per_input_line_in_order():
    ok = line().encode()
    out = run(ok + b"\n", b'{"rating":1}\n', b"not json\n", line(final_sale=True).encode() + b"\n")
    assert out == [
        '{"eligible":true,"reason":"eligible","risk":0}',
        '{"error":"invalid_request"}',
        '{"error":"invalid_json"}',
        '{"eligible":false,"reason":"final_sale","risk":0}',
    ]


def test_driver_blank_and_whitespace_lines_are_invalid_json_and_do_not_stop_later_lines():
    out = run(b"\n", b"   \n", b"\r\n", (line() + "\n").encode())
    assert out == ['{"error":"invalid_json"}'] * 3 + ['{"eligible":true,"reason":"eligible","risk":0}']


def test_driver_empty_input_has_no_output():
    assert run() == []
    assert list(impl.run(io.BytesIO(b""))) == []


def test_driver_non_ascii_bytes_are_invalid_json_and_isolated():
    out = run('{"a":"é"}\n'.encode("utf-8"), b'{"a":"\xff"}\n', (line() + "\n").encode())
    assert out[:2] == ['{"error":"invalid_json"}'] * 2
    assert json.loads(out[2])["eligible"] is True


def test_driver_last_line_without_newline_and_crlf_lines():
    out = run((line() + "\r\n").encode(), line(rating=1).encode())
    assert [json.loads(o)["risk"] for o in out] == [0, 40]


def test_driver_reads_a_binary_stream_line_by_line():
    data = (line() + "\n").encode() * 2 + b"{\n"
    out = list(impl.run(io.BytesIO(data)))
    assert out[2] == '{"error":"invalid_json"}' and len(out) == 3


def test_driver_does_not_join_physical_lines():
    # 一个对象拆成两行：每一行单独都是坏的
    half = line()[:40], line()[40:]
    out = run((half[0] + "\n").encode(), (half[1] + "\n").encode())
    assert out == ['{"error":"invalid_json"}'] * 2


def test_driver_output_lines_are_compact_json_with_stable_key_order():
    out = run((line(rating=1, final_sale=True) + "\n").encode())[0]
    assert out == '{"eligible":false,"reason":"final_sale","risk":40}'
    assert "\n" not in out and " " not in out


def test_driver_syntax_error_wins_over_request_error_and_codes_are_exact():
    # 语法不对时，即使字段也不对，也是 invalid_json
    assert run(b'{"rating":"x"\n') == ['{"error":"invalid_json"}']
    assert run(b'{"rating":"x"}\n') == ['{"error":"invalid_request"}']
    # 溢出是语法层：既不是 0，也不是 invalid_request，也不是别的错误文本
    assert run((line(value_cents=2**63) + "\n").encode()) == ['{"error":"invalid_json"}']
    assert run(('{"rating":' + "9" * 5000 + "}\n").encode()) == ['{"error":"invalid_json"}']


def test_driver_every_output_line_is_valid_json_with_only_known_keys():
    inputs = [b"\n", b"{\n", b'{"a":1}\n', (line() + "\n").encode(), b"\xff\n", b'{"a":1,"a":2}\n']
    for out in run(*inputs):
        parsed = json.loads(out)
        assert set(parsed) in ({"eligible", "reason", "risk"}, {"error"})
        if "error" in parsed:
            assert parsed["error"] in ("invalid_json", "invalid_request")


# ---- 与标准库对拍：同一批变异输入，验收结果必须相同 ----

BAD_TEXT = re.compile(r"[^\x00-\x7e]|(?<!\\)(?:\\\\)*\\u")  # 非 ASCII、DEL，以及真正的 \u 转义


def _reject(_):
    raise ValueError


def _unique(items):
    keys = [k for k, _ in items]
    if len(set(keys)) != len(keys):
        raise ValueError
    return dict(items)


def oracle_parse(text):
    """成熟的 JSON 库加上子集的额外限制：解析器的另一种写法，用来对拍。"""
    if type(text) is not str or BAD_TEXT.search(text):
        raise ValueError
    try:
        data = json.loads(text, parse_float=_reject, parse_constant=_reject, object_pairs_hook=_unique)
    except RecursionError:
        raise ValueError from None
    ok_value = lambda v: type(v) in (bool, str) or (type(v) is int and INT_MIN <= v <= INT_MAX)
    if type(data) is not dict or not all(ok_value(v) for v in data.values()):
        raise ValueError
    return data


def accepts(fn, text):
    try:
        return ("ok", fn(text))
    except ValueError as error:
        if str(error) == "invalid_json" or fn is oracle_parse:
            return ("bad", None)
        raise


def test_parse_agrees_with_a_stricter_standard_library_oracle_on_mutations():
    rng = random.Random(20261116)
    seeds = [
        '{"a":1,"b":true,"c":"x\\ny"}', '{"rating":5,"opened":false}', '{ "k" : -0 , "m":"\\/" }', "{}",
        '{"n":9223372036854775807}', '{"n":-9223372036854775808}', '{"s":"a\\\\b"}',
    ]
    alphabet = ['"', "\\", "{", "}", ",", ":", " ", "\n", "-", "0", "9", "a", "u", "t", "e", ".", "[", "1", "\t", "\x01"]
    checked = 0
    for seed in seeds:
        for _ in range(600):
            text = list(seed)
            for _ in range(rng.randint(1, 3)):
                op = rng.choice(["ins", "del", "rep"])
                i = rng.randrange(len(text) + 1)
                if op == "ins":
                    text.insert(i, rng.choice(alphabet))
                elif op == "del" and text:
                    del text[min(i, len(text) - 1)]
                elif text:
                    text[min(i, len(text) - 1)] = rng.choice(alphabet)
            candidate = "".join(text)
            assert accepts(impl.parse, candidate) == accepts(oracle_parse, candidate), repr(candidate)
            checked += 1
    assert checked == 4200
