# q12 · Merge Intervals — 合并重叠区间

> 2023 Snowflake OA 候选人索引直接复用的 LeetCode 原题。Part 1 为原题；Part 2 **(reconstructed)**：区间以数据流形式到达，支持随时查询当前合并结果。

## 背景

`catalog/raw/coding_oa.md` #19（对应 2023 Canada OA 索引 item #17）："Merge Intervals (LC-exact)"，直链 https://leetcode.com/problems/merge-intervals/ （LC 56），confidence MED，逐字复用无改编。这是最经典的区间合并题，Snowflake 的 OA 索引把它原样列出——没有任何本地化改编。

Part 2 的追问场景是面试官常见的追加提问："如果区间不是一次性给你，而是一个一个到达（比如系统里不断有新的'占用时段'注册进来），你怎么维护随时可查的合并视图？" 这把一次性算法题变成一个需要考虑增量维护策略的小系统设计问题。

## 输入格式

- **Part 1**：`intervals: list[list[int]]`，每个区间 `[start, end]`，`start <= end`（整数）。
- **Part 2**：一个 `IntervalStream` 对象，支持 `add(interval)`（把新区间放进流）和 `snapshot()`（返回当前所有已加入区间的合并结果）。

非法输入（区间不是长度为 2、边界非整数、或 `start > end`）抛 `ValueError`。

## API 契约

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]

class IntervalStream:
    def add(self, interval: list[int]) -> None: ...
    def snapshot(self) -> list[list[int]]: ...
```

## 规则

### Part 1 — LC 56 原题

合并所有重叠（包括首尾相接，即 `next.start <= current.end`）的区间，按 `start` 升序返回不重叠区间列表。

### Part 2 — 流式 add/snapshot **(reconstructed)**

区间通过 `add(interval)` 逐个到达（最多 1e5 次操作，`add` 和 `snapshot` 混合）；`snapshot()` 在被调用时返回"到目前为止所有已添加区间"的合并结果（等价于对已收到的全部区间跑一次 Part 1）。`add` 只做缓冲（均摊 O(1)），`snapshot` 重新排序+扫描（O(m log m)，`m` 为已加入区间数）——因为实际访问模式是"写多读少"，把排序开销摊到偶尔的读上比每次写都维护有序结构更简单也足够快。

## Worked examples（全部由 `solution.py` 实际运行得出）

| 输入 | 输出 |
|---|---|
| Part1 `[[1,3],[2,6],[8,10],[15,18]]` | `[[1, 6], [8, 10], [15, 18]]`（LC56 例 1） |
| Part1 `[[1,4],[4,5]]` | `[[1, 5]]`（LC56 例 2，首尾相接也算重叠） |
| Part1 `[[1,10],[2,3]]` | `[[1, 10]]`（完全嵌套） |
| Part2：`add([1,3])`→`add([6,8])`→`snapshot()` | `[[1, 3], [6, 8]]` |
| Part2：再 `add([2,5])`→`snapshot()` | `[[1, 5], [6, 8]]`（新区间把前两个桥接） |
| Part2：再 `add([7,9])`→`snapshot()` | `[[1, 5], [6, 9]]` |

## `main()` 命令流

```
PART 1                          PART 2
4                                4
1 3                              ADD 1 3
2 6                              ADD 6 8
8 10                             SNAPSHOT
15 18                            ADD 2 5
→ 1,6 8,10 15,18                 → 1,3 6,8
```

## 边界清单

- 首尾相接（`[1,4],[4,5]`）算重叠，必须合并；差 1 但不相接（`[1,3],[4,5]`）不合并
- 完全嵌套 / 完全重复的区间
- 空输入（`[]` → `[]`）、单区间、单点区间（`start == end`）
- 输入未按 `start` 排序、负数边界
- 非法区间（长度不对 / 非整数 / `start > end`）→ `ValueError`
- Part 2：空流的 `snapshot()`；`snapshot()` 返回值被调用方修改不能影响内部状态
- 性能：`n = 10⁵` 两个 part 都 < 2 s

## 追问

1. **为什么排序后一次扫描就够？** 按 `start` 排序后，当前区间只可能和"最近一个已合并区间"重叠（更早的区间要么已被并入，要么 `end` 更小不可能覆盖到后面），所以只需维护一个"当前合并区间"指针。
2. **如果区间是流式到来，且 `snapshot` 调用远比 `add` 频繁怎么办？** 换成有序结构（如按 `start` 排序的平衡树/跳表）做增量插入合并，使单次 `add` 摊销 O(log m)，避免每次 `snapshot` 都重新排序全部数据。
3. **区间数很大但取值范围小怎么优化？** 用差分数组/位图标记覆盖区间，一次线性扫描找出所有连续 `True` 段，把复杂度从 O(n log n) 降到 O(range)。
4. **多线程并发 `add` 呢？** 需要给 `_intervals` 加锁或用无锁队列缓冲，`snapshot` 读取时做一次性快照（复制或版本号），避免读到中间状态。

## 来源与置信度

- **MED**：`catalog/raw/coding_oa.md` #19，2023 Canada OA 索引 item #17，直链 https://leetcode.com/problems/merge-intervals/ （LC 56，逐字复用）。
- Part 2 为重建（reconstructed），非原题实录。

## 考什么

排序 + 一次扫描的区间合并范式 · 边界条件的精确定义（"重叠"包含"相接"）· 流式/增量场景下"写多读少"的摊销设计权衡（对应 skills_matrix S06 事件流/滑窗族的相邻技能点）。
