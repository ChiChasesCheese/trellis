"""模板 2 · 反复出现的九个模式 —— 每个都可直接跑、直接抄。

这些不是"Python 技巧"，是**从本仓库 92 道题里数出来的高频骨架**。
每个模式下面标了它在哪些题里出现过，以及对应 `skills_matrix.md` 的编号。

自测：`python3 loop/study/00-prereq/templates/patterns.py`
"""
from __future__ import annotations

import bisect
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal


# ================================================================ 1. 分组聚合
# 出现在：q02 q20 ps06 ps13 …  技能：S04
# 最常见的错误：写成"每行应用一次规则"，导致加法类规则被重复计。
# 正确顺序永远是 **先分组，再对组算**。
def group_sum(rows: list[dict], key: str, value: str) -> dict:
    agg: dict = defaultdict(int)
    for r in rows:
        agg[r[key]] += r[value]
    return dict(agg)


def group_multi_key(rows: list[dict], keys: tuple[str, ...], value: str) -> dict:
    """多字段分组用**元组**当 key：可哈希、天然有序、能直接排序输出。"""
    agg: dict = defaultdict(int)
    for r in rows:
        agg[tuple(r[k] for k in keys)] += r[value]
    return dict(agg)


# ================================================================ 2. 确定性排序
# 出现在：几乎全部  技能：S08
# **每一个 sorted 都要能说出完整的 tie-break key。** 说不出 = 输出不稳定 = 隐藏测试随机挂。
def sort_with_tiebreak(rows: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """金额降序，同额按 id 升序。混合升降序用负号（数值）或分两次稳定排序（字符串）。"""
    return sorted(rows, key=lambda t: (-t[1], t[0]))


def sort_mixed_direction(rows: list[tuple[str, str, int]]) -> list[tuple[str, str, int]]:
    """要按"字符串降序 + 数值升序"这种没法用负号的组合：**倒着做两次稳定排序**。

    Python 的 sort 是稳定的，所以先排次要键、再排主要键，结果正确。
    """
    out = sorted(rows, key=lambda t: t[2])                 # 次要键：数值升序
    return sorted(out, key=lambda t: t[1], reverse=True)   # 主要键：字符串降序


# ================================================================ 3. 滑动窗口
# 出现在：q23 ps01 ps13 q41 …  技能：S16 S12
# **窗口边界是闭区间还是开区间，题面不说就问；自己定了就写死在注释里。**
# `[t-w+1, t]` 和 `(t-w, t]` 差一个元素，隐藏测试专打这里。
def sliding_window_counts(events: list[tuple[int, str]], window: int) -> list[tuple[int, str, int]]:
    """events = [(ts, key)]，按 ts 升序。返回每个事件发生时，该 key 在窗口 [ts-window+1, ts] 内的计数。"""
    seen: dict[str, deque] = defaultdict(deque)
    out = []
    for ts, key in events:
        q = seen[key]
        q.append(ts)
        while q and q[0] < ts - window + 1:   # 闭区间：< 而不是 <=
            q.popleft()
        out.append((ts, key, len(q)))
    return out


# ================================================================ 4. 阈值状态翻转
# 出现在：ps13 q41 q01 …  技能：S05 S10
# TRIGGER 和 RESOLVE 的比较**方向相反**，严格/非严格正好翻转——照抄一个方向必错。
# 而且只在**状态翻转的那一刻**发事件，不是每次超阈值都发。
def threshold_events(series: list[tuple[int, int]], threshold: int) -> list[tuple[int, str]]:
    """series = [(ts, value)]。升破 threshold 发 TRIGGER，回落到 threshold 以下发 RESOLVE。"""
    out, firing = [], False
    for ts, value in series:
        if not firing and value >= threshold:     # 升破：>=
            firing = True
            out.append((ts, "TRIGGER"))
        elif firing and value < threshold:        # 回落：<   ← 方向相反
            firing = False
            out.append((ts, "RESOLVE"))
    return out


# ================================================================ 5. 事件流状态机
# 出现在：q10 q13 cd02 …  技能：S10 S03
# 命令流题的通用形状：**dispatch 表 + 每个 handler 只管一件事**，
# 主循环只负责分发。不要写成一坨 if-elif。
@dataclass
class Account:
    balance: int = 0
    history: list = field(default_factory=list)   # 注意：不能写 `= []`，可变默认参数是共享的


class Ledger:
    def __init__(self) -> None:
        self.accounts: dict[str, Account] = defaultdict(Account)

    def apply(self, cmd: str, acct: str, amount: int = 0) -> str | None:
        handler = getattr(self, f"_do_{cmd.lower()}", None)
        if handler is None:
            return f"UNKNOWN {cmd}"        # 未知命令：报错还是忽略？——定死并写清楚
        return handler(acct, amount)

    def _do_deposit(self, acct: str, amount: int) -> None:
        self.accounts[acct].balance += amount

    def _do_withdraw(self, acct: str, amount: int) -> str | None:
        a = self.accounts[acct]
        if a.balance < amount:
            return f"REJECTED {acct}"      # 拒绝的语义：是否记入 history？定死
        a.balance -= amount
        return None


# ================================================================ 6. 并查集
# 出现在：q18 ps09 …  技能：A16
# "谁和谁有关联"类题的标配。20 行以内，背下来。
class DSU:
    def __init__(self) -> None:
        self.parent: dict = {}

    def find(self, x):
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # 路径压缩
            x = self.parent[x]
        return x

    def union(self, a, b) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra

    def groups(self) -> dict:
        out: dict = defaultdict(list)
        for x in self.parent:
            out[self.find(x)].append(x)
        return {k: sorted(v) for k, v in out.items()}


# ================================================================ 7. 有界 BFS
# 出现在：ps09（1 跳 → ≤2 跳 → 全连通）  技能：A16
# part 递进最常见的形状：**限制跳数**和**无限跳**是两个不同的实现，别只写一个。
def bfs_within(adj: dict, start, max_hops: int | None = None) -> set:
    """max_hops=None 表示不限跳数（= 完整连通分量）。返回不含 start 本身。"""
    seen, frontier, hops = {start}, {start}, 0
    while frontier and (max_hops is None or hops < max_hops):
        nxt = {n for x in frontier for n in adj.get(x, ()) if n not in seen}
        seen |= nxt
        frontier = nxt
        hops += 1
    return seen - {start}


# ================================================================ 8. 金额
# 出现在：q03 q13 q20 q21 q22 …  技能：S06
# **永远整数最小单位，或 Decimal 且显式指定舍入。绝不 float 累加。**
def money_to_cents(s: str) -> int:
    """'10.00' → 1000。用 Decimal 中转，不要 int(float(s)*100)——那会漂移。"""
    return int((Decimal(s) * 100).to_integral_value(rounding=ROUND_HALF_UP))


def apply_rate(cents: int, rate_bps: int, fixed_cents: int = 0) -> int:
    """费率用 basis points（万分之一）整数存：290 = 2.9%。避免浮点。

    注意 Python 的 round() 是**银行家舍入**：round(2.5) == 2。要 half-up 得用 Decimal。
    """
    pct = (Decimal(cents) * rate_bps / 10000).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return int(pct) + fixed_cents


def format_money(cents: int) -> str:
    """1000 → '10.00'。整数运算，最后一步才变字符串。"""
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}{cents // 100}.{cents % 100:02d}"


# ================================================================ 9. 区间合并
# 出现在：q04 q29 …  技能：S13 A09
# **闭区间还是开区间**决定了 `<=` 还是 `<`——又是那个 off-by-one。
def merge_intervals(iv: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """闭区间 [a, b]，相邻（b+1 == 下一个 a）也合并。开区间要把 `+ 1` 去掉。"""
    if not iv:
        return []
    out = [list(x) for x in sorted(iv)]
    merged = [out[0]]
    for a, b in out[1:]:
        if a <= merged[-1][1] + 1:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    return [tuple(x) for x in merged]


def first_ge(sorted_vals: list[int], target: int) -> int:
    """有序表里第一个 >= target 的下标。手写二分容易写错边界，**用 bisect**。"""
    return bisect.bisect_left(sorted_vals, target)


# ================================================================ 自测
if __name__ == "__main__":
    assert group_sum([{"m": "a", "v": 1}, {"m": "a", "v": 2}, {"m": "b", "v": 5}], "m", "v") == {"a": 3, "b": 5}
    assert group_multi_key([{"a": 1, "b": 2, "v": 3}], ("a", "b"), "v") == {(1, 2): 3}
    assert sort_with_tiebreak([("b", 50), ("a", 50), ("c", 900)]) == [("c", 900), ("a", 50), ("b", 50)]
    assert sort_mixed_direction([("x", "b", 2), ("y", "b", 1), ("z", "a", 9)])[0][1] == "b"
    # window=3 时 ts=5 的窗口是闭区间 [3, 5]，ts=1 和 ts=2 都在窗外 → 计数是 1 不是 2。
    # （写这份模板时我自己第一遍就把这个断言写成了 2。这个 off-by-one 就是这么发生的。）
    assert sliding_window_counts([(1, "u"), (2, "u"), (5, "u")], 3) == [(1, "u", 1), (2, "u", 2), (5, "u", 1)]
    assert sliding_window_counts([(1, "u"), (2, "u"), (3, "u")], 3) == [(1, "u", 1), (2, "u", 2), (3, "u", 3)]
    assert threshold_events([(1, 1), (2, 5), (3, 6), (4, 1), (5, 9)], 5) == [
        (2, "TRIGGER"), (4, "RESOLVE"), (5, "TRIGGER")]
    led = Ledger()
    led.apply("DEPOSIT", "a", 100)
    assert led.apply("WITHDRAW", "a", 500) == "REJECTED a"
    assert led.accounts["a"].balance == 100
    d = DSU()
    d.union("x", "y")
    d.union("y", "z")
    assert len(d.groups()) == 1
    adj = {1: [2], 2: [1, 3], 3: [2, 4], 4: [3]}
    assert bfs_within(adj, 1, 1) == {2}
    assert bfs_within(adj, 1, 2) == {2, 3}
    assert bfs_within(adj, 1) == {2, 3, 4}
    assert money_to_cents("10.00") == 1000 and money_to_cents("0.005") == 1
    assert apply_rate(1000, 290, 30) == 59        # 2.9% of 1000 = 29, + 30
    assert format_money(-1050) == "-10.50"
    assert merge_intervals([(1, 3), (4, 6), (9, 10)]) == [(1, 6), (9, 10)]
    assert first_ge([1, 3, 5, 7], 4) == 2
    assert Counter("aab").most_common(1) == [("a", 2)]
    print("九个模式全部自测通过")
