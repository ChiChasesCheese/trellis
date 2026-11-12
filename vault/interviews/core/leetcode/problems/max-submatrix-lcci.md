---
slug: max-submatrix-lcci
---
## Q
**面试题 17.24 最大子矩阵**｜Hard

`N × M` 整数矩阵，求元素和最大的子矩阵，返回左上、右下坐标 `[r1, c1, r2, c2]`，多解任返一个。

## A
**一句话。** 枚举上下边界把行压成一维列和，再在其上做 Kadane 并记起止列。

```python
def get_max_matrix(matrix):
    rows, cols = len(matrix), len(matrix[0])
    best, ans = float("-inf"), [0, 0, 0, 0]
    for top in range(rows):
        col = [0] * cols       # top..bottom 行的列和
        for bottom in range(top, rows):
            row = matrix[bottom]
            col = [a + b for a, b in zip(col, row)]
            cur = start = 0
            for c, v in enumerate(col):
                if cur > 0:
                    cur += v
                else:
                    cur, start = v, c    # 前面不为正，重开
                if cur > best:
                    best = cur
                    ans = [top, start, bottom, c]
    return ans
```

**复杂度。** 时间 `O(R²C)`，空间 `O(C)`。

**易错点。**
- `best` 初值写 `0`：全负矩阵 `[[-3,-1],[-2,-4]]` 返回 `[0,0,0,0]`，应为 `[0,1,0,1]`。
- Kadane 重启时只改 `cur` 不改 `start`：左边界错。

**追问。**
- 和不超过 `K` 的最大子矩阵？：Kadane 失效，对列和的前缀和用有序结构 `bisect` 找最小的 `>= 前缀和-K`（LC 363）。

**同模式。** LC 53 最大子数组和、LC 363 矩形区域不超过 K 的最大数值和、LC 1074 元素和为目标值的子矩阵数量、LC 85 最大矩形
