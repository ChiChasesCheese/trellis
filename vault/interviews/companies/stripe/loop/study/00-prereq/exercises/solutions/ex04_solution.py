"""ex04 参考答案。先自己写，再对照。"""
from __future__ import annotations

import csv
from dataclasses import dataclass


@dataclass
class ChargeRecord:
    kind: str
    id: str
    acct: str
    cents: int


def split_command_and_rest(line: str) -> tuple[str, str]:
    # split(",", 1) 只切第一刀：第一段是命令，后面不管有多少个逗号都留在第二段里。
    parts = line.strip().split(",", 1)
    head = parts[0].strip()
    rest = parts[1].strip() if len(parts) > 1 else ""
    return head, rest


def last_resource_id(resource_path: str) -> str:
    # rsplit("/", 1) 从右边切一刀，取最后一段——不用管前面到底嵌套了几层。
    return resource_path.strip().rsplit("/", 1)[-1]


def to_cents(amount: str) -> int:
    """金额字符串（如 "12.50"）转成整数分。全程只做整数运算，不经过 float。"""
    s = amount.strip()
    neg = s.startswith("-")
    s = s.lstrip("-")
    whole, _, frac = s.partition(".")  # 没有 "." 也不会报错，frac 就是空字符串
    frac = (frac + "00")[:2]  # "5" -> "50"；"" -> "00"；"999" -> 截断成 "99"
    cents = int(whole) * 100 + int(frac)
    return -cents if neg else cents


def fmt_cents(cents: int) -> str:
    """整数分转成 "12.50" 这样的两位小数字符串。"""
    sign = "-" if cents < 0 else ""
    c = abs(cents)
    return f"{sign}{c // 100}.{c % 100:02d}"


def format_fee_line(merchant: str, fee_rate: float, cents: int, width: int = 12) -> str:
    """拼一行对账输出：merchant 右对齐到 width 列，fee_rate 是普通浮点数用 :.2f，
    cents 是金额分——绝不经过 float，走 fmt_cents。输出要跟样例逐字符对齐。
    """
    return f"{merchant:>{width}} | fee {fee_rate:.2f}% | amount {fmt_cents(cents)}"


def normalize_merchant_name(raw: str) -> str:
    """压缩内部空白（含 tab/换行）、转小写、去掉尾部句点。用于比较，不用于展示。"""
    collapsed = " ".join(raw.split())  # split() 不带参数：按任意空白切且自动丢空串
    return collapsed.lower().rstrip(".")


def parse_accept_language(header: str) -> list[tuple[str, float]]:
    """解析形如 "en-US, fr;q=0.8 , *;q=0.1" 的头：tag 去空白，q 缺省或解析失败都当 1.0。"""
    result: list[tuple[str, float]] = []
    for raw_entry in header.split(","):
        entry = raw_entry.strip()
        if not entry:
            continue
        tag, *params = [p.strip() for p in entry.split(";")]
        q = 1.0
        for p in params:
            if p.startswith("q="):
                try:
                    q = float(p[2:])
                except ValueError:
                    q = 1.0
        result.append((tag, q))
    return result


def split_quoted_fields(line: str) -> list[str]:
    """按逗号拆字段，但字段可能被双引号包裹（内部可能含逗号），例如：
    '"Alpha, Inc.",acct_9,1250' -> ["Alpha, Inc.", "acct_9", "1250"]。
    plain line.split(",") 在这种输入上会切错（切出 4 段而不是 3 段），
    所以这里借标准库 csv 模块按 CSV 规则解析这一行。
    """
    fields = next(csv.reader([line.strip()]))
    return [f.strip() for f in fields]


def parse_charge_record(line: str) -> ChargeRecord | None:
    """把一行 "CHARGE, ch_1 ,acct_9, 12.50" 解析成 ChargeRecord。
    空行、或字段数不是 4，都返回 None（不要盲目解包，解包前先判长度）。
    """
    line = line.strip()
    if not line:
        return None
    parts = [p.strip() for p in line.split(",")]
    if len(parts) != 4:
        return None
    kind, cid, acct, amount = parts
    return ChargeRecord(kind=kind, id=cid, acct=acct, cents=to_cents(amount))
