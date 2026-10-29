---
id: tlc-maximal-rectangle-5-alt
node: b.maximal-rectangle
type: qa
step: 5
---
## Q
**LC 85 最大矩形**｜另一种解法

不用单调栈，能不能用动态规划（DP）求最大矩形？这种做法和栈解法比，什么时候该选哪个？

## A
**思路。** 对每个格子 `(i, j)`，考虑「以它为底边上的一格、高度取 `height[i][j]`」的最宽矩形：`height[i][j]` 是向上连续 `1` 的个数；`left[i][j]`、`right[i][j]` 是在这个高度下能向左、向右延伸到的边界。向上一行的边界与本行最近的 `0` 取交，就得到本行的边界。面积 `height * (right - left)`，所有格子取最大。

```python
def maximal_rectangle_dp(matrix: list[list[str]]) -> int:
    rows, cols = len(matrix), len(matrix[0])
    height = [[0] * cols for _ in range(rows)]          # height[i][j]：(i, j) 向上连续 1 的个数
    left = [[0] * cols for _ in range(rows)]            # left[i][j]：高度 height[i][j] 的矩形能向左延伸到的最左列
    right = [[cols] * cols for _ in range(rows)]        # right[i][j]：能向右延伸到的最右列 + 1（开区间）
    best = 0
    for i in range(rows):
        cur_left, cur_right = 0, cols                   # 本行里"最近的 0"在左 / 右的位置
        for j in range(cols):
            if matrix[i][j] == "1":
                height[i][j] = (height[i - 1][j] if i else 0) + 1
                left[i][j] = max(left[i - 1][j] if i else 0, cur_left)
            else:
                cur_left = j + 1                        # 0 把下一格的左边界推到 j + 1
        for j in range(cols - 1, -1, -1):
            if matrix[i][j] == "1":
                right[i][j] = min(right[i - 1][j] if i else cols, cur_right)
                best = max(best, height[i][j] * (right[i][j] - left[i][j]))
            else:
                cur_right = j                           # 0 把前一格的右边界拉到 j
    return best
```

运行：题面示例 → `6`；`[["0"]]` → `0`；`[["1"]]` → `1`；`200 x 200` 全 `"1"` → `40000`。

**为什么对。** 对高度 `height[i][j]` 的矩形，它必须同时满足每一列在第 `i` 行向上都至少有这么高：向左的边界是上一行同一列的边界与「本行最近的 0」中更靠右的那个（`max`），向右取更靠左的（`min`）。所以 `left`、`right` 一格一格递推，不需要栈。

**取舍。** DP 版没有栈和弹出逻辑，容易证明，三张 `rows x cols` 的完整表空间 `O(rows * cols)`，时间同样 `O(rows * cols)`；栈版空间只有 `O(cols)`，并且把问题还原成 LC 84，一次学会两道题，也适合流式。面试里先说栈版（更通用），被追问「不用栈」时给 DP。
