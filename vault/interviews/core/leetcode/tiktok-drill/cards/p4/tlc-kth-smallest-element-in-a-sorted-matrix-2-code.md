---
id: tlc-kth-smallest-element-in-a-sorted-matrix-2-code
node: p4.kth-smallest-element-in-a-sorted-matrix
type: qa
step: 2
---
## Q
**LC 378 有序矩阵中第 K 小的元素**｜写出 Python 实现

`n × n` 矩阵（`1 <= n <= 300`，值在 `[-10^9, 10^9]`），每行每列非递减；返回排序后的第 `k` 小元素（`1 <= k <= n^2`，重复值各算一个）。要求用 `O(1)` 额外内存。

## A
**思路。** 在 `[左上角, 右下角]` 的值域上二分 `mid`。`count_le(mid)` 用阶梯扫描数出 `<= mid` 的个数：行从上到下，列指针从最右往左退，每行加上 `col + 1`。个数 `>= k` 则答案 `<= mid`，收缩上界；否则收缩下界。

```python
def kth_smallest(matrix: list[list[int]], k: int) -> int:
    n = len(matrix)

    def count_le(mid: int) -> int:             # 矩阵中 <= mid 的元素个数，阶梯式 O(n)
        count, col = 0, n - 1
        for row in matrix:                     # 行从上到下，每行的列边界只会左移
            while col >= 0 and row[col] > mid:
                col -= 1
            count += col + 1
        return count

    lo, hi = matrix[0][0], matrix[-1][-1]      # 答案一定落在 [最小值, 最大值]
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(mid) >= k:                 # 至少有 k 个数 <= mid：答案 <= mid
            hi = mid
        else:
            lo = mid + 1
    return lo
```

运行：`[[1,5,9],[10,11,13],[12,13,15]], k = 8` → `13`，`[[-5]], k = 1` → `-5`，`[[1,1],[1,3]]` 中 `k = 3` → `1`、`k = 4` → `3`；`n = 300` 约 `0.01` 秒。

**复杂度。** 时间 `O(n · log(max − min))`：二分约 `31` 轮，每轮 `count_le` 扫描 `O(n)`（行指针 `n` 次、列指针至多退 `n` 次）；空间 `O(1)`。

**写法要点。** `for row in matrix` 直接遍历行，免去下标；`count_le` 做成内层函数，闭包读取 `matrix` 和 `n`；`col` 在整个扫描里只减不增，这是阶梯法 `O(n)` 的原因；用 `lo < hi` 配 `hi = mid`，循环结束 `lo == hi` 就是答案，不需要再单独检查。Python 3.10+ 也可以写成 `lo + bisect_left(range(hi - lo + 1), k, key=lambda off: count_le(lo + off))`，让 `bisect` 做二分。
