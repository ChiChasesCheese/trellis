---
slug: minimum-moves-to-spread-stones-over-grid
---
## Q
**LC 2850 将石头分散到网格图的最少移动次数**｜Medium

`3×3` 网格共 `9` 颗石头，每次把一颗石头移到相邻格。求让每格恰好一颗的最少移动次数。

## A
**一句话。** 多余石头和空格一一配对、代价是曼哈顿距离，枚举空格的全排列取最小。

```python
def minimum_moves(grid):
    cells = [(r, c) for r in range(3) for c in range(3)]
    extra = [(r, c) for r, c in cells
             for _ in range(grid[r][c] - 1)]  # 多 k 颗算 k-1 次
    empty = [(r, c) for r, c in cells if grid[r][c] == 0]
    return min(
        sum(abs(a - c) + abs(b - d)
            for (a, b), (c, d) in zip(extra, order))
        for order in permutations(empty))     # 谁去哪个空格
```

**复杂度。** 时间 `O(E!·E)`（`E<=8` 个空格），空间 `O(E)`。

**易错点。**
- 一格多颗只算一颗：`[[1,3,0],[1,0,0],[1,0,3]]` 得 `2`，应为 `4`。
- 贪心先配最近的一对：`[[0,2,0],[2,1,1],[1,1,1]]` 会得 `4`，应为 `2`。

**追问。**
- 网格更大怎么办？：排列爆炸，改状压 DP（`dp[mask]`）或匈牙利算法 `O(E^3)`。
- 每格需求量不同？：变成运输问题，用最小费用最大流。

**同模式。** LC 1066 校园自行车分配 II、LC 1947 最大兼容性评分和、LC 2172 数组的最大与和、LC 1879 两个数组最小的异或值之和
