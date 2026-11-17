"""支付表单校验（PaymentForm）练习骨架。公开 API 与 `solution.py` 一致；放进真实工作区时，
把 `FieldState`、`PaymentSnapshot` 换成 `from models import ...`，类 `PaymentForm` 写进 `form.py` 即可运行公开测试。

产品规则（逐条都有测试）：
 1. 表单有五个字段，名字固定：number、name、month、year、cvv。初始时每个字段值为空串、未触碰。
 2. `change(field, value)` 原样保存字符串：不裁剪空白、不改大小写、不补零；每次改值都重新判断有效性；不改变触碰标记。
 3. `blur(field)` 把该字段标为已触碰，之后无论怎么改值都保持已触碰；重复失焦没有副作用。
 4. `reset()` 清空所有字段的值和触碰标记，保留构造时注入的年份。
 5. 各字段的有效值（全部只认 ASCII）：
    number 恰好 16 个数字；name 一个或多个英文字母，不含空格；month 恰好两位数字且在 01 到 12 之间；
    year 恰好四位数字且在 currentYear 到 currentYear+3 之间（含两端）；cvv 恰好 3 个数字。
    空白、换行、正负号、全角或其他文字的数字和字母一律无效；前导零保留；月份与年份互相独立，没有“当前月份”规则。
 6. 错误文字固定：Invalid Card Number、Invalid Card Name、Invalid Month、Invalid Year、Invalid CVV。
 7. `snapshot()` 返回 `PaymentSnapshot`：`fields` 是五个字段名到 `FieldState(value, touched, valid, error)` 的字典；
    `canSubmit` 仅当五个字段全部有效且全部已触碰时为真。`error` 只在“已触碰且无效”时是文字，其余情况为 None。
 8. 快照是独立的：之后再调用任何方法，旧快照不变；改动返回的快照，表单和其他快照不变；两个表单互不影响。
 9. 构造函数要求 currentYear 是 2000 到 2096 的整数（保证窗口末端仍是四位数），否则抛 ValueError；
    未知字段名抛 ValueError，非字符串的值抛 TypeError，失败的调用不改变任何状态。
10. `touch_all()` 把五个字段都标为已触碰（点“提交”时用），不改任何值；之后每个无效字段同时显示自己的错误。
11. `first_invalid()` 按 number、name、month、year、cvv 的顺序返回第一个无效字段的名字，全部有效时返回 None；与触碰无关。
12. `apply_action(form, body)` 是 HTTP 边界：body 必须是字典，`action` 是 "change"、"blur"、"reset" 之一，
    键集合必须恰好是 {action} ∪ {change: field,value；blur: field；reset: 无}，所有取值都是 str，field 是五个名字之一。
    形状不对抛 `ActionError`，并且表单一点不动；成功时返回新快照的纯字典（`dataclasses.asdict`）。
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

FIELD_NAMES: tuple[str, ...] = ("number", "name", "month", "year", "cvv")
YEAR_WINDOW = 4


@dataclass
class FieldState:
    value: str
    touched: bool
    valid: bool
    error: str | None


@dataclass
class PaymentSnapshot:
    fields: dict[str, FieldState]
    canSubmit: bool


class ActionError(ValueError):
    """HTTP 动作体形状不对（对应 400）。"""


@dataclass(frozen=True, slots=True)
class Rule:
    message: str
    accepts: Callable[[str], bool]


def build_rules(current_year: int) -> dict[str, Rule]:
    raise NotImplementedError


class PaymentForm:
    def __init__(self, currentYear: int) -> None:
        raise NotImplementedError

    def change(self, field: str, value: str) -> None:
        raise NotImplementedError

    def blur(self, field: str) -> None:
        raise NotImplementedError

    def touch_all(self) -> None:
        raise NotImplementedError

    def first_invalid(self) -> str | None:
        raise NotImplementedError

    def reset(self) -> None:
        raise NotImplementedError

    def snapshot(self) -> PaymentSnapshot:
        raise NotImplementedError


def apply_action(form: PaymentForm, body: object) -> dict[str, object]:
    raise NotImplementedError
