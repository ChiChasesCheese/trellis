"""ex01 参考答案。先自己写，再对照。"""
from __future__ import annotations

from collections import defaultdict


def select_where(rows: list[dict], min_amount: int) -> list[str]:
    return [r["charge_id"] for r in rows if r["amount"] >= min_amount]


def sum_by_merchant(rows: list[dict]) -> dict[str, int]:
    total: dict[str, int] = defaultdict(int)
    for r in rows:
        total[r["merchant"]] += r["amount"]
    return dict(total)  # 转回普通 dict，方便和 {} 比较


def join_names(rows: list[dict], merchants: list[dict]) -> list[tuple[str, str]]:
    name_of = {m["merchant_id"]: m["name"] for m in merchants}  # 建索引：O(1) 查找
    return [(r["charge_id"], name_of.get(r["merchant"], "UNKNOWN")) for r in rows]


def top_k(rows: list[dict], k: int) -> list[str]:
    ordered = sorted(rows, key=lambda r: (-r["amount"], r["charge_id"]))  # 完整 tie-break
    return [r["charge_id"] for r in ordered[:k]]


def dispute_ratio_over(rows: list[dict], num: int, den: int) -> list[str]:
    total: dict[str, int] = defaultdict(int)
    disputed: dict[str, int] = defaultdict(int)
    for r in rows:
        total[r["merchant"]] += 1
        if r["status"] == "disputed":
            disputed[r["merchant"]] += 1
    # d/t > num/den  ⇔  d*den > num*t （t、den 都是正数，交叉相乘不改变方向）
    return [m for m in sorted(total) if disputed[m] * den > num * total[m]]
