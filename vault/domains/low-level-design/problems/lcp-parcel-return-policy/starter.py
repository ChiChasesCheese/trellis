"""ParcelPolicy 退货策略引擎与 JSON 解析（待修复）。公开 API 与 `solution.py` 一致：`parse`、`evaluate`、`Decision`，
另有命令行驱动的核心 `process_line` / `run`。放进真实工作区时，`parse` 去 `json_parser.py`，`evaluate` 去 `policy.py`。

这份代码能跑，也过得了最简单的例子，但和下面的规则有好几处不符：它就是要你修的东西。

产品规则（逐条都有测试）：
 1. 输入是一个扁平 JSON 对象：键是 ASCII 字符串，值是有符号 64 位整数、布尔或 ASCII 字符串；不接受数组、嵌套对象、
    `null`、小数、指数。空白只有空格、制表、回车、换行，且只在字符串之外。
 2. 字符串里只有可打印 ASCII 32..126，除去双引号和反斜杠；转义只有 `\\"` `\\\\` `\\/` `\\b` `\\f` `\\n` `\\r` `\\t`；
    `\\u`、别的转义、原始控制字符、非 ASCII 都不行；转义出来的控制字符在解码结果里是允许的。
 3. 对象可以为空；键必须带引号、冒号、逗号分隔、没有尾逗号；解码之后的键重复就拒绝；输入被截断、对象之后还有
    非空白内容都拒绝。
 4. 整数形如 `-?(0|[1-9][0-9]*)`，必须落在有符号 64 位范围内（两端都含，`-0` 也行）；前导 `+`、前导零、溢出都拒绝；
    布尔不是整数。所有语法错误都抛 `ValueError("invalid_json")`。
 5. 请求恰好六个字段：`rating`（整数 1..5）、`value_cents`、`account_age_days`、`days_since_purchase`
    （非负的 64 位整数）、`opened`、`final_sale`（布尔）。缺字段、多字段、类型不对（`True` 不是整数）、范围不对，
    一律 `ValueError("invalid_request")`；六个字段全部验完才做决定；直接调用 `evaluate` 也要校验。
 6. 风险 = (5 - rating) * 10 + 金额分（< 10000 分得 0；10000..49999 得 15；≥ 50000 得 30）
    + 账龄分（< 30 天得 25；30..179 得 10；≥ 180 得 0）。被拒绝的请求也返回算出的风险。
 7. 拒绝规则按序：`final_sale` → "final_sale"；`days_since_purchase > 30` → "window_expired"（第 30 天仍在窗口内）；
    已打开且 `value_cents >= 10000` → "opened_high_value"；风险 ≥ 60 → "high_risk"；都不是则 eligible=True、
    reason="eligible"。拒绝的 eligible 一律是 False。
 8. 驱动：每个物理行一个请求，输出一行 `{eligible, reason, risk}` 或 `{error: ...}`（紧凑 JSON）；空行是
    `invalid_json`；非 ASCII 字节是 `invalid_json`；空输入没有输出；坏行不影响后面的行；不往标准输出写别的。

Python 3.11，标准库。
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterable, Iterator
from dataclasses import asdict, dataclass


class InvalidJson(ValueError):
    def __init__(self) -> None:
        super().__init__("invalid_json")


class InvalidRequest(ValueError):
    def __init__(self) -> None:
        super().__init__("invalid_request")


_INT_MAX = 2**63 - 1
_ESCAPES = {'"': '"', "\\": "\\", "/": "/", "b": "\b", "f": "\f", "n": "\n", "r": "\r", "t": "\t"}
# 词法已经做对：空白只有四种；字符串只收 32..126 里除引号、反斜杠之外的字符加八种转义；整数形状严格
_TOKEN = re.compile(
    r'[ \t\r\n]*(?:(?P<str>"(?:[ !#-\[\]-~]|\\["\\/bfnrt])*")|(?P<num>-?(?:0|[1-9][0-9]*))|(?P<word>true|false)|(?P<punct>[{}:,]))'
)


def _tokens(text: str) -> list[object]:
    found: list[object] = []
    pos = 0
    while (match := _TOKEN.match(text, pos)) is not None:
        pos = match.end()
        kind, raw = match.lastgroup, match.group(match.lastgroup)
        if kind == "str":
            found.append(("v", re.sub(r"\\(.)", lambda m: _ESCAPES[m.group(1)], raw[1:-1])))
        elif kind == "num":
            # 缺陷：超出 64 位的整数悄悄变成 0，而不是 invalid_json
            number = int(raw) if len(raw.lstrip("-")) <= 19 else 0
            found.append(("v", number if -(2**63) <= number <= _INT_MAX else 0))
        elif kind == "word":
            found.append(("v", raw == "true"))
        else:
            found.append(raw)
    if text[pos:].strip(" \t\r\n"):
        raise InvalidJson
    return found


def parse(text: str) -> dict[str, int | bool | str]:
    if type(text) is not str:
        raise InvalidJson
    toks = _tokens(text)
    if toks[:1] != ["{"]:
        raise InvalidJson
    members: dict[str, int | bool | str] = {}
    at = 1
    if toks[1:2] == ["}"]:
        at = 2
    else:
        while True:
            key, colon, value = (toks[at : at + 3] + [None, None, None])[:3]
            if not (isinstance(key, tuple) and isinstance(key[1], str) and colon == ":" and isinstance(value, tuple)):
                raise InvalidJson
            # 缺陷：重复键没有检查，后一个悄悄覆盖前一个（按解码后的键）
            members[key[1]] = value[1]
            at += 3
            if toks[at : at + 1] == [","]:
                at += 1
            elif toks[at : at + 1] == ["}"]:
                at += 1
                break
            else:
                raise InvalidJson
    if at != len(toks):
        raise InvalidJson
    return members


@dataclass(frozen=True)
class Decision:
    eligible: bool
    reason: str
    risk: int


_NEEDED = {"rating", "value_cents", "account_age_days", "days_since_purchase", "opened", "final_sale"}


def _is_count(x: object) -> bool:
    return type(x) is int and 0 <= x <= _INT_MAX


def evaluate(request: dict[str, int | bool | str]) -> Decision:
    # 缺陷：只检查"六个字段都在"，多出来的字段也放行
    if type(request) is not dict or not _NEEDED <= set(request):
        raise InvalidRequest
    rating, value, age, days = (request[k] for k in ("rating", "value_cents", "account_age_days", "days_since_purchase"))
    opened, final_sale = request["opened"], request["final_sale"]
    # 校验已经做对：六个字段全部验完才做决定；`type(x) is int` 挡住布尔
    if not (type(rating) is int and 1 <= rating <= 5):
        raise InvalidRequest
    if not (_is_count(value) and _is_count(age) and _is_count(days)):
        raise InvalidRequest
    if type(opened) is not bool or type(final_sale) is not bool:
        raise InvalidRequest
    risk = (5 - rating) * 10
    # 缺陷：两个金额阈值都漏了"下界含"，恰好 50000 与 10000 少一档
    risk += 30 if value > 50_000 else 15 if value > 10_000 else 0
    risk += 25 if age < 30 else 10 if age < 180 else 0
    if final_sale:
        reason = "final_sale"
    # 缺陷：第 30 天也算过期，窗口应该是 days > 30
    elif days >= 30:
        reason = "window_expired"
    elif opened and value >= 10_000:
        reason = "opened_high_value"
    elif risk >= 60:
        reason = "high_risk"
    else:
        reason = "eligible"
    return Decision(reason == "eligible", reason, risk)


def process_line(raw: bytes) -> str:
    try:
        result: dict[str, object] = asdict(evaluate(parse(raw.decode("ascii"))))
    except UnicodeDecodeError:  # 驱动已经做对：非 ASCII 字节就是 invalid_json，不泄漏解码提示
        result = {"error": "invalid_json"}
    except (InvalidJson, InvalidRequest) as error:
        result = {"error": str(error)}
    return json.dumps(result, separators=(",", ":"))


def run(lines: Iterable[bytes]) -> Iterator[str]:
    # 驱动已经做对：每个物理行一个结果，空行是 invalid_json，不跳过
    for raw in lines:
        yield process_line(raw)
