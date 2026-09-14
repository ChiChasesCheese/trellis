# pc12 · Top Two Users by Total Purchase Amount：练的是"金额绝不能过浮点数"

> [!tldr]
> - fastprep.io 一手 Easy 电面题（2026-06 报告）；**Part 2（按天分组）、Part 3（流式 + 退款）均为 (reconstructed)**
> - 这题考的是：按用户求和取 top two，核心陷阱是金额必须转成整数分，不能用 `float` 累加
> - 三步套路：字符串切分金额成整数分 → 哈希表按用户累加、`(-total, user)` 排序取前二 → 叠加分组/流式两个追问，计数逻辑不变
> - 最值得带走的一个模式：**涉及金额的题永远先把字符串转成整数最小单位（分），全程不经过 `float`——浮点数不能精确表示大多数十进制小数，累加误差会在数据量大时真的改变排名**

## 1. 题目在说什么（人话版）

给一批 `"user,amount"` 记录，按用户累加购买金额，返回总额最高的两个用户。

```
records = ["alice,10.00", "bob,25.50", "alice,5.00", "carol,25.50"]
# alice=15.00, bob=25.50, carol=25.50 -> bob 和 carol 打平，按用户名升序 bob < carol
-> [("bob", 2550), ("carol", 2550)]
```

## 2. 读题：把文字变成模型

- **实体**：用户、购买记录（金额字符串）。
- **输出**：`(user, cents)` 列表，总额降序、金额相同按用户名升序，长度最多 2。
- **状态**：一个 `{user: 累计分数}` 的哈希表。
- **一句话建模**：这是一个 **按 key 分组求和 + 确定性排序取 top-k** 问题，关键是金额的整数化处理。

> [!note] 为什么必须转成整数分
> 浮点数无法精确表示大多数十进制小数（`0.1 + 0.2 != 0.3`）。金额格式固定是"整数.两位
> 小数"，直接按小数点位置切分成"整数部分"和"两位小数部分"转成整数（`"12.34"` →
> `1234`），全程不经过 `float`，就不会有累加误差；输出也是分，不是重新拼出来的美元字符串。

## 3. 下笔顺序（面试里就按这个顺序敲）

1. **先写金额解析**：按小数点切分成整数部分和两位小数，拼成整数分；格式不对（缺小数点、位数不对）直接 `ValueError`。
2. **Part 1 最小可用**：哈希表按用户累加分数，`(-total, user)` 排序取前二。
3. **Part 2 叠加**：外层再按日期分组，组内复用 Part 1 的求和/排序逻辑，取 top-k 而不是固定 top two。
4. **Part 3 叠加**：把"一次性读入所有记录"换成"事件流顺序处理"，金额允许为负（退款），`QUERY` 事件在当前时间点拍一次快照。

## 4. 代码怎么组织

```
_parse_cents(amount, *, allow_negative) -> int   # 唯一的金额解析入口
_ranked(totals) -> list[(user, cents)]           # (-total, user) 排序
top_two_users(records)                            # Part 1
top_k_per_day(records, k)                         # Part 2：按天分组后复用 _ranked
process_stream(events)                            # Part 3：流式累加 + QUERY 快照
part1 / part2 / part3
```
`_parse_cents` 和 `_ranked` 被三个 part 共享；Part 1/2 禁止负数金额（`allow_negative=False`），
Part 3 允许（退款），这是唯一的参数化差异。

## 5. 核心代码骨架

```python
import re
_AMOUNT_RE = re.compile(r"\d+\.\d{2}")

def _parse_cents(amount, *, allow_negative):
    s = amount.strip()
    sign = 1
    if s.startswith("-"):
        if not allow_negative:
            raise ValueError("amount must be non-negative")
        sign, s = -1, s[1:]
    if not _AMOUNT_RE.fullmatch(s):
        raise ValueError(f"amount must look like '12.34': {amount!r}")
    whole, frac = s.split(".")
    return sign * (int(whole) * 100 + int(frac))

def _ranked(totals):
    return sorted(totals.items(), key=lambda p: (-p[1], p[0]))

def top_two_users(records):
    totals = {}
    for rec in records:
        user, amount = rec.split(",")
        totals[user] = totals.get(user, 0) + _parse_cents(amount, allow_negative=False)
    return _ranked(totals)[:2]

def process_stream(events):
    # Part 3：顺序处理，QUERY 拍快照，退款可以把总额打成负数但仍参与排名
    totals, snapshots = {}, []
    for ev in events:
        if ev.strip() == "QUERY":
            snapshots.append(_ranked(totals)[:2])
            continue
        user, amount = ev.split(",")
        totals[user] = totals.get(user, 0) + _parse_cents(amount, allow_negative=True)
    return snapshots
```

## 6. 面试里怎么说（边写边讲）

- 开始前：「金额是两位小数的字符串，我会直接按字符串位置切成整数分处理，不经过 `float`，避免浮点累加误差。」
- 写 Part 1 时：「打平按用户名升序，用哈希表 O(1) 累加、排序取前二是 O(n log n)。」
- 引出 Part 3 时：「流式处理里退款是负数更新，用户总额可以变负但仍留在候选池里，`QUERY` 只是对当前哈希表排序拍个快照。」

## 7. 常见跑偏（方法层面，3 条）

- 用 `float(amount) * 100` 转分，大量累加后出现误差，排名在边界情况下算错。
- Part 1/2 忘了拒绝负数金额（这两个 part 没有退款语义），或者 Part 3 忘了允许负数。
- Part 3 每次 `QUERY` 都重新拼一次全量排序没问题，但如果直接维护"只保留 top 2"的增量结构却漏掉了退款后名次可能重新洗牌的情况。

## 8. 同族题 / 延伸

- 同一类"分组求和 + 确定性排序 tie-break"：`pc11`（字符计数排序）、`pc03`（滑窗事件流）。
- 练习命令：`python3 loop/mock.py start pc12`
