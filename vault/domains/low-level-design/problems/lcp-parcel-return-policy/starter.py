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


_TOKEN = re.compile(r'\s*(?:(?P<str>"(?:[^"\\]|\\.)*")|(?P<num>-?[0-9]+)|(?P<word>true|false)|(?P<punct>[{}:,]))')


def _decode(raw: str) -> str:
    return re.sub(r"\\(.)", lambda m: {"n": "\n", "t": "\t", "r": "\r", "b": "\b", "f": "\f"}.get(m.group(1), m.group(1)), raw[1:-1])


def parse(text: str) -> dict[str, int | bool | str]:
    tokens: list[object] = []
    pos = 0
    while text[pos:].strip():
        match = _TOKEN.match(text, pos)
        if match is None:
            raise InvalidJson
        pos = match.end()
        kind = match.lastgroup
        raw = match.group(kind)
        if kind == "str":
            tokens.append(("v", _decode(raw)))
        elif kind == "num":
            tokens.append(("v", int(raw)))
        elif kind == "word":
            tokens.append(("v", raw == "true"))
        else:
            tokens.append(raw)
    if not tokens or tokens[0] != "{" or tokens[-1] != "}":
        raise InvalidJson
    body = tokens[1:-1]
    result: dict[str, int | bool | str] = {}
    if not body:
        return result
    for i in range(0, len(body), 4):
        chunk = body[i : i + 4]
        if len(chunk) < 3 or chunk[1] != ":" or not isinstance(chunk[0], tuple) or not isinstance(chunk[0][1], str):
            raise InvalidJson
        result[chunk[0][1]] = chunk[2][1]
    return result


@dataclass(frozen=True)
class Decision:
    eligible: bool
    reason: str
    risk: int


_NEEDED = {"rating", "value_cents", "account_age_days", "days_since_purchase", "opened", "final_sale"}


def evaluate(request: dict[str, int | bool | str]) -> Decision:
    if not isinstance(request, dict) or not _NEEDED <= set(request):
        raise InvalidRequest
    rating = request["rating"]
    value = request["value_cents"]
    age = request["account_age_days"]
    days = request["days_since_purchase"]
    if not isinstance(rating, int) or not 1 <= rating <= 5:
        raise InvalidRequest
    if not all(isinstance(x, int) and x >= 0 for x in (value, age, days)):
        raise InvalidRequest
    # 风险：评分、金额、账龄三项相加
    risk = (5 - rating) * 10
    risk += 30 if value > 50_000 else 15 if value > 10_000 else 0
    risk += 25 if age < 30 else 10 if age < 180 else 0
    if request["final_sale"]:
        reason = "final_sale"
    elif days >= 30:
        reason = "window_expired"
    elif request["opened"] and value >= 10_000:
        reason = "opened_high_value"
    elif risk >= 60:
        reason = "high_risk"
    else:
        reason = "eligible"
    return Decision(reason == "eligible", reason, risk)


def process_line(raw: bytes) -> str:
    try:
        result = asdict(evaluate(parse(raw.decode("ascii"))))
    except ValueError as error:
        result = {"error": str(error)}
    return json.dumps(result, separators=(",", ":"))


def run(lines: Iterable[bytes]) -> Iterator[str]:
    for raw in lines:
        if raw.strip():
            yield process_line(raw)
