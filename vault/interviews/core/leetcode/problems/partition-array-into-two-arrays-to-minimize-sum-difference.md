---
slug: partition-array-into-two-arrays-to-minimize-sum-difference
---
## Q
**LC 2035 将数组分成两个数组并最小化数组和的差**｜Hard

长度为 `2n` 的数组（`n<=15`）分成各 `n` 个元素的两组，求两组和之差绝对值的最小值。

## A
**一句话。** 折半枚举：两半各枚举子集和并按个数分组，左选 `c` 个、右选 `n-c` 个，二分找最接近 `总和/2` 的搭档。

```python
def minimum_difference(nums):
    n = len(nums) // 2
    total = sum(nums)

    def sums_by_size(arr):
        by = [[0]] + [[] for _ in arr]   # by[c]：选 c 个的所有和
        for x in arr:
            for c in range(len(arr) - 1, -1, -1):  # 倒序防重用
                by[c + 1] += [s + x for s in by[c]]
        return by

    left = sums_by_size(nums[:n])
    right = sums_by_size(nums[n:])
    best = inf
    for c in range(n + 1):    # 左 c 个，右就必须 n-c 个
        rs = sorted(right[n - c])
        for a in left[c]:
            i = bisect_right(rs, total // 2 - a)
            for b in rs[max(i - 1, 0):i + 1]:
                best = min(best, abs(total - 2 * (a + b)))
    return best
```

**复杂度。** 时间 `O(2^n · n)`，空间 `O(2^n)`。

**易错点。**
- 忽略「各 `n` 个」：`[1,1,1,3]` 单取 `3` 得 `0`，应为 `2`，所以必须按个数分组。
- 初始最优值写成 `abs(total)`：它未必是合法分法，`[6,-1,6,-13]` 会得 `2`，应为 `12`；用 `inf`。
- 暴力 `combinations(nums, n)`：`n=15` 约 `1.55×10^8` 种，超时。

**追问。**
- 为什么只看二分位置左右两个邻居？：和 `a+b` 要最接近 `total/2`，最优 `b` 必在 `total//2 - a` 的插入位置两侧。
- 无「各 `n` 个」限制呢？：就是 LC 1049，背包 DP 即可。

**同模式。** LC 1755 最接近目标值的子序列和、LC 416 分割等和子集、LC 1049 最后一块石头的重量 II、LC 805 数组的均值分割
