# q13 · Minimum Interval to Include Each Query — 每个查询最小的覆盖区间

> 2023 Snowflake OA 候选人索引直接复用的 LeetCode 原题。Part 1 为原题；Part 2 **(reconstructed)**：不仅要大小，还要知道具体是哪个区间。

## 背景

`catalog/raw/coding_oa.md` #21（对应 2023 Canada OA 索引 item #19）："Minimum Interval to Include Each Query (LC-exact)"，直链 https://leetcode.com/problems/minimum-interval-to-include-each-query/ （LC 1851），confidence MED，逐字复用。

Part 2 的追问是很自然的现实需求：光知道"最小覆盖区间有多大"往往不够用，调用方通常还想知道"到底是哪个区间覆盖了我"，才能去查那个区间对应的记录/资源。

## 输入格式

- `intervals: list[list[int]]`，每个 `[left, right]`（`left <= right`），大小定义为 `right - left + 1`；
- `queries: list[int]`。

非法输入（区间长度不对、边界非整数、`left > right`，或 query 非整数）抛 `ValueError`。

## API 契约

```python
def min_interval_sizes(intervals: list[list[int]], queries: list[int]) -> list[int]
def min_interval_bounds(intervals: list[list[int]], queries: list[int]) -> list[tuple[int, int]]
```

## 规则

### Part 1 — LC 1851 原题

对每个 `queries[j]`，在所有满足 `left <= queries[j] <= right` 的区间里，返回**最小的 `size`**；如果没有区间覆盖它，返回 `-1`。

**标准解法**：把区间按 `left` 排序，把 query 按值排序但记住原始下标；用一个按 `(size, left)` 排序的最小堆做扫描——扫到某个 query 时，先把所有 `left <= query` 的区间压入堆，再把堆顶"已经过期"（`right < query`）的区间弹掉，剩下的堆顶就是当前最优。堆里可能残留其它已过期但还没弹出的条目，不影响正确性（它们的 key 一定不小于堆顶，永远不会被选中）。整体 O((n + q) log n)。

### Part 2 — 返回具体是哪个区间 **(reconstructed)**

不只是返回大小，还要返回被选中区间的 `(start, end)`。**平局规则**：多个区间大小相同都能覆盖该 query 时，选 `start` 最小的那个（堆的排序键就是 `(size, start)`，天然满足这个平局规则）。没有区间覆盖时返回 `(-1, -1)`。

## Worked examples（全部由 `solution.py` 实际运行得出）

| intervals | queries | Part 1 | Part 2 |
|---|---|---|---|
| `[[1,4],[2,4],[3,6],[4,4]]` | `[2,3,4,5]` | `[3, 3, 1, 4]`（LC1851 例 1） | `[(2,4), (2,4), (4,4), (3,6)]` |
| `[[2,3],[2,5],[1,8],[20,25]]` | `[2,19,5,22]` | `[2, -1, 4, 6]`（LC1851 例 2） | `[(2,3), (-1,-1), (2,5), (20,25)]` |
| `[[1,4],[2,5]]` | `[3]` | `[4]` | `[(1, 4)]`（大小同为 4，平局选 `start` 更小的 `[1,4]`） |
| `[]` | `[1,2]` | `[-1, -1]` | `[(-1,-1), (-1,-1)]` |

## `main()` 命令流

```
PART 1                    PART 2
4 4                        4 4
1 4                        1 4
2 4                        2 4
3 6                        3 6
4 4                        4 4
2 3 4 5                    2 3 4 5
→ 3 3 1 4                  → 2,4 2,4 4,4 3,6
```

## 边界清单

- query 命中区间边界（`left`/`right` 恰好等于 query）
- 单点区间（`left == right`，size = 1）
- 完全没有 query 覆盖它的区间（返回 `-1` / `(-1,-1)`）
- 完全重复的区间（相同 `[left, right]`）
- 空 `intervals` 或空 `queries`
- Part 2：同大小平局必须选 `start` 更小的（不能只看堆弹出顺序的偶然结果）
- 非法输入：区间长度不对 / 边界非整数 / `left > right` / query 非整数 → `ValueError`
- 性能：`n = q = 10⁵` 两个 part 都 < 2 s

## 追问

1. **为什么要按 query 的值排序而不是原始顺序处理？** 只有排序后才能保证"扫过的区间左端点单调不减"，从而保证每个区间只被压入堆一次，整体均摊 O(log n)。
2. **堆里躺着的"过期"区间会不会导致漏选？** 不会：堆顶永远是当前最小 key，过期的堆顶弹出后，下一个堆顶要么合法要么继续弹，任何还没弹出的过期条目 key 只会更大，天然被跳过。
3. **如果区间会动态增删（不是一次性给定）呢？** 需要换成支持删除的数据结构（如按 `(size, left)` 排序的平衡树/懒删除堆 + 版本号），删除操作变成 O(log n) 标记而不是重建。
4. **多个 query 相同值需要去重复用结果吗？** 可以：排序后相同值的 query 连续出现，处理完一个后可以直接复制结果给后面相同值的 query，避免重复弹堆判断（不影响复杂度上界但减少常数）。

## 来源与置信度

- **MED**：`catalog/raw/coding_oa.md` #21，2023 Canada OA 索引 item #19，直链 https://leetcode.com/problems/minimum-interval-to-include-each-query/ （LC 1851，逐字复用）。
- Part 2 为重建（reconstructed），非原题实录。

## 考什么

离线扫描 + 最小堆的"每个元素只进堆一次"摊销技巧（对应 skills_matrix S08 LC 原题+复杂度压一档）· 排序保持原始下标的模式 · 平局规则的显式定义（tie-break key 必须写进契约，呼应 CONVENTIONS.md 的排序规则要求）。
