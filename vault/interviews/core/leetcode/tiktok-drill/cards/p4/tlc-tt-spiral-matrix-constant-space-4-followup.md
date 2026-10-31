---
id: tlc-tt-spiral-matrix-constant-space-4-followup
node: p4.tt-spiral-matrix-constant-space
type: qa
step: 4
---
## Q
**螺旋矩阵（O(1) 额外空间、不改输入）**｜追问

面试官接着问：（1）逆过来，生成 `n x n` 的螺旋矩阵（LC 59）；（2）起点和方向不固定，从任意格子向外螺旋（LC 885）；（3）输出的列表也要省掉，能不能做成惰性的？

## A
1. **生成螺旋矩阵**：同样的四条边界，改成往格子里填计数器 `1, 2, 3, ...`；`n x n` 的情形下 `top < bottom` 这类守卫仍然需要，最里面一圈可能只有一格。
2. **向外螺旋**：步长按 `1, 1, 2, 2, 3, 3, ...` 增长，方向依次为右、下、左、上；走到矩阵外的格子照样前进但不输出，直到输出了 `m * n` 个元素为止。这时用的是方向向量，没有边界收缩。
3. **惰性输出**：把函数改成生成器，用 `yield` 逐个产出，调用方可以边消费边处理，额外空间仍是 `O(1)`。

```python
from collections.abc import Iterator


def spiral_iter(matrix: list[list[int]]) -> Iterator[int]:
    if not matrix or not matrix[0]:
        return
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            yield matrix[top][c]
        for r in range(top + 1, bottom + 1):
            yield matrix[r][right]
        if top < bottom:
            for c in range(right - 1, left - 1, -1):
                yield matrix[bottom][c]
        if left < right:
            for r in range(bottom - 1, top, -1):
                yield matrix[r][left]
        top, bottom, left, right = top + 1, bottom - 1, left + 1, right - 1
```

`list(spiral_iter([[1,2,3],[4,5,6],[7,8,9]]))` → `[1, 2, 3, 6, 9, 8, 7, 4, 5]`。

**Python 提醒**：生成器函数里不能 `return 值` 来返回结果；空矩阵时写裸 `return` 就是产出零个元素。对反向区间用 `range(a, b, -1)`，不要用反向切片：下界为 `-1` 的切片会从末尾倒数，`[1, 2, 3][1:-1:-1]` 得到 `[]`。
