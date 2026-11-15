---
slug: guess-number-higher-or-lower
---
## Q
**LC 374 猜数字大小**｜Easy

从 `1..n`（`n < 2^31`）中猜一个数，接口 `guess(num)` 返回 `-1`（猜大了）、`1`（猜小了）或 `0`（猜中）。返回这个数。

## A
**一句话。** 标准二分：在 `[lo, hi]` 里猜中点，猜大了收右边界，猜小了收左边界。

```python
def guess_number(n):
    lo, hi = 1, n              # 答案一定在 [lo, hi]
    while True:
        mid = (lo + hi) // 2
        r = guess(mid)
        if r == 0:
            return mid
        if r < 0:
            hi = mid - 1       # 猜大了
        else:
            lo = mid + 1       # 猜小了
```

**复杂度。** 时间 `O(log n)`，空间 `O(1)`。

**易错点。**
- 把 `-1` 当成「答案更小」以外的意思：`-1` 是 `num > pick`，要往左找。
- 在定长整数语言里写 `(lo + hi) / 2`：会溢出，要 `lo + (hi - lo) / 2`；Python 无此问题。

**追问。**
- 猜错要付钱、求最坏情况的最小花费？：区间 DP，`f[l][r] = min(k + max(f[l][k-1], f[k+1][r]))`，就是 LC 375。
- 只有「大于等于」的判断接口？：找第一个满足条件的位置，`while lo < hi` 写法，同 LC 278。

**同模式。** LC 704 二分查找、LC 278 第一个错误的版本、LC 35 搜索插入位置
