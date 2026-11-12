---
slug: number-of-submatrices-that-sum-to-target
---
## Q
**LC 1074 元素和为目标值的子矩阵数量**｜Hard

统计矩阵 `matrix` 中元素和等于 `target` 的非空子矩阵个数，元素可为负。

## A
**一句话。** 枚举上下边界，把中间几行按列压成一维数组，再用前缀和加哈希数「和为 `target` 的子数组」。

```python
def num_submatrix_sum_target(matrix, target):
    m, n = len(matrix), len(matrix[0])
    ans = 0
    for top in range(m):
        col = [0] * n          # top..bottom 行的列和
        for bottom in range(top, m):
            row = matrix[bottom]
            col = [a + b for a, b in zip(col, row)]
            seen, s = Counter({0: 1}), 0
            for v in col:      # 一维：和为 target 的子数组
                s += v
                ans += seen[s - target]
                seen[s] += 1
    return ans
```

**复杂度。** 时间 `O(m^2 n)`，空间 `O(n)`。

**易错点。**
- 哈希表不以 `{0: 1}` 开头：从第一列开始的子数组漏掉，`[[5]]`、`target=5` 得 `0`，应为 `1`。
- 先更新后查询：`target = 0` 时数到自己（空子数组），`[[904]]` 得 `1`，应为 `0`。
- 用滑动窗口：有负数，`s > target` 时缩左端会错过解。

**追问。**
- 行数远大于列数怎么办？：先转置，枚举较小的那一维，变成 `O(min^2 · max)`。
- 和不超过 `target` 的个数？：哈希失效，改用有序结构 `bisect` 维护前缀和，`O(m^2 n log n)`。

**同模式。** LC 560 和为 K 的子数组、LC 363 矩形区域不超过 K 的最大数值和、LC 974 和可被 K 整除的子数组、LC 525 连续数组
