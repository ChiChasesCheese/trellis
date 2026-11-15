---
slug: parallel-courses-ii
---
## Q
**LC 1494 并行课程 II**｜Hard

`n` 门课，`relations[i] = [a, b]` 表示 `a` 是 `b` 的先修课。每学期最多上 `k` 门，且只能上先修课已全部修完的课。求修完全部课程的最少学期数。

## A
**一句话。** 状态压缩 DP：`f[mask]` 是修完集合 `mask` 的最少学期；每学期从「先修都满足的课」里选一个不超过 `k` 门的子集。

```python
def min_number_of_semesters(n, relations, k):
    pre = [0] * n
    for a, b in relations:
        pre[b - 1] |= 1 << (a - 1)       # b 的先修课集合
    f = [inf] * (1 << n)          # f[mask]：修完 mask 的最少学期
    f[0] = 0
    for mask in range(1 << n):
        if f[mask] == inf:
            continue
        avail = 0
        for i in range(n):
            done = pre[i] & mask == pre[i]   # 先修课都修完
            if done and not mask >> i & 1:
                avail |= 1 << i
        sub = avail
        while sub:                       # 枚举 avail 的非空子集
            if sub.bit_count() <= k:
                nm = mask | sub
                f[nm] = min(f[nm], f[mask] + 1)
            sub = (sub - 1) & avail
    return f[(1 << n) - 1]
```

**复杂度。** 时间 `O(3^n)`，空间 `O(2^n)`。

**易错点。**
- 每学期贪心选「后继最多」的课：局部最优不全局最优，要枚举子集。
- 子集大小不限制：选的门数必须 `≤ k`。
- 先修判断写成 `pre[i] & mask`：要求 `pre[i]` 全部在 `mask` 里，即 `pre[i] & mask == pre[i]`。

**追问。**
- 为什么复杂度是 `3^n`？：每门课对一个 `mask`，处于「已修」「可选子集」「其余」三种状态之一。
- 无环保证是什么？：题目保证先修关系是有向无环图，所以终点必可达。

**同模式。** LC 1136 平行课程、LC 207 课程表、LC 210 课程表 II
