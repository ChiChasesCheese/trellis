"""ex01 · 从 SQL 到 Python —— 你的作答文件。

每个函数先在纸上写出对应的 SQL，再翻译成 Python。
运行测试：python -m pytest test_ex01.py -q
"""
from __future__ import annotations

from collections import defaultdict

# 每一行 row 是一个 dict，例如
# {"charge_id": "ch_1", "merchant": "m_a", "amount": 1000, "status": "ok"}


def select_where(rows: list[dict], min_amount: int) -> list[str]:
    """SELECT charge_id FROM rows WHERE amount >= min_amount（保持输入顺序）。"""
    return [row["charge_id"] for row in rows if row["amount"] >= min_amount]


def sum_by_merchant(rows: list[dict]) -> dict[str, int]:
    """SELECT merchant, SUM(amount) FROM rows GROUP BY merchant。"""
    by_merchant = defaultdict(int)
    for row in rows:
        merchant, amount = row["merchant"], row["amount"]
        by_merchant[merchant] += amount
    return by_merchant


def join_names(rows: list[dict], merchants: list[dict]) -> list[tuple[str, str]]:
    """SELECT r.charge_id, m.name FROM rows r LEFT JOIN merchants m ON r.merchant = m.merchant_id
    找不到的 name 用 "UNKNOWN"。保持 rows 顺序。"""
    name_of = {m["merchant_id"]: m["name"] for m in merchants}
    return [(r["charge_id"], name_of.get(r["merchant"], "UNKNOWN")) for r in rows]


def top_k(rows: list[dict], k: int) -> list[str]:
    """SELECT charge_id FROM rows ORDER BY amount DESC, charge_id ASC LIMIT k。"""
    ordered = sorted(rows, key=lambda r: (-r["amount"], r["charge_id"]))
    return [r["charge_id"] for r in ordered[:k]]


def dispute_ratio_over(rows: list[dict], num: int, den: int) -> list[str]:
    """争议率（status == "disputed" 的行数 / 总行数）严格大于 num/den 的 merchant，字典序。
    禁止用除法 / 浮点 —— 用交叉相乘。"""
    total = defaultdict[str, int](int)
    disputed = defaultdict[str, int](int)
    for r in rows:
        total[r["merchant"]] += 1
        if r["status"] == "disputed":
            disputed[r["merchant"]] += 1
    return [m for m in sorted(total) if disputed[m] * den > num * total[m]]