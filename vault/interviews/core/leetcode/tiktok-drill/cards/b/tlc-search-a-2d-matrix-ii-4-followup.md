---
id: tlc-search-a-2d-matrix-ii-4-followup
node: b.search-a-2d-matrix-ii
type: qa
step: 4
---
## Q
**LC 240 搜索二维矩阵 II**｜追问

面试官接着问：（1）`m` 远小于 `n` 时有没有更快的写法？（2）要统计矩阵里不超过 `target` 的元素个数？（3）为什么不能像 LC 74 那样整体二分？

## A
1. **`m` 远小于 `n`。** 逐行二分的 `O(m log n)` 可能比 `O(m + n)` 更快：

```python
from bisect import bisect_left


def search_matrix_bisect(matrix: list[list[int]], target: int) -> bool:
    for row in matrix:
        i = bisect_left(row, target)
        if i < len(row) and row[i] == target:
            return True
    return False
```

2. **统计不超过 `target` 的个数。** 阶梯法：从右上角出发，若 `matrix[row][col] <= target`，这一行从左到当前列都不超过，加上 `col + 1` 并下移；否则左移。`O(m + n)`，这是 LC 378「第 K 小」二分答案的内层判断。
3. **不能整体二分。** LC 74 保证每行末尾小于下一行开头，所以拉直后整体有序；这里没有这个保证（例 1 第一行末尾 `15`、第二行开头 `2`），拉直后的数组不是有序的，二分的前提不成立。

**Python 提醒**：`bisect_left` 返回的是插入点，不是"是否找到"；必须检查 `i < len(row)` 并确认 `row[i] == target`，否则目标比所有元素都大时会越界或误判。
