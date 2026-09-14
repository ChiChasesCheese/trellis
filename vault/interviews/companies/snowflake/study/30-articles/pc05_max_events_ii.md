# pc05 · Max Events II：练的是"闭区间 + 二分找下一个 + 被追问方案时不重写"

> [!tldr]
> - Part 1 是 2026-06 一手电面原题 LC 1751；**Part 2 输出方案、Part 3 去掉 k 限制放大到 10⁵ 是 (reconstructed)**
> - 这题考的是：至多 k 个互不重叠（闭区间）活动的最大价值
> - 三步套路：按开始时间排序 → `nxt[i] = bisect_right(starts, end_i)` → `dp[j][i] = max(跳过, 取 + dp[j−1][nxt[i]])`
> - 最值得带走的一个模式：**闭区间用 `bisect_right`，半开区间用 `bisect_left`**——这一个字母就是 off-by-one

## 1. 题目在说什么（人话版)

一堆活动，每个有开始日、结束日（包含当天）、价值。同一天只能参加一个，参加就得从头待到尾。最多参加 k 个，价值总和最大多少？追问：具体参加哪些？不限个数、10 万个活动时怎么做？

小例子：
```
[1,2,4] [3,4,3] [2,3,1], k=2 → 7（第一和第二个；第三个和两个都冲突）
```

## 2. 读题：把文字变成模型

- **实体**：活动 `[start, end, value]`、选择数上限 k。
- **冲突规则**：后一个的 start 必须**严格大于**前一个的 end。
- **状态**：排序后的下标、`nxt[i]`、`dp[j][i]`。
- **一句话建模**：这是一个 **"带个数上限的加权区间调度"**，DP 两维（从第几个活动往后、还剩几次）。

> [!note] 为什么按开始时间排序、往后 DP
> 按 start 排序后，"选了 i 之后下一个能选的"是一个前缀之后的连续段，二分就能找到第一个 `start > end_i`。`dp[j][i]` 表示"只考虑第 i 个及以后、至多再选 j 个"，转移只看 `i+1` 和 `nxt[i]`。

## 3. 下笔顺序

1. **问清**：end 是否包含？k 与 n 的乘积上限？价值会不会为负？
2. **Part 1**：排序 → `starts` → `nxt` → 从后往前填 `dp`（外层 j，内层 i 倒序）。
3. **Part 2**：保留整张表，从 `(i=0, j=k)` 往前走：取与不取价值相同时优先取（确定性），取了跳到 `nxt[i]`、`j−1`。
4. **Part 3**：按 end 排序，`best[i] = max(best[i−1], v + best[p])`，`p = bisect_left(ends, start)`（结束严格早于开始的个数）。O(n log n)。
5. **收尾**：`k = 0`、空、`k > n`、相邻闭区间冲突。

## 4. 代码怎么组织

```
_validate(events)
_table(events, k) -> (order, nxt, dp)       # Part 1/2 共用
max_value / max_value_with_events           # Part 1 / Part 2
max_value_unbounded                         # Part 3：不同排序、一维
_read_k / _read_events / part1..part3
```

## 5. 核心代码骨架

```python
def _table(events, k):
    order = sorted(range(len(events)), key=lambda i: (events[i][0], events[i][1], i))
    starts = [events[i][0] for i in order]
    nxt = [bisect_right(starts, events[order[i]][1]) for i in range(len(order))]
    n = len(order)
    dp = [[0] * (n + 1) for _ in range(k + 1)]
    for j in range(1, k + 1):
        for i in range(n - 1, -1, -1):
            take = events[order[i]][2] + dp[j - 1][nxt[i]]
            dp[j][i] = max(dp[j][i + 1], take)
    return order, nxt, dp

def max_value_unbounded(events):
    order = sorted(range(len(events)), key=lambda i: (events[i][1], events[i][0], i))
    ends = [events[i][1] for i in order]
    best = [0] * (len(order) + 1)
    for pos, idx in enumerate(order, 1):
        s, _, v = events[idx]
        best[pos] = max(best[pos - 1], v + best[bisect_left(ends, s)])
    return best[-1]
```

## 6. 每个 part 叠加什么

| Part | 改动 | 复杂度 |
|---|---|---|
| 1 | 二维 DP | O(n log n + n·k) |
| 2 | 保留整表，正向回溯 | 同上 |
| 3 | 换成按 end 排序的一维 DP | O(n log n) |

## 7. 常见坑

- `bisect_left` 写在闭区间上：`[1,2]` 和 `[2,3]` 被当成不冲突。
- `k` 维度开成 `k` 而不是 `k+1`。
- Part 2 回溯时忘了跳到 `nxt[i]` 而是 `i+1`。
- Part 3 仍用二维表：`k = n = 10⁵` 时 10¹⁰。
- 相同区间出现多次、单日活动。

## 8. 追问怎么接

1. **内存 O(n·k) 太大？** Part 1 只要两层滚动；Part 2 要方案就记"选择位"或 Hirschberg 式分治。
2. **半开区间？** `bisect_right` 改 `bisect_left`。
3. **活动流式到达（按结束时间）？** Part 3 的递推可在线维护；乱序到达用平衡树维护"结束时间 → 最优前缀值"。
4. **每个活动有参加成本、预算约束？** 变成带容量的背包，维度换成预算。

## 9. 自测清单

- [ ] 说出闭区间用 `bisect_right` 的原因
- [ ] 写出 Part 1 的 DP 转移
- [ ] 写出 Part 3 的一维递推

## 相关题与 skills

S03 加权区间调度 · S08 复杂度再压一档。相关：`q04` Maximum Order Volume（同一模式的 OA 版）、`q01` paid/free server（二选一调度 DP）。
