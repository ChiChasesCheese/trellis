"""ex03 · 数据结构 list / dict / set / tuple —— 你的作答文件。运行：python -m pytest test_ex03.py -q"""
from __future__ import annotations

# 实现时大概率用得上：
# from collections import Counter, defaultdict


def dedupe_charge_ids_keep_order(charge_ids: list[str]) -> list[str]:
    """保序去重：重复的 charge_id 只保留第一次出现的那个位置。"""
    # TODO
    return []


def clone_amounts(amounts: list[int]) -> list[int]:
    """返回 amounts 的一份独立拷贝（分为单位的金额列表）。
    调用方后续会在返回值上原地追加/修改，不能影响传进来的原始列表。
    """
    # TODO
    return []


def record_dispute_note(
    charge_id: str,
    note: str,
    notes_by_charge: dict[str, list[str]] | None = None,
) -> dict[str, list[str]]:
    """把 (charge_id, note) 追加进 notes_by_charge[charge_id] 对应的列表里，返回这个 dict。
    不传 notes_by_charge 时，每次调用都必须拿到一个全新的空 dict——
    不能用可变对象当默认参数，否则状态会在两次调用之间泄漏。
    """
    # TODO
    return {}


def group_charges_by_merchant(rows: list[dict]) -> dict[str, list[dict]]:
    """按 row["merchant"] 分组：dict 的 value 是该 merchant 名下的行列表，组内保持 rows 里的原始顺序。"""
    # TODO
    return {}


def invert_status_index(status_by_charge: dict[str, str]) -> dict[str, list[str]]:
    """{charge_id: status} 反转成 {status: [charge_id, ...]}，每个 value 列表按 charge_id 字典序排序。"""
    # TODO
    return {}


def sum_amount_by_merchant_and_country(rows: list[dict]) -> dict[tuple[str, str], int]:
    """按 (row["merchant"], row["country"]) 这个元组做 key，求每组 amount 之和（二维聚合）。"""
    # TODO
    return {}


def rank_disputed_merchants(rows: list[dict], k: int) -> list[str]:
    """统计 status == "disputed" 的行按 merchant 计数，返回次数最多的前 k 个 merchant id。
    次数降序；次数相同时按 merchant id 字典序（升序）——注意 Counter.most_common() 的并列顺序
    是插入顺序，不满足这个要求。
    """
    # TODO
    return []


def filter_charges_for_known_merchants(rows: list[dict], known_merchants: set[str]) -> list[str]:
    """返回 merchant 出现在 known_merchants 里的那些行的 charge_id，保持 rows 的原始顺序。
    known_merchants 是 set 而不是 list：这里要对每一行都做一次成员判断，
    set 的 `in` 是 O(1)，list 的 `in` 是 O(n)。
    """
    # TODO
    return []
