---
id: tlc-longest-consecutive-sequence-4-followup
node: a.longest-consecutive-sequence
type: qa
step: 4
---
## Q
**LC 128 最长连续序列**｜追问

面试官接着问：（1）要返回序列本身，而不仅是长度？（2）数据是流，每来一个数都要回答当前最长长度？（3）允许最多补 `k` 个缺失的数？

## A
1. **返回序列**：记下最优的起点 `start` 和长度 `best`，最后返回 `list(range(start, start + best))`。更新答案时用 `if end - x > best: best, start = end - x, x`。
2. **流式**：维护字典 `length`，`length[x]` 只在**段的两个端点**上有意义。新数 `x` 到来：若 `x` 已存在跳过；取 `left = length.get(x-1, 0)`、`right = length.get(x+1, 0)`，新段长 `total = left + right + 1`；把 `length[x - left]` 和 `length[x + right]` 都更新为 `total`（更新两端点），`best = max(best, total)`。每次 `O(1)`。也可用并查集按大小合并。
3. **补 `k` 个缺口**：先去重排序，得到升序数组 `a`；滑动窗口 `[l, r]`，窗口内缺口数 `(a[r] - a[l]) - (r - l)` 不超过 `k`，窗口长度加上 `k` 取最大（需要处理 `k` 超出两端的补数）。时间 `O(n log n)`（排序）。

**Python 提醒**：集合遍历顺序不保证，不要依赖它；`max(iterable, default=0)` 对空输入给默认值，比先判断 `if not nums` 更简洁；`set` 里放的是 `int`，哈希是它本身，`x - 1 in seen` 与数值大小无关，`10^9` 量级也是 `O(1)`。
