---
slug: maximum-length-of-pair-chain
---
## Q
**LC 646 最长数对链**｜Medium

数对 `[a, b]`（`a < b`），`[c, d]` 能接在 `[a, b]` 后面当且仅当 `b < c`。任选、任意顺序，求最长数对链的长度。

## A
**一句话。** 就是最多不相交区间：按右端排序，能接上就接，每次选结束最早的数对，给后面留最多空间。

```python
def find_longest_chain(pairs):
    pairs.sort(key=lambda p: p[1])   # 按右端排序
    ans, end = 0, -inf
    for a, b in pairs:
        if a > end:            # 严格大于才能接
            ans += 1
            end = b
    return ans
```

**复杂度。** 时间 `O(n log n)`，空间 `O(1)`（不计排序）。

**易错点。**
- 按左端排序后贪心：长区间排在前面会挡住后面多个短区间。
- 写成 `a >= end`：题目要求 `b < c`，端点相等不能接。

**追问。**
- DP 写法？：按左端排序后 `f[i] = 1 + max(f[j])`（`pairs[j][1] < pairs[i][0]`），就是 LIS，`O(n²)` 或二分 `O(n log n)`。
- 和 LC 435 的关系？：最多保留的不重叠区间数就是这里的链长，删掉的个数是 `n` 减它。

**同模式。** LC 435 无重叠区间、LC 452 用最少数量的箭引爆气球、LC 300 最长递增子序列
