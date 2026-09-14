---
id: cc-algorithms-dp-rolling-rows
node: algorithms.dp
type: qa
---
## Q
A 2-D DP table of 10^5 × 10^3 integers. Is that affordable, and what do you do about it?

## A
**10^8 cells is out of the question — but if the transition only reads the previous row, keep two rows.**

```python
prev = [0] * (m + 1)
for i in range(1, n + 1):
    cur = [0] * (m + 1)
    for j in range(1, m + 1):
        cur[j] = best(prev[j], cur[j - 1], prev[j - 1])
    prev = cur
```

- Memory drops from O(n·m) to O(m); the time is unchanged.
- **The price is reconstruction**: you can no longer walk the table back to recover *which* choices produced the answer. If the choice sequence is part of the output, keep the full table (or recompute by divide-and-conquer).
- Updating a single row in place works only when the transition reads strictly one direction — then the iteration order of that dimension is what preserves the values you still need (ascending for unbounded knapsack, descending for 0/1).
- Check the arithmetic before coding: 10^5 × 10^3 × 8 bytes is 800 MB of `int` objects at best ([[cc-algorithms-recognition-constraint-sizes]]).

## Q zh
一张 10^5 × 10^3 的二维整数 DP 表。负担得起吗？该怎么办？

## A zh
**10^8 个格子根本没门 —— 但如果转移只读上一行，就只保留两行。**

```python
prev = [0] * (m + 1)
for i in range(1, n + 1):
    cur = [0] * (m + 1)
    for j in range(1, m + 1):
        cur[j] = best(prev[j], cur[j - 1], prev[j - 1])
    prev = cur
```

- 内存从 O(n·m) 降到 O(m)；时间不变。
- **代价是无法回溯**：你再也不能沿表回走以恢复*哪些*选择产生了答案。如果选择序列是输出的一部分，就保留完整的表（或用分治重算）。
- 只有当转移严格只读一个方向时，才能原地更新单行 —— 此时该维度的遍历顺序正是保住你还需要的值的关键（完全背包升序，0/1 背包降序）。
- 写代码前先算一下：10^5 × 10^3 × 8 字节，往好里说也是 800 MB 的 `int` 对象（[[cc-algorithms-recognition-constraint-sizes]]）。
