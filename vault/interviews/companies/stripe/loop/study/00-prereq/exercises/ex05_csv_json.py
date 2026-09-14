"""ex05 · CSV 与 JSON —— 你的作答文件。运行：python -m pytest test_ex05.py -q"""
from __future__ import annotations

from typing import Any

# 你会用到：csv, io, json, decimal.Decimal（金额别用 float），collections.defaultdict

# 哨兵：区分"key 不存在"和"值就是 None"。d.get(k, _MISSING) is _MISSING 才叫"不存在"。
_MISSING = object()


def read_csv_text(text: str) -> list[dict]:
    """把 CSV 字符串（不是文件！用 io.StringIO 包一层）解析成 dict 列表：
    用 csv.DictReader 按列名取值（列顺序无所谓、允许多余列）；key/value 两侧空白去掉；
    amount 转成 int；缺 id 或 amount 解析失败的行直接跳过（脏数据不该让整批解析失败）。"""
    # TODO
    return [{"_todo": True}]


def write_csv_rows(rows: list[dict], fieldnames: list[str]) -> str:
    """用 csv.DictWriter 把 rows 写成 CSV 字符串：带表头，行尾用 "\\n"（不是 csv 默认的 "\\r\\n"）。"""
    # TODO
    return ""


def clean_numeric_rows(rows: list[dict], field: str) -> tuple[list[dict], list[dict]]:
    """把 rows 按 `field` 能不能解析成 int 分成 (ok, bad) 两组。
    设计决定：不抛异常——脏行被收进 bad 里让调用方自己决定要不要报错/记日志，
    ok 里的行会返回一份新 dict，`field` 已经替换成 int。"""
    # TODO
    return [{"_todo": True}], [{"_todo": True}]


def parse_events_jsonl(text: str) -> list[dict]:
    """JSONL：一行一个 JSON 对象。跳过空行；某一行不是合法 JSON 就跳过那一行（不抛异常）。"""
    # TODO
    return [{"_todo": True}]


def dig(obj: Any, *path: Any, default: Any = None) -> Any:
    """安全地深挖嵌套结构：obj["charges"]["data"][0]["amount"] 这种，但任何一层都可能
    缺失、是 None，或者类型对不上（比如你以为是 list 结果是 dict）。挖不下去就返回 default。"""
    # TODO
    return "_todo_"


def field_status(d: dict, key: str) -> str:
    """区分三种情况，返回 "missing" / "null" / "present"：
    key 不在 d 里 → "missing"；d[key] is None → "null"；否则 → "present"。
    用哨兵 _MISSING，不要用 d.get(key) is None（那样"不存在"和"值是 None"分不清）。"""
    # TODO
    return "_todo_"


def sum_amounts_decimal(values: list) -> str:
    """把 values（可能混着 int/float/str）当金额精确求和，返回字符串。
    用 Decimal(str(v)) 而不是直接 Decimal(v) 或者用 float 累加——
    float(0.1) + float(0.2) 不等于 0.3，金额场景这种漂移不可接受。"""
    # TODO
    return "_todo_"


def summarize_list_response(body: dict) -> tuple[int, str | None]:
    """Stripe 风格的列表响应 {"object":"list","data":[...],"has_more":...}：
    返回 (data 里 amount 的总和, 最后一个元素的 id 或 None)。
    body 里有 "error" key 时视为失败响应，直接返回 (0, None)。"""
    # TODO
    return (-1, "_todo_")


def csv_to_grouped_report(text: str, key_field: str, amount_field: str) -> str:
    """完整小流水线：CSV 字符串 → 记录列表 → 按 key_field 聚合 amount_field（Decimal 精确求和）
    → 输出稳定的 JSON 字符串（sort_keys=True），形如 {"m_a": "150", "m_b": "70"}。
    聚合金额解析失败的行跳过；key_field 为空的行也跳过。"""
    # TODO
    return "{}"
