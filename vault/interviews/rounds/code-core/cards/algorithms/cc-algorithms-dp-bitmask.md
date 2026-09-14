---
id: cc-algorithms-dp-bitmask
node: algorithms.dp
type: qa
---
## Q
n ≤ 20 balances must be split into as many disjoint zero-sum groups as possible. Approach and cost?

## A
**Bitmask DP over subsets:** `dp[mask]` = the greatest number of disjoint zero-sum groups the members of `mask` can be split into.

```python
for mask in range(1, 1 << n):
    low = mask & -mask
    total[mask] = total[mask ^ low] + val[low.bit_length() - 1]
    dp[mask] = max(dp[mask ^ (1 << i)] for i in range(n) if mask >> i & 1) + (total[mask] == 0)
```

- O(2^n · n) — about 2·10^7 at n = 20, which is the practical ceiling for an interpreted language.
- `mask & -mask` isolates the lowest set bit; that is how each subset's sum is built in O(1) from a smaller subset.
- The settlement answer is then `n − dp[full]` ([[cc-algorithms-settlement-min-transfers]]).
- Above n ≈ 22 this is dead — and the constraint saying "n ≤ 20" is the problem telling you which technique it wants ([[cc-algorithms-recognition-constraint-sizes]]).

## Q zh
n ≤ 20 个余额要被划分成尽可能多的互不相交的零和组。思路和代价？

## A zh
**在子集上做 bitmask DP：** `dp[mask]` = `mask` 中的成员最多能被划分成多少个互不相交的零和组。

```python
for mask in range(1, 1 << n):
    low = mask & -mask
    total[mask] = total[mask ^ low] + val[low.bit_length() - 1]
    dp[mask] = max(dp[mask ^ (1 << i)] for i in range(n) if mask >> i & 1) + (total[mask] == 0)
```

- O(2^n · n) —— n = 20 时约 2·10^7，这是解释型语言的实际上限。
- `mask & -mask` 取出最低位的 1；这就是从更小的子集在 O(1) 内推出每个子集和的方法。
- 清账的答案于是是 `n − dp[full]`（[[cc-algorithms-settlement-min-transfers]]）。
- n 超过约 22 这条路就死了 —— 而写着「n ≤ 20」的约束正是题目在告诉你它想要哪种技术（[[cc-algorithms-recognition-constraint-sizes]]）。
