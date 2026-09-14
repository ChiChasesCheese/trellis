"""ex03 参考答案。先自己写，再对照。"""
from __future__ import annotations

from collections import Counter, defaultdict


def dedupe_charge_ids_keep_order(charge_ids: list[str]) -> list[str]:
    # dict 的 key 从 3.7 起保持插入顺序，且天然去重：一步到位。
    return list(dict.fromkeys(charge_ids))


def clone_amounts(amounts: list[int]) -> list[int]:
    # amounts[:] / list(amounts) 都行——重点是返回"另一个列表"，
    # 不能写 `return amounts`（那只是同一个对象的另一个名字）。
    return amounts[:]


def record_dispute_note(
    charge_id: str,
    note: str,
    notes_by_charge: dict[str, list[str]] | None = None,
) -> dict[str, list[str]]:
    # 默认参数只在函数定义时求值一次；如果写成 `notes_by_charge: ... = {}`，
    # 所有"没传这个参数"的调用会共享同一个 dict，越攒越多。
    # 用 None 当哨兵，函数体里再决定要不要新建。
    if notes_by_charge is None:
        notes_by_charge = {}
    notes_by_charge.setdefault(charge_id, []).append(note)
    return notes_by_charge


def group_charges_by_merchant(rows: list[dict]) -> dict[str, list[dict]]:
    # 只分桶、不聚合：每个 merchant 对应它名下的行，组内保持原始顺序。
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row["merchant"]].append(row)
    return dict(grouped)


def invert_status_index(status_by_charge: dict[str, str]) -> dict[str, list[str]]:
    # {charge_id: status} 反转成 {status: [charge_id, ...]}。
    # 原 dict 的遍历顺序取决于写入顺序，不是业务含义，所以每组显式 sorted 定序。
    by_status: dict[str, list[str]] = defaultdict(list)
    for charge_id, status in status_by_charge.items():
        by_status[status].append(charge_id)
    return {status: sorted(ids) for status, ids in by_status.items()}


def sum_amount_by_merchant_and_country(rows: list[dict]) -> dict[tuple[str, str], int]:
    # 二维聚合：key 不是单个字段，是 (merchant, country) 这个元组——
    # 元组不可变，能当 dict key；list 不行。
    total: dict[tuple[str, str], int] = defaultdict(int)
    for row in rows:
        total[(row["merchant"], row["country"])] += row["amount"]
    return dict(total)


def rank_disputed_merchants(rows: list[dict], k: int) -> list[str]:
    # 数每个 merchant 有多少笔 disputed。
    disputed_counts = Counter(row["merchant"] for row in rows if row["status"] == "disputed")
    # 陷阱：Counter.most_common() 并列时按"插入顺序"，不是字典序。
    # 要"次数降序、并列字典序升序"，必须自己 sorted(key=元组)。
    ranked = sorted(disputed_counts, key=lambda merchant: (-disputed_counts[merchant], merchant))
    return ranked[:k]


def filter_charges_for_known_merchants(rows: list[dict], known_merchants: set[str]) -> list[str]:
    # known_merchants 必须是 set：这里对每一行都要做一次"在不在"判断，
    # set 是 O(1)，list 是 O(n)——rows 和 known_merchants 都大的时候差距是数量级的。
    return [row["charge_id"] for row in rows if row["merchant"] in known_merchants]
