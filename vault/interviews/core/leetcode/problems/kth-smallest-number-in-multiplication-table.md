---
slug: kth-smallest-number-in-multiplication-table
---
## Q
**LC 668 乘法表中第k小的数**｜Hard

`m × n` 的乘法表第 `i` 行第 `j` 列是 `i·j`（从 1 起）。返回表中第 `k` 小的数。

## A
**一句话。** 对答案二分：数「表中不超过 `x` 的数有多少个」，第 `i` 行有 `min(x // i, n)` 个，找最小的 `x` 使个数 `≥ k`。

```python
def find_kth_number(m, n, k):
    def count(x):                   # 表中 <= x 的个数
        return sum(min(x // i, n) for i in range(1, m + 1))
    lo, hi = 1, m * n
    while lo < hi:
        mid = (lo + hi) // 2
        if count(mid) >= k:
            hi = mid                # mid 可能就是答案
        else:
            lo = mid + 1
    return lo
```

**复杂度。** 时间 `O(m log(mn))`，空间 `O(1)`。

**易错点。**
- 用 `count(mid) > k` 判断：要找个数刚好达到 `k` 的最小值，应是 `>= k` 并收缩右端。
- 每行忘了 `min(…, n)`：`x` 大时 `x // i` 会超过列数。
- 答案一定在表里：二分得到的最小 `x` 满足个数 `≥ k` 而 `x-1` 不满足，所以 `x` 必是表中的数。

**追问。**
- 为什么能二分？：`count(x)` 随 `x` 单调不减，是「值域上的二分」。
- 想要 `O(min(m,n) log)`？：交换使 `m ≤ n`，只遍历较小的维度。

**同模式。** LC 378 有序矩阵中第 K 小的元素、LC 719 找出第 K 小的数对距离、LC 440 字典序的第K小数字、LC 786 第 K 个最小的质数分数
