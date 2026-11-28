---
tags:
  - lld/lcproject
---

# 退货策略引擎与严格 JSON 解析修复（Return Approval Engine）

**这个项目要做什么。** 只接受扁平 JSON 子集：严格转义、64 位整数不溢出、拒绝重复键；六个必填字段校验、阈值评分、按固定顺序的拒绝规则、坏行不影响后续行。

## 设计要点

退货策略引擎与严格 JSON 解析（ParcelPolicy）参考解：一行一个请求，坏行只影响它自己。

设计五句话：
1. 解析和策略是两层，各有各的错误：语法层只抛 `InvalidJson`，策略层只抛 `InvalidRequest`；两者都是 `ValueError`，
   `str(error)` 恰好是合同里的错误码，所以按合同的写法 `except ValueError as e: str(e)` 也成立。
2. 解析器是一个只前进的读取器（`_Reader`）：一个位置指针、`expect`/`peek`，按"对象 → 键值对 → 值"递归下降；
   整数先用正则匹配出合法形状，再按位数和范围拒绝，绝不静默改成别的值。
3. 请求先被校验成一个冻结的 `ReturnRequest`（六个字段恰好齐全、类型恰好是 `int`/`bool`、范围对），
   之后的风险与拒绝规则只看这个值，不再碰字典，所以"先全部校验再做决定"由类型保证。
4. 拒绝规则是一张有序的表（原因, 条件）；表的顺序就是合同的优先级，第一条命中的赢。
5. `process_line` 是行驱动的核心：解码、解析、评估、序列化，只捕获两种命名错误；一行失败不碰别的行，无状态。

## 考点与卡片

- **支持的 JSON 子集：一个扁平对象，值只有 64 位整数、布尔、ASCII 字符串**：[[lcp-parcel-return-policy-contract-rules]]
- **数组、嵌套对象、null、小数、指数一律拒绝，这是刻意的子集**：[[lcp-parcel-return-policy-contract-rules]]
- **空白只有空格、制表、回车、换行，且只在字符串之外**：[[lcp-parcel-return-policy-contract-rules]]
- **字符串内只收可打印 ASCII 32 到 126，原始控制字符与非 ASCII 拒绝**：[[lcp-parcel-return-policy-contract-rules]]
- **转义只有八种；\u 与别的转义拒绝，转义出来的控制字符可以出现在结果里**：[[lcp-parcel-return-policy-contract-rules]]
- **键必须带引号、冒号、逗号分隔；尾逗号与缺值拒绝**：[[lcp-parcel-return-policy-contract-rules]]
- **重复键按解码后的键判断：a/b 与 a\/b 是同一个键**：[[lcp-parcel-return-policy-contract-rules]]、[[lcp-parcel-return-policy-reflection-overflow-tests]]
- **字典赋值悄悄覆盖重复键：后一个值赢，错误被吞掉**
- **整数语法 -?(0|[1-9][0-9]*)：加号、前导零、-、0x 都拒绝，-0 接受**：[[lcp-parcel-return-policy-contract-rules]]
- **整数必须落在有符号 64 位范围内，两端都含**：[[lcp-parcel-return-policy-contract-rules]]、[[lcp-parcel-return-policy-reflection-overflow-tests]]
- **溢出要拒绝，不能静默变成 0 或被截断**：[[lcp-parcel-return-policy-reflection-overflow-tests]]
- **超长数字要先看位数再调用 int()：否则 Python 会抛出另一种 ValueError**：[[lcp-parcel-return-policy-reflection-overflow-tests]]
- **布尔是布尔，不是整数：true 不能当评分或金额**：[[lcp-parcel-return-policy-contract-rules]]
- **bool 是 int 的子类：用 type(x) is int，不用 isinstance**：[[lcp-parcel-return-policy-contract-rules]]、[[lcp-parcel-return-policy-state-and-invariant]]
- **正则里用 [0-9] 而不是 \d，用 match 的位置而不是 $，免得接受别的文字系统的数字**：[[lcp-parcel-return-policy-reflection-overflow-tests]]
- **对象之后只能是空白：完整消费输入，截断与多余内容都拒绝**：[[lcp-parcel-return-policy-contract-rules]]、[[lcp-parcel-return-policy-reflection-overflow-tests]]
- **所有语法错误都是同一个 ValueError，消息恰好是 invalid_json**：[[lcp-parcel-return-policy-contract-rules]]、[[lcp-parcel-return-policy-state-and-invariant]]
- **请求必须恰好六个字段：缺字段与多字段都是 invalid_request**：[[lcp-parcel-return-policy-contract-rules]]
- **rating 是 1 到 5 的整数；另三个数是非负的 64 位整数**：[[lcp-parcel-return-policy-contract-rules]]
- **六个字段全部校验完才做决定：final_sale 为真时别处的坏字段也要报错**：[[lcp-parcel-return-policy-contract-rules]]、[[lcp-parcel-return-policy-state-and-invariant]]
- **evaluate 单独被调用也要校验，不能假设上游解析器已经把关**：[[lcp-parcel-return-policy-contract-rules]]、[[lcp-parcel-return-policy-state-and-invariant]]
- **风险分 = (5 - 星级) * 10 + 金额分 + 账龄分**：[[lcp-parcel-return-policy-contract-rules]]
- **金额与账龄分的下界都含在本段：10000、50000、30、180 恰好落在边界时归更高档**：[[lcp-parcel-return-policy-contract-rules]]、[[lcp-parcel-return-policy-reflection-overflow-tests]]
- **被拒绝的请求也要返回算出的风险分**：[[lcp-parcel-return-policy-contract-rules]]
- **拒绝规则的顺序：final_sale、窗口、opened_high_value、high_risk，第一条命中的赢**：[[lcp-parcel-return-policy-contract-rules]]、[[lcp-parcel-return-policy-state-and-invariant]]
- **第 30 天仍在退货窗口内：条件是大于 30，不是大于等于**：[[lcp-parcel-return-policy-contract-rules]]、[[lcp-parcel-return-policy-reflection-overflow-tests]]
- **规则顺序写成一张有序表，而不是责任链类：行为相同、只有顺序不同，用数据**：[[lcp-parcel-return-policy-state-and-invariant]]
- **语法错误与策略错误是两层：前者 invalid_json，后者 invalid_request，语法先于策略**：[[lcp-parcel-return-policy-state-and-invariant]]、[[lcp-parcel-return-policy-contract-rules]]
- **驱动按物理行读：一行一个请求，不拼接相邻行；空行是 invalid_json，空输入没有输出**：[[lcp-parcel-return-policy-contract-rules]]
- **坏行只产生一条错误输出，不影响后面的行：try 包住的是一行**：[[lcp-parcel-return-policy-contract-rules]]、[[lcp-parcel-return-policy-state-and-invariant]]
- **非 ASCII 字节在解码时就是 invalid_json；UnicodeDecodeError 也是 ValueError，要单独认出来**：[[lcp-parcel-return-policy-state-and-invariant]]
- **标准输出只写结果行：诊断文字不能出现在 stdout**：[[lcp-parcel-return-policy-contract-rules]]
- **按名字捕获两种命名错误；意外的 ValueError 是缺陷，要冒出去而不是变成错误行**：[[lcp-parcel-return-policy-state-and-invariant]]
- **溢出安全的测试：两端上限、再加一、20 位、五千位；完整消费的测试：每种尾部内容**：[[lcp-parcel-return-policy-reflection-overflow-tests]]
- **用标准库 json 当对拍的参照，加上子集的额外限制，对变异输入逐个比较**：[[lcp-parcel-return-policy-reflection-overflow-tests]]、[[lcp-parcel-return-policy-reflection-library-swap]]
- **换成成熟的 JSON 库：库当作词法与基础解析，子集规则放在它外面的一层**：[[lcp-parcel-return-policy-reflection-library-swap]]
- **json 库不会替你拒绝 \u、非 ASCII、顶层非对象、嵌套值，这些要在库之外检查**：[[lcp-parcel-return-policy-reflection-library-swap]]
- **换库之前先把现有行为冻成特征测试，换完两套实现对拍**：[[lcp-parcel-return-policy-reflection-library-swap]]、[[lcp-parcel-return-policy-reflection-overflow-tests]]
- **给智能体的指令：规则先行、先列代码与规则的差异、一次修一类缺陷、每次一个失败的测试**：[[lcp-parcel-return-policy-contract-rules]]
- **智能体只补测试期望值时容易从被测代码抄答案：期望值要独立写出**：[[lcp-parcel-return-policy-reflection-overflow-tests]]

## 参考解

```python
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
```

## 测试覆盖（46 个）

- `test_contract_example`
- `test_day_thirty_is_inside_the_window_and_day_thirty_one_is_not`
- `test_malformed_object_is_invalid_json`
- `test_empty_object_and_whitespace_variants`
- `test_value_types_and_boolean_stays_boolean`
- `test_integers_accepted_including_both_signed_limits`
- `test_string_escapes_decode_and_controls_may_be_escaped`
- `test_parse_accepts_crlf_inside_its_argument`
- `test_syntax_rejected`
- `test_non_string_argument_is_invalid_json`
- `test_deep_nesting_is_invalid_json_and_never_a_crash`
- `test_unicode_digits_are_not_integers`
- `test_duplicate_decoded_keys_rejected`
- `test_keys_that_differ_only_in_case_or_escape_meaning_are_distinct`
- `test_overflow_is_invalid_json_not_zero_and_not_another_error`
- `test_leading_zero_run_is_not_a_long_valid_number`
- `test_trailing_content_after_a_valid_object_is_rejected`
- `test_trailing_whitespace_is_fine`
- `test_missing_and_extra_fields_are_invalid_request`
- `test_non_dict_request_is_invalid_request`
- `test_integer_fields_refuse_every_other_type_including_bool`
- `test_boolean_fields_refuse_every_other_type`
- `test_rating_range`
- `test_nonnegative_signed_64_bit_range`
- `test_every_field_is_validated_before_any_decision`
- `test_evaluate_does_not_modify_the_request`
- `test_value_points_at_every_boundary`
- `test_age_points_at_every_boundary`
- `test_rating_points`
- `test_reason_order_when_several_rules_apply`
- `test_high_risk_boundary_uses_inputs_that_do_not_move_other_boundaries`
- `test_opened_high_value_boundary`
- `test_risk_is_reported_for_every_rejection`
- `test_whole_grid_against_the_independent_oracle`
- `test_decision_is_a_frozen_value`
- `test_driver_one_output_line_per_input_line_in_order`
- `test_driver_blank_and_whitespace_lines_are_invalid_json_and_do_not_stop_later_lines`
- `test_driver_empty_input_has_no_output`
- `test_driver_non_ascii_bytes_are_invalid_json_and_isolated`
- `test_driver_last_line_without_newline_and_crlf_lines`
- `test_driver_reads_a_binary_stream_line_by_line`
- `test_driver_does_not_join_physical_lines`
- `test_driver_output_lines_are_compact_json_with_stable_key_order`
- `test_driver_syntax_error_wins_over_request_error_and_codes_are_exact`
- `test_driver_every_output_line_is_valid_json_with_only_known_keys`
- `test_parse_agrees_with_a_stricter_standard_library_oracle_on_mutations`

## 自己做一遍

从 `starter.py` 开始写，写完跑测试；参考解在 `solution.py`。

```bash
cd vault/domains/low-level-design/problems/lcp-parcel-return-policy
python3 -m pytest -q
```
