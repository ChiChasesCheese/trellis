---
id: tlc-trapping-rain-water-ii-5-alt
node: p4.trapping-rain-water-ii
type: qa
step: 5
---
## Q
**LC 407 接雨水 II**｜另一种解法

不用堆，换成「先假设内部水位很高、再反复往下松弛」的做法。写出来，并说明什么时候选它、什么时候选堆。

## A
**思路。** 每格的水位 `level` 满足：外圈 `level = 自身高度`；内部 `level = max(自身高度, 四个邻居水位的最小值)`。初始把所有内部格子的水位设成全图最高高度（上界），然后反复扫描内部格子，用这个公式往下更新，直到一整遍扫描没有任何变化。答案是 `sum(level − 高度)`。

```python
def trap_rain_water_relax(height_map: list[list[int]]) -> int:
    m, n = len(height_map), len(height_map[0])
    top = max(map(max, height_map))
    level = [[height_map[r][c] if r in (0, m - 1) or c in (0, n - 1) else top for c in range(n)]
             for r in range(m)]                # 内部先假设水位到最高，再不断往下松弛
    changed = True
    while changed:
        changed = False
        for r in range(1, m - 1):
            for c in range(1, n - 1):
                new = max(height_map[r][c],
                          min(level[r + 1][c], level[r - 1][c], level[r][c + 1], level[r][c - 1]))
                if new < level[r][c]:
                    level[r][c] = new
                    changed = True
    return sum(level[r][c] - height_map[r][c] for r in range(m) for c in range(n))
```

运行：示例 1 → `4`，示例 2 → `10`，`[[1,1,1],[1,0,1],[1,1,1]]` → `1`，`[[5]]` → `0`。

**对比。** 松弛法的正确性来自「水位是满足上述方程的最大解」，代码短、无需堆，面试里容易写对，适合先给出正确答案或者图很小时；但每一遍扫描 `O(mn)`，水位像波一样从边界往里传，每遍传不远，最坏需要 `O(mn)` 遍，总计 `O((mn)^2)`，`200 × 200` 时可能很慢。堆解法每格只处理一次，`O(mn log(mn))`，是规模到 `4 · 10^4` 时应该选的方案。

**别用的做法。** 按行、按列分别用一维方法再取较小值：水可以绕路流出，会多算（示例 1 得 `5`，正确 `4`）。
