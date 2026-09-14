"""ex04 · 字符串与解析 —— 你的作答文件。运行：python -m pytest test_ex04.py -q"""
from __future__ import annotations

import csv  # noqa: F401  用得到的话就用，用不到就删
from dataclasses import dataclass


@dataclass
class ChargeRecord:
    kind: str
    id: str
    acct: str
    cents: int


def split_command_and_rest(line: str) -> tuple[str, str]:
    """把一行按第一个逗号拆成 (命令, 剩余部分)，两边都去空白；剩余部分内部的逗号不再切。
    没有逗号时剩余部分是空字符串。
    """
    # TODO
    return ("", "")


def last_resource_id(resource_path: str) -> str:
    """取形如 "acct_9/charges/ch_1" 的路径里最后一段（"ch_1"）；没有 "/" 就返回去空白后的整段。"""
    # TODO
    return ""


def to_cents(amount: str) -> int:
    """金额字符串（如 "12.50"、"-0.05"、"7"）转成整数分，全程不经过 float。"""
    # TODO
    return 0


def fmt_cents(cents: int) -> str:
    """整数分转成两位小数的字符串，如 1250 -> "12.50"，-5 -> "-0.05"，0 -> "0.00"。"""
    # TODO
    return ""


def format_fee_line(merchant: str, fee_rate: float, cents: int, width: int = 12) -> str:
    """拼一行输出：merchant 右对齐到 width 列 + " | fee " + fee_rate（两位小数）+ "% | amount " + 金额。
    金额部分用 fmt_cents（不能用 float 表示分）；fee_rate 是普通浮点数，用 f"{fee_rate:.2f}"。
    """
    # TODO
    return ""


def normalize_merchant_name(raw: str) -> str:
    """压缩内部空白、转小写、去掉尾部句点。"  Alpha   INC. " -> "alpha inc"。"""
    # TODO
    return ""


def parse_accept_language(header: str) -> list[tuple[str, float]]:
    """解析形如 "en-US, fr;q=0.8 , *;q=0.1" 的头，返回 [(tag, q), ...]；
    tag 去空白；缺省 q 或者 q 解析失败都当作 1.0。
    """
    # TODO
    return []


def split_quoted_fields(line: str) -> list[str]:
    """按逗号拆字段，但字段可能被双引号包裹、内部也可能含逗号，
    例如 '"Alpha, Inc.",acct_9,1250' -> ["Alpha, Inc.", "acct_9", "1250"]。
    注意：普通的 line.split(",") 在这种输入上会切错。
    """
    # TODO
    return []


def parse_charge_record(line: str) -> ChargeRecord | None:
    """把一行 "CHARGE, ch_1 ,acct_9, 12.50" 解析成 ChargeRecord。
    空行、或字段数不是 4，都返回 None（解包前先判断长度，不要盲目解包）。
    """
    # TODO
    return None
