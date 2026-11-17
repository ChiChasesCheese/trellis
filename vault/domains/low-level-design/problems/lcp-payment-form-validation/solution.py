"""支付表单校验（PaymentForm）参考解。

设计五行：
1. 每个字段只存两样东西：用户敲进去的原始字符串、是否失焦过（`_Entry`）；有效性和错误文字都不存。
2. 有效性由 `Rule` 表按字段名查出来：一条规则 = 错误文字 + 一个只看字符串的判定函数；年份窗口由注入的当前年份在构造时算好。
3. `snapshot()` 每次从头算：valid = 规则通过；error = 已触碰且无效时才是规则文字；canSubmit = 五个字段都 valid 且 touched。
4. 返回给调用方的永远是新对象（新字典、新 `FieldState`），内部状态不外泄；字符串本身不可变，可以放心共享。
5. `apply_action` 是 HTTP 边界：只认三种动作的精确键集合与字符串类型，形状不对就抛 `ActionError`，表单状态一点不动。
"""
from __future__ import annotations

import dataclasses
from collections.abc import Callable
from dataclasses import dataclass

FIELD_NAMES: tuple[str, ...] = ("number", "name", "month", "year", "cvv")
YEAR_WINDOW = 4  # 当前年份起算共四年：currentYear … currentYear+3


@dataclass
class FieldState:
    """一个字段在某一刻的样子。"""

    value: str
    touched: bool
    valid: bool
    error: str | None


@dataclass
class PaymentSnapshot:
    """整张表单在某一刻的样子；`fields` 按 FIELD_NAMES 的顺序。"""

    fields: dict[str, FieldState]
    canSubmit: bool


class ActionError(ValueError):
    """HTTP 动作体形状不对（对应 400）。"""


@dataclass(frozen=True, slots=True)
class Rule:
    """一个字段的规则：判定函数只看字符串，错误文字固定。"""

    message: str
    accepts: Callable[[str], bool]


@dataclass(slots=True)
class _Entry:
    """内部可变状态：原始输入和是否失焦过。"""

    value: str = ""
    touched: bool = False


def _ascii_digits(length: int) -> Callable[[str], bool]:
    """恰好 `length` 个 ASCII 数字。先查 isascii：isdigit 单独用会放过全角数字、阿拉伯数字和上标。"""

    def accepts(text: str) -> bool:
        return len(text) == length and text.isascii() and text.isdigit()

    return accepts


def _ascii_letters(text: str) -> bool:
    """至少一个字符，全是 ASCII 字母；空格、重音字母、数字都不行。"""
    return text.isascii() and text.isalpha()


def build_rules(current_year: int) -> dict[str, Rule]:
    """五条规则。月份和年份直接写成合法字符串的集合：不调用 int()，也就没有正负号、空白、下划线的歧义。"""
    months = frozenset(f"{m:02d}" for m in range(1, 13))
    years = frozenset(str(y) for y in range(current_year, current_year + YEAR_WINDOW))
    return {
        "number": Rule("Invalid Card Number", _ascii_digits(16)),
        "name": Rule("Invalid Card Name", _ascii_letters),
        "month": Rule("Invalid Month", months.__contains__),
        "year": Rule("Invalid Year", years.__contains__),
        "cvv": Rule("Invalid CVV", _ascii_digits(3)),
    }


class PaymentForm:
    """五个字段的输入状态机：change 改值，blur 标触碰，reset 清空，snapshot 拍照。"""

    def __init__(self, currentYear: int) -> None:
        if type(currentYear) is not int or not 2000 <= currentYear <= 2096:
            raise ValueError("currentYear must be an int in 2000..2096")
        self._year = currentYear
        self._rules = build_rules(currentYear)
        self._entries = {name: _Entry() for name in FIELD_NAMES}

    def _entry(self, field: str) -> _Entry:
        try:
            return self._entries[field]
        except (KeyError, TypeError):
            raise ValueError(f"unknown field: {field!r}") from None

    def change(self, field: str, value: str) -> None:
        """原样保存字符串（不裁剪、不规范化）；不碰触碰标记。"""
        entry = self._entry(field)
        if not isinstance(value, str):
            raise TypeError("value must be a str")
        entry.value = value

    def blur(self, field: str) -> None:
        """标记触碰；重复失焦无副作用。"""
        self._entry(field).touched = True

    def touch_all(self) -> None:
        """点“提交”时的做法：把五个字段都标为已触碰，让每个无效字段同时亮出错误。"""
        for entry in self._entries.values():
            entry.touched = True

    def first_invalid(self) -> str | None:
        """第一个无效字段的名字（按页面顺序），用来在提交失败时把光标送过去；全有效时为 None。"""
        for name in FIELD_NAMES:
            if not self._rules[name].accepts(self._entries[name].value):
                return name
        return None

    def reset(self) -> None:
        """清空所有值和触碰标记，保留年份与规则。"""
        self._entries = {name: _Entry() for name in FIELD_NAMES}

    def snapshot(self) -> PaymentSnapshot:
        """每次现算、现建：返回值与表单、与上一次的快照都不共享可变对象。"""
        fields: dict[str, FieldState] = {}
        for name in FIELD_NAMES:
            entry, rule = self._entries[name], self._rules[name]
            valid = rule.accepts(entry.value)
            shown = entry.touched and not valid
            fields[name] = FieldState(
                value=entry.value,
                touched=entry.touched,
                valid=valid,
                error=rule.message if shown else None,
            )
        ready = all(state.valid and state.touched for state in fields.values())
        return PaymentSnapshot(fields=fields, canSubmit=ready)


# 每种动作需要的键（除 action 之外）；多一个或少一个都算畸形
_ACTION_KEYS: dict[str, tuple[str, ...]] = {
    "reset": (),
    "blur": ("field",),
    "change": ("field", "value"),
}


def apply_action(form: PaymentForm, body: object) -> dict[str, object]:
    """HTTP 边界：校验 JSON 体的形状，执行动作，返回快照的纯字典。校验全部通过之前不碰表单。"""
    if not isinstance(body, dict):
        raise ActionError("body must be an object")
    action = body.get("action")
    if type(action) is not str or action not in _ACTION_KEYS:
        raise ActionError("unknown action")
    wanted = {"action", *_ACTION_KEYS[action]}
    if set(body) != wanted:
        raise ActionError("unexpected or missing keys")
    if any(type(body[key]) is not str for key in wanted):
        raise ActionError("every value must be a string")
    if "field" in wanted and body["field"] not in FIELD_NAMES:
        raise ActionError("unknown field")
    if action == "reset":
        form.reset()
    elif action == "blur":
        form.blur(body["field"])
    else:
        form.change(body["field"], body["value"])
    return dataclasses.asdict(form.snapshot())


if __name__ == "__main__":
    form = PaymentForm(2031)
    steps = [("number", "4000000000000002"), ("name", "Ada"), ("month", "11"), ("year", "2033"), ("cvv", "42")]
    for name, text in steps:
        form.change(name, text)
        form.blur(name)
        snap = form.snapshot()
        print(f"{name:7} {text!r:20} error={snap.fields[name].error!r:24} canSubmit={snap.canSubmit}")
    form.change("cvv", "420")
    print("fixed cvv  ->", form.snapshot().canSubmit)
    form.reset()
    form.touch_all()
    print("after touch_all:", [s.error for s in form.snapshot().fields.values()])
