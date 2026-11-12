---
slug: search-a-2d-matrix-ii
---
## Q
**LC 240 搜索二维矩阵 II**｜Medium

矩阵每行从左到右升序、每列从上到下升序，判断 `target` 是否存在。

## A
**一句话。** 从右上角出发：比目标大就左移（排除这一列），比目标小就下移（排除这一行）。

```python
def search_matrix(matrix, target):
    row, col = 0, len(matrix[0]) - 1    # 右上角：行最大、列最小
    while row < len(matrix) and col >= 0:
        x = matrix[row][col]
        if x == target:
            return True
        if x > target:
            col -= 1    # 整列都 >= x
        else:
            row += 1    # 整行都 <= x
    return False
```

**复杂度。** 时间 `O(m+n)`，空间 `O(1)`。

**易错点。**
- 当成 LC 74 展平二分：这里下一行开头可能比上一行末尾小，二分会漏解。
- 从左上角出发：右移下移都变大，无法决定排除什么。
- 边界写成 `col > 0`：漏掉第 `0` 列，应为 `col >= 0`。

**追问。**
- 从左下角出发行吗？：行，它是列最大、行最小，比目标大上移、小右移，与右上角对称。
- 统计 `<= target` 的个数？：同一阶梯，每行把 `col` 左移到 `<= target` 后累加 `col+1`，`O(m+n)`。

**同模式。** LC 74 搜索二维矩阵、LC 378 有序矩阵中第 K 小的元素、LC 11 盛最多水的容器、LC 167 两数之和 II
