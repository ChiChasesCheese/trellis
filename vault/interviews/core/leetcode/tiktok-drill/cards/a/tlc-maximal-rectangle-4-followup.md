---
id: tlc-maximal-rectangle-4-followup
node: a.maximal-rectangle
type: qa
step: 4
---
## Q
**LC 85 最大矩形**｜追问

面试官接着问：（1）要返回最大矩形的位置而不只是面积？（2）矩阵一行一行流式到来、放不进内存？（3）改成求最大的正方形？

## A
1. **返回位置。** 弹栈结算面积时，当前行 `r` 就是矩形的底边：

```python
def maximal_rectangle_box(matrix: list[list[str]]) -> tuple[int, tuple[int, int, int, int]]:
    heights = [0] * len(matrix[0])
    best, box = 0, (-1, -1, -1, -1)             # 面积；(上, 左, 下, 右)，闭区间
    for r, row in enumerate(matrix):
        heights = [h + 1 if cell == "1" else 0 for h, cell in zip(heights, row)]
        padded = [*heights, 0]
        stack: list[int] = []
        for i, h in enumerate(padded):
            while stack and padded[stack[-1]] >= h:
                height = padded[stack.pop()]
                left = stack[-1] if stack else -1
                area = height * (i - left - 1)
                if area > best:
                    best, box = area, (r - height + 1, left + 1, r, i - 1)
            stack.append(i)
    return best, box
```

2. **流式。** 栈版本一次只读一行，只保留 `heights`（`O(cols)`），天然适合流式输入；每来一行更新高度再结算一次。
3. **最大正方形（LC 221）。** 状态 `dp[i][j]` 是以 `(i, j)` 为右下角的最大正方形边长，`dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1`（该格为 `1`），用完整的二维表；空间可以压到 `O(n)`：见 Python 工具箱「DP 降维」。

**Python 提醒**：矩阵元素是字符串，`if cell` 对 `"0"` 也为真，必须写 `cell == "1"`；初始化二维表不要写 `[[0] * cols] * rows`，它会让所有行共用同一个列表。
