"""退货策略引擎与严格 JSON 解析（ParcelPolicy）参考解：一行一个请求，坏行只影响它自己。

设计五句话：
1. 解析和策略是两层，各有各的错误：语法层只抛 `InvalidJson`，策略层只抛 `InvalidRequest`；两者都是 `ValueError`，
   `str(error)` 恰好是合同里的错误码，所以按合同的写法 `except ValueError as e: str(e)` 也成立。
2. 解析器是一个只前进的读取器（`_Reader`）：一个位置指针、`expect`/`peek`，按"对象 → 键值对 → 值"递归下降；
   整数先用正则匹配出合法形状，再按位数和范围拒绝，绝不静默改成别的值。
3. 请求先被校验成一个冻结的 `ReturnRequest`（六个字段恰好齐全、类型恰好是 `int`/`bool`、范围对），
   之后的风险与拒绝规则只看这个值，不再碰字典，所以"先全部校验再做决定"由类型保证。
4. 拒绝规则是一张有序的表（原因, 条件）；表的顺序就是合同的优先级，第一条命中的赢。
5. `process_line` 是行驱动的核心：解码、解析、评估、序列化，只捕获两种命名错误；一行失败不碰别的行，无状态。
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable, Iterable, Iterator
from dataclasses import asdict, dataclass

INT64_MIN, INT64_MAX = -(2**63), 2**63 - 1
# 只认 ASCII 数字：不用 \d（它会匹配别的文字系统里的数字），也不用 $（它会在末尾换行前匹配）
_INTEGER = re.compile(r"-?(?:0|[1-9][0-9]*)")
_ESCAPES = {'"': '"', "\\": "\\", "/": "/", "b": "\b", "f": "\f", "n": "\n", "r": "\r", "t": "\t"}
_WHITESPACE = " \t\r\n"
_LITERALS = (("true", True), ("false", False))


class InvalidJson(ValueError):
    """语法层的错误：输入不是受支持的 JSON 子集。消息固定为 `invalid_json`。"""

    def __init__(self) -> None:
        super().__init__("invalid_json")


class InvalidRequest(ValueError):
    """策略层的错误：语法对，但字段不齐、类型不对或范围不对。消息固定为 `invalid_request`。"""

    def __init__(self) -> None:
        super().__init__("invalid_request")


class _Reader:
    """只前进的读取器：`pos` 是下一个要读的字符；每个方法读完一个语法单元，读不下去就抛 `InvalidJson`。"""

    def __init__(self, text: str) -> None:
        self.text, self.pos = text, 0

    def skip_whitespace(self) -> None:
        while self.pos < len(self.text) and self.text[self.pos] in _WHITESPACE:
            self.pos += 1

    def peek(self) -> str:
        """下一个字符（先跳过空白）；输入读完了就是空串，空串不等于任何记号。"""
        self.skip_whitespace()
        return self.text[self.pos] if self.pos < len(self.text) else ""

    def accept(self, token: str) -> bool:
        if self.peek() == token:
            self.pos += 1
            return True
        return False

    def expect(self, token: str) -> None:
        if not self.accept(token):
            raise InvalidJson

    def string(self) -> str:
        self.expect('"')
        out: list[str] = []
        while self.pos < len(self.text):  # 字符串里不跳空白：空格是内容
            ch = self.text[self.pos]
            self.pos += 1
            if ch == '"':
                return "".join(out)
            if ch == "\\":
                escape = self.text[self.pos : self.pos + 1]
                if escape not in _ESCAPES:  # 包括 \u 和输入在反斜杠处结束
                    raise InvalidJson
                out.append(_ESCAPES[escape])
                self.pos += 1
            elif 32 <= ord(ch) <= 126:
                out.append(ch)
            else:  # 原始控制字符、DEL、非 ASCII
                raise InvalidJson
        raise InvalidJson  # 没有收尾的引号

    def integer(self) -> int:
        self.skip_whitespace()
        match = _INTEGER.match(self.text, self.pos)
        if match is None:
            raise InvalidJson
        digits = match.group()
        # 合法形状没有前导零，所以超过 19 位的一定溢出；先拒绝，免得 int() 为超长数字抛出别的 ValueError
        if len(digits.lstrip("-")) > 19 or not INT64_MIN <= int(digits) <= INT64_MAX:
            raise InvalidJson
        self.pos = match.end()
        return int(digits)

    def value(self) -> int | bool | str:
        ch = self.peek()
        if ch == '"':
            return self.string()
        for word, decoded in _LITERALS:
            if self.text.startswith(word, self.pos):
                self.pos += len(word)
                return decoded
        return self.integer()  # 数组、对象、null、小数点、指数都会在这里或之后失败

    def obj(self) -> dict[str, int | bool | str]:
        result: dict[str, int | bool | str] = {}
        self.expect("{")
        if not self.accept("}"):
            while True:
                key = self.string()
                if key in result:  # 按解码后的键判重："a/b" 与 "a\/b" 是同一个键
                    raise InvalidJson
                self.expect(":")
                result[key] = self.value()
                if not self.accept(","):
                    break
            self.expect("}")
        return result


def parse(text: str) -> dict[str, int | bool | str]:
    """把一个扁平 JSON 对象解析成字典；任何不符合子集的输入都抛 `InvalidJson`。"""
    if type(text) is not str:
        raise InvalidJson
    reader = _Reader(text)
    result = reader.obj()
    if reader.peek() != "":  # 对象之后只能是空白
        raise InvalidJson
    return result


@dataclass(frozen=True)
class Decision:
    eligible: bool
    reason: str
    risk: int


FIELDS = frozenset({"rating", "value_cents", "account_age_days", "days_since_purchase", "opened", "final_sale"})


def _is_count(x: object) -> bool:
    """非负的 64 位整数。`bool` 是 `int` 的子类，所以比较类型本身而不是 isinstance。"""
    return type(x) is int and 0 <= x <= INT64_MAX


@dataclass(frozen=True)
class ReturnRequest:
    """校验之后的请求：能构造出来，就说明六个字段齐全、类型与范围都对。"""

    rating: int
    value_cents: int
    account_age_days: int
    days_since_purchase: int
    opened: bool
    final_sale: bool

    @classmethod
    def from_mapping(cls, request: object) -> ReturnRequest:
        """六个字段先全部验完，再构造；任何一处不对都是同一个 `InvalidRequest`。"""
        if not isinstance(request, dict) or request.keys() != FIELDS:
            raise InvalidRequest
        rating = request["rating"]
        if not (
            type(rating) is int
            and 1 <= rating <= 5
            and all(_is_count(request[k]) for k in ("value_cents", "account_age_days", "days_since_purchase"))
            and type(request["opened"]) is bool
            and type(request["final_sale"]) is bool
        ):
            raise InvalidRequest
        return cls(**request)

    @property
    def risk(self) -> int:
        """风险分：星级、金额、账龄三项之和；每个下界都含在本段内。"""
        value = 30 if self.value_cents >= 50_000 else 15 if self.value_cents >= 10_000 else 0
        age = 25 if self.account_age_days < 30 else 10 if self.account_age_days < 180 else 0
        return (5 - self.rating) * 10 + value + age


# 拒绝规则：顺序就是优先级，第一条命中的赢；第二项收的是请求和已算好的风险分
_REJECTIONS: tuple[tuple[str, Callable[[ReturnRequest, int], bool]], ...] = (
    ("final_sale", lambda r, risk: r.final_sale),
    ("window_expired", lambda r, risk: r.days_since_purchase > 30),  # 第 30 天仍在窗口内
    ("opened_high_value", lambda r, risk: r.opened and r.value_cents >= 10_000),
    ("high_risk", lambda r, risk: risk >= 60),
)


def evaluate(request: dict[str, int | bool | str]) -> Decision:
    """校验、算风险、按序检查拒绝规则。风险分对被拒绝的请求同样返回。"""
    parsed = ReturnRequest.from_mapping(request)
    risk = parsed.risk
    reason = next((name for name, hit in _REJECTIONS if hit(parsed, risk)), "eligible")
    return Decision(reason == "eligible", reason, risk)


def process_line(raw: bytes) -> str:
    """一个物理行 → 一行输出（不含换行）。只捕获两种命名错误，别的异常是缺陷，要冒出去。"""
    try:
        result: dict[str, object] = asdict(evaluate(parse(raw.decode("ascii"))))
    except UnicodeDecodeError:  # 非 ASCII 字节；它也是 ValueError，必须在别的处理之前认出来
        result = {"error": "invalid_json"}
    except (InvalidJson, InvalidRequest) as error:
        result = {"error": str(error)}
    return json.dumps(result, separators=(",", ":"))


def run(lines: Iterable[bytes]) -> Iterator[str]:
    """一行一结果，空输入没有结果；行与行之间没有任何共享状态。"""
    for raw in lines:
        yield process_line(raw)


if __name__ == "__main__":
    sample = b'{"rating":4,"value_cents":10000,"account_age_days":29,"days_since_purchase":30,"opened":false,"final_sale":false}\n'
    for out in run([sample, b"\n", b'{"rating":true}\n']):
        print(out)
