---
id: tlc-patterns-hashing-5-variants
node: patterns.hashing
type: qa
step: 5
---
## Q
**哈希（Hashing）｜五种变形**

哈希题有哪几种常见形态？每种里「键」和「值」分别是什么，模板怎么改？

## A
1. **补数查找**（LC 1）：键 = 元素值，值 = 下标；查 `target - x`。变形：LC 15 三数之和（排序 + 双指针更合适）、LC 560（键 = 前缀和，值 = 出现次数）。
2. **频次统计**（LC 347、438、76）：`Counter`；比较两个窗口的计数、取前 `k` 大。
3. **签名分组**（LC 49、694）：键 = 归一化形状。LC 694 不同岛屿的数量：DFS 记录每个格子相对起点的偏移，排序后转 `tuple` 放进 `set`。
4. **集合判存在 / 去重**（LC 128、217）：只关心「有没有」，用 `set`；LC 128 用 `x - 1 not in s` 定位起点。
5. **点 / 对作为键**（LC 939）：把坐标 `(x, y)` 放进 `set`，枚举对角线上的两点，检查另两个角是否存在：

```python
def min_area_rect(points: list[list[int]]) -> int:
    seen: set[tuple[int, int]] = set()
    best = float("inf")
    for x, y in points:
        for px, py in seen:               # 与之前的每个点配对做对角
            if x != px and y != py and (x, py) in seen and (px, y) in seen:
                best = min(best, abs(x - px) * abs(y - py))
        seen.add((x, y))
    return 0 if best == float("inf") else int(best)
```

运行：`[[1,1],[1,3],[3,1],[3,3],[2,2]]` → `4`；`[[1,1],[1,3],[3,1],[3,3],[4,1],[4,3]]` → `2`；`[[0,0],[1,1]]` → `0`。时间 `O(n^2)`，`n <= 500` 可行。
