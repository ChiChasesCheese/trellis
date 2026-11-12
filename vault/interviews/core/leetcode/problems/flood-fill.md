---
slug: flood-fill
---
## Q
**LC 733 图像渲染**｜Easy

从 `image[sr][sc]` 出发，把与它原色相同的四连通像素全部改成 `color`，返回修改后的图像。

## A
**一句话。** DFS 把与起点原色相同的四连通像素改成新色，改过的像素不再等于原色，所以不会重复访问。

```python
def flood_fill(image, sr, sc, color):
    old = image[sr][sc]
    if old == color:       # 同色：改了也不留痕迹，会无限递归
        return image
    m, n = len(image), len(image[0])

    def dfs(r, c):
        if 0 <= r < m and 0 <= c < n and image[r][c] == old:
            image[r][c] = color    # 兼作 visited
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

    dfs(sr, sc)
    return image
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 漏掉 `old == color` 的判断：`color` 与起点同色时无限递归，抛 `RecursionError`。
- 写成 8 个方向：右下角不连通的 `1` 被误改，示例 1 得 `[[2,2,2],[2,2,0],[2,0,2]]`。

**追问。**
- `50 x 50` 同色递归会爆栈？：蛇形路径深度可达 `2500`，改 BFS 或显式栈。
- 不想改原图？：另开 `visited` 集合，或复制一份图。

**同模式。** LC 200 岛屿数量、LC 695 岛屿的最大面积、LC 130 被围绕的区域、LC 463 岛屿的周长
