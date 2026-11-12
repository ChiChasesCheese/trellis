---
slug: kth-smallest-element-in-a-sorted-matrix
---
## Q
**LC 378 有序矩阵中第 K 小的元素**｜Medium

`n × n` 矩阵每行每列都升序，求排序后第 `k` 小的元素（重复值各算一个），内存要优于 `O(n²)`。

## A
**一句话。** 二分答案：二分值 `mid`，阶梯式扫描数出 `<= mid` 的个数，个数 `>= k` 则答案 `<= mid`。

```python
def kth_smallest(matrix, k):
    n = len(matrix)

    def count_le(mid):         # 阶梯式 O(n)
        cnt, col = 0, n - 1
        for row in matrix:     # 列边界只会左移
            while col >= 0 and row[col] > mid:
                col -= 1
            cnt += col + 1
        return cnt

    lo, hi = matrix[0][0], matrix[-1][-1]
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**复杂度。** 时间 `O(n log(max-min))`，空间 `O(1)`。

**易错点。**
- 去重后再数：示例一去重后第 `8` 小是 `15`，应为 `13`。
- 收缩条件写成 `> k` 或 `hi = mid - 1`：返回不在矩阵里的值或差一位。
- 每行列指针都从头开始：退化成 `O(n²)`。

**追问。**
- 为什么返回的 `lo` 一定在矩阵里？：满足条件的最小值必须恰好等于某个元素，否则 `lo` 还能再减小。
- 还有别的解法吗？：堆做 `n` 路归并，`O(k log n)`，`k` 小时更快。

**同模式。** LC 668 乘法表中第 k 小的数、LC 719 找出第 K 小的数对距离、LC 786 第 K 个最小的素数分数、LC 373 查找和最小的 K 对数字
