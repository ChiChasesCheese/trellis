---
slug: flower-planting-with-no-adjacent
---
## Q
**LC 1042 不邻接植花**｜Medium

`n` 个花园，`paths` 是双向的路径，每个花园至多连着 3 条路径。有 4 种花，给每个花园种一种，使有路径相连的花园种的花不同，返回任一方案（花的种类是 `1..4`）。

## A
**一句话。** 每个花园至多 3 个邻居，4 种花总能剩下一种；按编号顺序给每个花园选一种邻居没用过的花（贪心着色）。

```python
def garden_no_adj(n, paths):
    g = [[] for _ in range(n)]
    for a, b in paths:
        g[a - 1].append(b - 1)
        g[b - 1].append(a - 1)
    color = [0] * n              # 0 表示还没种
    for i in range(n):
        used = {color[j] for j in g[i]}
        for c in (1, 2, 3, 4):
            if c not in used:
                color[i] = c     # 邻居用过的不选，总有剩的
                break
    return color
```

**复杂度。** 时间 `O(n + m)`，空间 `O(n + m)`。

**易错点。**
- 下标差 1：花园编号从 1 开始，数组从 0 开始。
- 把 `0` 当成一种颜色：未种的邻居是 `0`，不影响 `1..4` 的选择。

**追问。**
- 为什么贪心一定成功？：最大度数是 3，邻居最多占用 3 种颜色，4 种颜色里必有空余。
- 度数没限制呢？：贪心不保证，一般图着色是 NP 难问题，只能保证颜色数不超过最大度数加 1。

**同模式。** LC 785 判断二分图、LC 886 可能的二分法、LC 133 克隆图
