---
slug: maximal-rectangle
---
## Q
**LC 85 最大矩形**｜Hard

`'0'`、`'1'` 矩阵，求只含 `'1'` 的最大矩形面积。

## A
**一句话。** 逐行累计每列向上连续 `1` 的高度，每行当作一次 LC 84 柱状图最大矩形，用单调栈求解。

```python
def maximal_rectangle(matrix):
    def hist(hs):
        hs = hs + [0]              # 哨兵，弹空栈
        st, best = [], 0
        for i, h in enumerate(hs):
            while st and hs[st[-1]] >= h:
                top = hs[st.pop()]
                left = st[-1] if st else -1
                best = max(best, top * (i - left - 1))
            st.append(i)
        return best

    hs = [0] * len(matrix[0])
    best = 0
    for row in matrix:
        hs = [h + 1 if c == "1" else 0
              for h, c in zip(hs, row)]
        best = max(best, hist(hs))
    return best
```

**复杂度。** 时间 `O(rows·cols)`，空间 `O(cols)`。

**易错点。**
- 遇到 `0` 不清零：`[["1"],["0"],["1"]]` 得 `2`，应为 `1`。
- 漏掉末尾哨兵 `0`：栈里剩下的柱子没人弹出，`[["1","1"]]` 得 `1`，应为 `2`。
- 用 `if cell` 判断：`"0"` 是非空字符串恒为真，必须写 `c == "1"`。

**追问。**
- 只求最大正方形呢？：LC 221，`dp[i][j] = min(上, 左, 左上) + 1`。
- 不用栈能做吗？：用 `height/left/right` 三张表做 DP。

**同模式。** LC 84 柱状图中最大的矩形、LC 221 最大正方形、LC 1504 统计全 1 子矩形、LC 42 接雨水
