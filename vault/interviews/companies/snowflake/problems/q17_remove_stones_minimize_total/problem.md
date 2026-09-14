# q17 · Remove Stones to Minimize the Total — 反复对半去掉最大堆，最小化总量

> Snowflake OA 题池（FastPrep 汇总）直接复用的 LeetCode 原题。Part 1 为原题；Part 2 **(reconstructed)**：堆是在线到达的，操作和插入穿插进行。

## 背景

`catalog/raw/coding_oa.md` #39："Remove Stones to Minimize the Total"，confidence MED，"LC-exact (LC 1962)，reported via FastPrep OA pool, Easy, Heap/Greedy, last reported 2024-12"。这是最经典的贪心+堆题之一：每次操作对"当前最大的一堆"取半（下取整），操作 k 次后求总量最小值——因为规则本身就规定了"选最大的那堆"，所以这题严格来说没有"选择空间"，贪心正确性是显然的（唯一合法操作序列本身就是最优的），真正考的是"用什么数据结构高效地反复取最大值"。

## 输入格式

- `piles: list[int]`，每个 `piles[i] >= 1`；
- `k: int`，`k >= 0`，操作次数。

非法输入（非正整数堆、`k` 为负数、非整数）抛 `ValueError`。

## API 契约

```python
def min_total_after_k_removals(piles: list[int], k: int) -> int

class StoneStream:
    def add(self, pile: int) -> None: ...
    def apply(self, k: int) -> int: ...
```

## 规则

### Part 1 — LC 1962 原题

执行 `k` 次操作：每次选**当前最大**的一堆，移走 `floor(pile / 2)` 颗石子（即堆变为 `pile - floor(pile/2)`，也就是 `ceil(pile/2)`）。`k` 次操作后返回所有堆的总和。

**解法**：最大堆（Python 用取负数模拟）。每次弹出最大值，减去它的一半（下取整），推回堆里，重复 `k` 次；如果堆顶已经是 `0`（意味着所有堆都已经是 `0`，因为最大堆顶是 `0` 说明全零），提前结束（后续操作不会再改变任何东西）。总复杂度 O(n + k log n)。

### Part 2 — 堆在线到达，操作穿插进行 **(reconstructed)**

`add(pile)` 随时插入一颗新的堆；`apply(k)` 立即对**当前已有的所有堆**执行 `k` 次上述操作，返回执行后的总量（并把状态保留到下一次 `add`/`apply`）。这正是把一次性的批处理算法变成一个长期存活的服务：同一个最大堆和一个滚动维护的 `total` 贯穿整个生命周期，不需要每次 `apply` 都重新汇总。

## Worked examples（全部由 `solution.py` 实际运行得出）

| 输入 | 输出 |
|---|---|
| Part1 `piles=[5,4,9], k=2` | `12`（LC1962 例 1：9→5，某个 5→3，剩 `[3,4,5]`） |
| Part1 `piles=[4,3,6,7], k=3` | `12`（LC1962 例 2） |
| Part1 `piles=[1], k=5` | `1`（`floor(1/2)=0`，再怎么操作都不变） |
| Part2：`add(5)`→`add(4)`→`add(9)`→`apply(2)` | `12` |
| Part2：再 `add(2)`→`apply(1)` | `12`（此时堆是 `[3,4,5,2]`，总量 14，取最大的 5 减 2 得 3，总量 12） |

## `main()` 命令流

```
PART 1              PART 2
3 2                  4
5 4 9                ADD 5
→ 12                 ADD 4
                      ADD 9
                      APPLY 2
                      → 12
```

## 边界清单

- `k = 0`：不做任何操作，原样返回总和
- `k` 远大于收敛所需次数：所有堆最终固定在 `0` 或 `1`（`floor(1/2)=0`，但 `1-0=1` 是不动点），提前终止避免浪费
- 单堆、所有堆相等
- 空堆列表 / 空流的 `apply`
- 非法输入：堆非正整数、`k` 为负数或非整数 → `ValueError`
- 性能：`n = 10⁵` 且 `k = 10⁵` 两个 part 都 < 2 s

## 追问

1. **为什么这题的贪心不需要证明"选最大"是最优的？** 因为规则本身就规定了"每次操作必须选当前最大的一堆"——这是题目定义的操作，不是候选人要设计的策略；真正的设计空间在于"如何在有序集合上高效地反复取最大值+更新"，也就是堆的选择。
2. **能不能不用堆，比如每次线性扫描找最大值？** 可以但是 O(kn)，`k, n` 都到 1e5 时会超时；堆把每次"取最大+更新"降到 O(log n)。
3. **如果堆的值域很小（比如 `<= 10^4`），能不能用桶/计数排序代替堆？** 可以：维护一个按堆大小分桶的计数数组，每次找最大非空桶，用桶排序思想避开堆的 `log` 因子，把总复杂度降到 O(n + k + maxVal)。
4. **在线场景下，如果还需要支持"移除某个特定的堆"呢？** 标准二叉堆不支持高效的任意删除；需要换成带"惰性删除"标记的堆，或者用平衡树/有序多重集合维护，删除变成 O(log n) 的标记+跳过。

## 来源与置信度

- **MED**：`catalog/raw/coding_oa.md` #39，FastPrep OA 题池汇总，"Easy, Heap/Greedy"，最近一次报告 2024-12，LC-exact，对应 https://leetcode.com/problems/remove-stones-to-minimize-the-total/ （LC 1962）。
- Part 2 为重建（reconstructed），非原题实录。

## 考什么

最大堆的标准应用（反复取最大值+更新，对应 skills_matrix S08 LC 原题族）· "规则已固定选择、只考数据结构效率"的贪心变体识别 · 在线服务化：把批处理算法包装成状态贯穿多次调用的长期对象。
