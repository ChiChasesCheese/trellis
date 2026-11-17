import copy
import dataclasses
import importlib
import os
import random
import re

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))
PaymentForm = impl.PaymentForm
ActionError = impl.ActionError
apply_action = impl.apply_action

NAMES = ("number", "name", "month", "year", "cvv")
MESSAGES = {
    "number": "Invalid Card Number",
    "name": "Invalid Card Name",
    "month": "Invalid Month",
    "year": "Invalid Year",
    "cvv": "Invalid CVV",
}
GOOD = {"number": "4000123412341234", "name": "Ada", "month": "11", "year": "2030", "cvv": "042"}  # 年份按当前年份 2029 算


def filled(year=2029, touch=True):
    form = PaymentForm(year)
    for name in NAMES:
        form.change(name, GOOD[name] if name != "year" else str(year + 2))
        if touch:
            form.blur(name)
    return form


def plain(snap):
    return dataclasses.asdict(snap)


def field(form, name):
    return form.snapshot().fields[name]


def test_initial_state_is_empty_untouched_and_silent():
    snap = PaymentForm(2029).snapshot()
    assert list(snap.fields) == list(NAMES)
    for state in snap.fields.values():
        assert (state.value, state.touched, state.valid, state.error) == ("", False, False, None)
    assert snap.canSubmit is False


def test_change_stores_exactly_and_does_not_touch():
    form = PaymentForm(2029)
    form.change("name", "  Ada \n")
    state = field(form, "name")
    assert state.value == "  Ada \n"
    assert state.touched is False and state.valid is False and state.error is None


def test_blur_touches_and_survives_later_changes():
    form = PaymentForm(2029)
    form.blur("cvv")
    assert field(form, "cvv").touched is True
    form.change("cvv", "123")
    form.change("cvv", "")
    assert field(form, "cvv").touched is True
    assert field(form, "month").touched is False  # 别的字段不受影响
    form.blur("cvv")  # 重复失焦无副作用
    assert field(form, "cvv").touched is True


def test_error_is_visible_only_after_touch_and_clears_when_fixed():
    form = PaymentForm(2029)
    form.change("month", "13")
    assert field(form, "month").error is None  # 无效但未触碰
    form.blur("month")
    assert field(form, "month").error == "Invalid Month"
    form.change("month", "12")
    state = field(form, "month")
    assert state.valid is True and state.error is None  # 改对后立刻消失
    form.change("month", "00")
    assert field(form, "month").error == "Invalid Month"  # 已触碰：再改错立刻又出现


def test_blur_on_a_never_edited_field_shows_the_error():
    form = PaymentForm(2029)
    form.blur("number")
    state = field(form, "number")
    assert (state.value, state.valid, state.error) == ("", False, "Invalid Card Number")


@pytest.mark.parametrize(
    ("name", "good", "bad"),
    [
        ("number", ["0000000000000000", "9876543210987654"], ["", "123456789012345", "12345678901234567", "1234 5678 9012 3456", "123456789012345a"]),
        ("name", ["A", "z", "AdaLovelace"], ["", "Ada Lovelace", "Ada1", "Ada-L", "Zoë", "Ada\n", " Ada"]),
        ("month", ["01", "09", "10", "12"], ["", "1", "00", "13", "001", "0a", "+1", "-1", " 1", "1 ", "99"]),
        ("cvv", ["000", "007", "999"], ["", "7", "07", "0007", "12a", "-12", "+12", "1 2", "12\n"]),
    ],
)
def test_format_rules(name, good, bad):
    for text in good:
        form = PaymentForm(2029)
        form.change(name, text)
        assert field(form, name).valid is True, text
    for text in bad:
        form = PaymentForm(2029)
        form.change(name, text)
        form.blur(name)
        state = field(form, name)
        assert (state.valid, state.error) == (False, MESSAGES[name]), repr(text)


@pytest.mark.parametrize("name", ["number", "month", "year", "cvv"])
def test_non_ascii_digits_are_rejected(name):
    length = {"number": 16, "month": 2, "year": 4, "cvv": 3}[name]
    for digit in ("٣", "３", "²", "५"):  # 阿拉伯-印度数字、全角、上标、天城文
        form = PaymentForm(2029)
        form.change(name, digit * length)
        assert field(form, name).valid is False, (name, digit)


def test_year_window_is_inclusive_and_four_ascii_digits():
    form = PaymentForm(2040)
    verdicts = {}
    for text in ("2039", "2040", "2041", "2042", "2043", "2044", "02040", "204", "٢٠٤٠", " 2040"):
        form.change("year", text)
        verdicts[text] = field(form, "year").valid
    assert [t for t, ok in verdicts.items() if ok] == ["2040", "2041", "2042", "2043"]


@pytest.mark.parametrize("year", [2000, 2096])
def test_year_window_at_both_ends_of_the_allowed_range(year):
    form = PaymentForm(year)
    for offset, ok in [(-1, False), (0, True), (3, True), (4, False)]:
        form.change("year", str(year + offset))
        assert field(form, "year").valid is ok, (year, offset)


def test_month_and_year_are_independent():
    form = PaymentForm(2029)
    for month in ("01", "06", "12"):
        form.change("month", month)
        form.change("year", "2029")
        assert field(form, "month").valid and field(form, "year").valid


def test_can_submit_needs_every_field_valid_and_touched():
    form = filled()
    assert form.snapshot().canSubmit is True
    # 有效但没失焦
    fresh = filled(touch=False)
    assert fresh.snapshot().canSubmit is False
    for name in NAMES:
        fresh.blur(name)
    assert fresh.snapshot().canSubmit is True
    # 失焦了但有一个无效：改动立刻生效
    form.change("cvv", "4")
    assert form.snapshot().canSubmit is False
    form.change("cvv", "421")
    assert form.snapshot().canSubmit is True


@pytest.mark.parametrize("missing", NAMES)
def test_one_untouched_field_blocks_submit(missing):
    form = PaymentForm(2029)
    for name in NAMES:
        form.change(name, GOOD[name] if name != "year" else "2030")
        if name != missing:
            form.blur(name)
    assert form.snapshot().canSubmit is False
    form.blur(missing)
    assert form.snapshot().canSubmit is True


def test_touch_all_reveals_every_error_at_once_and_changes_no_value():
    form = PaymentForm(2029)
    form.change("month", "13")
    form.change("cvv", "123")
    form.touch_all()
    snap = form.snapshot()
    assert [s.touched for s in snap.fields.values()] == [True] * 5
    assert {n: s.error for n, s in snap.fields.items()} == {
        "number": "Invalid Card Number", "name": "Invalid Card Name", "month": "Invalid Month", "year": "Invalid Year", "cvv": None,
    }
    assert snap.fields["month"].value == "13" and snap.canSubmit is False


def test_first_invalid_follows_page_order_and_ignores_touch():
    form = PaymentForm(2029)
    assert form.first_invalid() == "number"
    form.change("number", "1" * 16)
    form.change("name", "Ada")
    assert form.first_invalid() == "month"
    form.change("month", "05")
    form.change("year", "2031")
    assert form.first_invalid() == "cvv"
    form.change("cvv", "123")
    assert form.first_invalid() is None
    form.change("name", "A da")
    assert form.first_invalid() == "name"


def test_reset_clears_values_and_touched_but_keeps_the_year():
    form = filled(year=2033)
    form.reset()
    snap = form.snapshot()
    for state in snap.fields.values():
        assert (state.value, state.touched, state.valid, state.error) == ("", False, False, None)
    assert snap.canSubmit is False
    form.change("year", "2036")  # 窗口末端仍按 2033 算
    form.change("year", "2037")
    assert field(form, "year").valid is False
    form.change("year", "2036")
    assert field(form, "year").valid is True


def test_snapshots_are_independent_of_the_form_and_of_each_other():
    form = filled()
    before = form.snapshot()
    frozen = copy.deepcopy(plain(before))
    form.change("name", "Grace")
    form.reset()
    form.change("number", "1")
    assert plain(before) == frozen  # 之后的操作不改旧快照

    mine = form.snapshot()
    expected = copy.deepcopy(plain(mine))
    for state in list(mine.fields.values()):  # 肆意改返回值
        try:
            state.value, state.touched, state.valid, state.error = "x", True, True, "boom"
        except Exception:
            pass
    for tamper in (lambda: mine.fields.clear(), lambda: mine.fields.update(extra=None), lambda: setattr(mine, "canSubmit", True)):
        try:
            tamper()
        except Exception:
            pass
    assert plain(form.snapshot()) == expected
    assert plain(form.snapshot()) == plain(form.snapshot())


def test_forms_do_not_share_state():
    a, b = PaymentForm(2029), PaymentForm(2050)
    a.change("number", "1" * 16)
    a.blur("number")
    assert field(b, "number").value == "" and field(b, "number").touched is False
    b.reset()
    assert field(a, "number").value == "1" * 16
    a.change("year", "2029")
    b.change("year", "2029")
    assert field(a, "year").valid is True and field(b, "year").valid is False


def test_walkthrough_with_a_space_in_the_name():
    form = PaymentForm(2029)
    form.change("name", "Ada Lovelace")
    form.blur("name")
    state = field(form, "name")
    assert (state.value, state.touched, state.valid, state.error) == ("Ada Lovelace", True, False, "Invalid Card Name")
    form.reset()
    assert plain(form.snapshot()) == plain(PaymentForm(2029).snapshot())


def test_full_flow_then_shortening_the_cvv_disables_submit():
    form = PaymentForm(2029)
    for name, text in [("number", "5500123412341234"), ("name", "Ada"), ("month", "03"), ("year", "2032"), ("cvv", "042")]:
        form.change(name, text)
        form.blur(name)
    assert form.snapshot().canSubmit is True
    form.change("cvv", "42")
    snap = form.snapshot()
    assert snap.canSubmit is False and snap.fields["cvv"].error == "Invalid CVV"


def test_leading_zeros_are_kept():
    form = PaymentForm(2029)
    form.change("month", "07")
    form.change("cvv", "000")
    assert field(form, "month").value == "07" and field(form, "cvv").value == "000"
    assert field(form, "month").valid and field(form, "cvv").valid


def test_bad_calls_raise_and_change_nothing():
    form = filled()
    before = plain(form.snapshot())
    with pytest.raises(ValueError):
        form.change("card", "1")
    with pytest.raises(ValueError):
        form.blur("")
    with pytest.raises(TypeError):
        form.change("cvv", 123)
    with pytest.raises(TypeError):
        form.change("cvv", None)
    assert plain(form.snapshot()) == before


@pytest.mark.parametrize("year", [1999, 2097, 2026.0, "2026", None, True])
def test_constructor_rejects_a_year_outside_the_contract(year):
    with pytest.raises(ValueError):
        PaymentForm(year)


def oracle(name, year, text):
    patterns = {
        "number": r"[0-9]{16}",
        "name": r"[A-Za-z]+",
        "month": r"0[1-9]|1[0-2]",
        "cvv": r"[0-9]{3}",
    }
    if name == "year":
        return re.fullmatch(r"[0-9]{4}", text) is not None and year <= int(text) <= year + 3
    return re.fullmatch(patterns[name], text) is not None


def test_random_strings_agree_with_a_regex_oracle():
    rng = random.Random(20261117)
    alphabet = list("0123456789ABCabc \n+-_.") + ["٣", "３", "²", "é", "\t"]
    for _ in range(4000):
        year = rng.randint(2000, 2096)
        name = rng.choice(NAMES)
        size = rng.choice([0, 1, 2, 3, 4, 16, 17]) if rng.random() < 0.7 else rng.randint(0, 6)
        if rng.random() < 0.5:
            text = "".join(rng.choice("0123456789") for _ in range(size))
        else:
            text = "".join(rng.choice(alphabet) for _ in range(size))
        if name == "year" and rng.random() < 0.5:
            text = str(year + rng.randint(-2, 6))
        form = PaymentForm(year)
        form.change(name, text)
        assert field(form, name).valid is oracle(name, year, text), (name, year, text)


def test_apply_action_runs_each_action_and_returns_plain_data():
    form = PaymentForm(2029)
    out = apply_action(form, {"action": "change", "field": "cvv", "value": "9"})
    assert out["fields"]["cvv"]["value"] == "9" and isinstance(out["fields"]["cvv"], dict)
    out = apply_action(form, {"action": "blur", "field": "cvv"})
    assert out["fields"]["cvv"]["error"] == "Invalid CVV"
    out["fields"]["cvv"]["error"] = "tampered"
    assert field(form, "cvv").error == "Invalid CVV"
    out = apply_action(form, {"action": "reset"})
    assert out["fields"]["cvv"]["value"] == "" and out["canSubmit"] is False


@pytest.mark.parametrize(
    "body",
    [
        None, [], "reset", 7, {},
        {"action": "reset", "field": "cvv"},
        {"action": "blur"},
        {"action": "blur", "field": "cvv", "value": "1"},
        {"action": "change", "field": "cvv"},
        {"action": "change", "field": "cvv", "value": 1},
        {"action": "change", "field": "cvv", "value": None},
        {"action": "change", "field": ["cvv"], "value": "1"},
        {"action": "change", "field": "zip", "value": "1"},
        {"action": "jump", "field": "cvv"},
        {"action": ["reset"]},
    ],
)
def test_malformed_actions_are_rejected_before_touching_the_form(body):
    form = filled()
    before = plain(form.snapshot())
    with pytest.raises(ActionError):
        apply_action(form, body)
    assert plain(form.snapshot()) == before
