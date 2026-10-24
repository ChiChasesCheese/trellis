---
id: tlc-maximal-square-4-followup
node: a.maximal-square
type: qa
step: 4
---
## Q
**LC 221 最大正方形**｜追问

面试官接着问：（1）统计矩阵里**所有**全 1 正方形的个数？（2）要返回最大正方形的位置，而不只是面积？（3）把「正方形」改成「矩形」怎么做？

## A
1. **统计个数**（LC 1277）：以 `(i, j)` 为右下角、边长最大为 `s` 的正方形，同时意味着边长 `1..s` 的正方形各有一个，贡献 `s` 个。所以把每格的 `dp` 累加即可，`3×3` 全 1 得 `14`。
```python
def count_squares(matrix: list[list[str]]) -> int:
    n = len(matrix[0])
    dp = [0] * (n + 1)
    total = 0
    for row in matrix:
        diag = 0
        for j, ch in enumerate(row):
            up = dp[j + 1]
            dp[j + 1] = min(dp[j], up, diag) + 1 if ch == "1" else 0
            diag = up
            total += dp[j + 1]
    return total
```
2. **返回位置**：需要知道右下角坐标。刷新最大边长时同时记 `(i, j)`，则左上角是 `(i - side + 1, j - side + 1)`。滚动数组下仍然成立，因为行号 `i` 和列号 `j` 在循环里都是现成的。
3. **最大矩形**（LC 85）：状态不再是边长，而是每列向上连续 `1` 的高度 `heights[j]`。对每一行，把 `heights` 当作柱状图，用单调栈求最大矩形面积（LC 84），总 `O(mn)`。关键的区别是：矩形的两条边相互独立，而正方形的两条边被同一个 `min(...) + 1` 绑在一起。

**Python 提醒**：输入是 `list[list[str]]`，每个元素是单字符字符串，比较用 `ch == "1"`；若有人传入整数矩阵，`"1" == 1` 为 `False`，DP 会静默地全部归零。把 `matrix` 转成整数矩阵再算时，注意 `int(ch)` 是 `O(1)` 但整张表要多一遍遍历。
