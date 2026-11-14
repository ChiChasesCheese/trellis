---
slug: flood-fill
---
## Q
**LC 733 图像渲染**｜Easy

从 `image[sr][sc]` 出发，把与它原色相同的四连通像素全部改成 `color`，返回修改后的图像。

## A
**一句话。** DFS 把与起点原色相同的四连通像素改成新色，改过的像素不再等于原色，所以不会重复访问。

**图解。** 从框中的起点出发，四连通且同色的格子都被改成新色，右下角的 `1` 不连通，保持原样。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 130">
<rect x="20" y="16" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="35.0" y="35.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="50" y="16" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="65.0" y="35.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="80" y="16" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="95.0" y="35.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="20" y="46" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="35.0" y="65.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="50" y="46" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="65.0" y="65.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="80" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="95.0" y="65.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="20" y="76" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="35.0" y="95.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="50" y="76" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="65.0" y="95.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="80" y="76" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="95.0" y="95.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="50" y="46" width="30" height="30" rx="1" fill="none" style="stroke:var(--accent,#3b6fd4)" stroke-width="2.6"/>
<polyline points="124,61 158,61" fill="none" stroke-width="1.4" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="158.0,61.0 152.0,64.0 152.0,58.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="170" y="16" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="185.0" y="35.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="200" y="16" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="215.0" y="35.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="230" y="16" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="245.0" y="35.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="170" y="46" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="185.0" y="65.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="200" y="46" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="215.0" y="65.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="230" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="245.0" y="65.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="170" y="76" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="185.0" y="95.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="200" y="76" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="215.0" y="95.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="230" y="76" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="245.0" y="95.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="65" y="124" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">原图，框为起点</text>
<text x="215" y="124" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">color = 2</text>
</svg>

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
