---
slug: spiral-matrix
---
## Q
**LC 54 螺旋矩阵**｜Medium

按顺时针螺旋顺序返回 `m × n` 矩阵的所有元素。

## A
**一句话。** 维护四个边界，每圈依次走上、右、下、左四条边，走完边界各向内收一格。

```python
def spiral_order(matrix):
    res = []
    top, bot = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    while top <= bot and left <= right:
        res += matrix[top][left:right + 1]    # 上
        for r in range(top + 1, bot + 1):     # 右
            res.append(matrix[r][right])
        if top < bot and left < right:   # 至少两行两列才有下、左
            res += matrix[bot][left:right][::-1]  # 下
            for r in range(bot - 1, top, -1):     # 左
                res.append(matrix[r][left])
        top, bot = top + 1, bot - 1
        left, right = left + 1, right - 1
    return res
```

**复杂度。** 时间 `O(mn)`，空间 `O(1)`。

**易错点。**
- 漏掉 `top < bot and left < right`：`[[1,2,3]]` 得 `[1,2,3,2,1]`，`[[1],[2],[3]]` 得 `[1,2,3,2]`。
- 下边、左边把拐角取两次：下边不含最右格，左边行范围不含 `top` 和 `bot`。
- 切片结束下标忘了加一：`matrix[top+1:bot+1]` 才含 `bot` 行。

**追问。**
- 逆时针或从内向外？：改四条边的顺序，或把结果反转。
- 另一种写法？：方向向量 + 撞墙右转，用 `seen` 标记，见 LC 59。

**同模式。** LC 59 螺旋矩阵 II、LC 885 螺旋矩阵 III、LC 48 旋转图像、LC 498 对角线遍历
