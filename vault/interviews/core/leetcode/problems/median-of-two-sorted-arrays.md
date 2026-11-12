---
slug: median-of-two-sorted-arrays
---
## Q
**LC 4 寻找两个正序数组的中位数**｜Hard

两个升序数组 `nums1`、`nums2`，求合并后的中位数，要求 `O(log(m+n))`。

## A
**一句话。** 在较短数组上二分切点，使左半共 `(m+n+1)//2` 个且左半最大值不超过右半最小值。

```python
def find_median_sorted_arrays(nums1, nums2):
    a, b = sorted((nums1, nums2), key=len)   # 在短的上二分
    m, n = len(a), len(b)
    half = (m + n + 1) // 2
    lo, hi = 0, m
    while lo <= hi:
        i = (lo + hi) // 2    # a 取前 i 个进左半
        j = half - i          # b 取前 j 个进左半
        al = a[i-1] if i > 0 else -inf
        ar = a[i] if i < m else inf
        bl = b[j-1] if j > 0 else -inf
        br = b[j] if j < n else inf
        if al > br:
            hi = i - 1
        elif bl > ar:
            lo = i + 1
        else:
            if (m + n) % 2:
                return float(max(al, bl))
            return (max(al, bl) + min(ar, br)) / 2
```

**复杂度。** 时间 `O(log min(m,n))`，空间 `O(1)`。

**易错点。**
- 在长数组上二分：`j = half - i` 越出 `[0, n]`，`([1..6],[7,8])` 结果错。
- `half` 写成 `(m+n)//2`：总数为奇数时左半少一个，`([1,3],[2])` 得 `1.0`，应为 `2.0`。
- 切在两端不加 `±inf` 哨兵：`a[i-1]`（`i=0`）取到末尾，`a[i]`（`i=m`）越界。

**追问。**
- 怎么二分「值」而不是切点？：对候选值用 `bisect_right` 统计两数组中 `<= x` 的个数，二分第 `k` 小。
- 数据流中位数（LC 295）？：大顶堆加小顶堆，插入 `O(log n)`。

**同模式。** LC 295 数据流的中位数、LC 378 有序矩阵中第 K 小的元素、LC 719 找出第 K 小的数对距离、LC 410 分割数组的最大值
