---
slug: spiral-matrix
---
## Q
**LC 54 螺旋矩阵**｜Medium

按顺时针螺旋顺序返回 `m × n` 矩阵的所有元素。

## A
**一句话。** 维护四个边界，每圈依次走上、右、下、左四条边，走完边界各向内收一格。

**图解。** 沿上、右、下、左走完一圈后，四个边界各向内收一格，再走下一圈。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 180">
<rect x="46" y="30" width="34" height="34" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="63.0" y="51.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="80" y="30" width="34" height="34" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="97.0" y="51.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="114" y="30" width="34" height="34" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="131.0" y="51.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="148" y="30" width="34" height="34" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="165.0" y="51.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="46" y="64" width="34" height="34" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="63.0" y="85.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="80" y="64" width="34" height="34" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="97.0" y="85.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="114" y="64" width="34" height="34" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="131.0" y="85.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="148" y="64" width="34" height="34" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="165.0" y="85.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<rect x="46" y="98" width="34" height="34" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="63.0" y="119.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<rect x="80" y="98" width="34" height="34" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="97.0" y="119.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10</text>
<rect x="114" y="98" width="34" height="34" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="131.0" y="119.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">11</text>
<rect x="148" y="98" width="34" height="34" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="165.0" y="119.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">12</text>
<polyline points="73.0,57.0 175.0,57.0 175.0,125.0 73.0,125.0 73.0,91.0 141.0,91.0" fill="none" stroke-width="1.4" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="141.0,91.0 135.0,94.0 135.0,88.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="114" y="22" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">top</text>
<text x="114" y="150" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">bot</text>
<text x="40" y="85.0" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">left</text>
<text x="188" y="85.0" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">right</text>
<text x="130" y="172" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">浅色：第 1 圈　深色：第 2 圈</text>
</svg>

```python
def spiral_order(matrix):
    res = []
    top, bot = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    while top <= bot and left <= right:
        res += matrix[top][left:right + 1]    # 上
        for r in range(top + 1, bot + 1):     # 右
            res.append(matrix[r][right])
        if top < bot and left < right:   # 至少两行两列才有下、左
            res += matrix[bot][left:right][::-1]  # 下
            for r in range(bot - 1, top, -1):     # 左
                res.append(matrix[r][left])
        top, bot = top + 1, bot - 1
        left, right = left + 1, right - 1
    return res
```

**复杂度。** 时间 `O(mn)`，空间 `O(1)`。

**易错点。**
- 漏掉 `top < bot and left < right`：`[[1,2,3]]` 得 `[1,2,3,2,1]`，`[[1],[2],[3]]` 得 `[1,2,3,2]`。
- 下边、左边把拐角取两次：下边不含最右格，左边行范围不含 `top` 和 `bot`。
- 切片结束下标忘了加一：`matrix[top+1:bot+1]` 才含 `bot` 行。

**追问。**
- 逆时针或从内向外？：改四条边的顺序，或把结果反转。
- 另一种写法？：方向向量 + 撞墙右转，用 `seen` 标记，见 LC 59。

**同模式。** LC 59 螺旋矩阵 II、LC 885 螺旋矩阵 III、LC 48 旋转图像、LC 498 对角线遍历
