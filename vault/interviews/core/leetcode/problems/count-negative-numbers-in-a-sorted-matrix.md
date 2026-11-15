---
slug: count-negative-numbers-in-a-sorted-matrix
---
## Q
**LC 1351 统计有序矩阵中的负数**｜Easy

`m × n` 矩阵按行、按列都非严格递减，统计负数个数。要求 `O(m+n)`。

## A
**一句话。** 每行负数在右侧连成一段，且分界列随行往下只会左移，指针 `j` 从右上角出发走一条阶梯。

**图解。** 深色是负数，每行的分界只会比上一行更靠左，`j` 全程只左移 `n` 步。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 212">
<rect x="26" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="41.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="56" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="86" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="101.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="116" y="12" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="131.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-1</text>
<rect x="26" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="41.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="56" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="86" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="101.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="116" y="46" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="131.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-1</text>
<rect x="26" y="80" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="41.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="56" y="80" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="86" y="80" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="101.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-1</text>
<rect x="116" y="80" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="131.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-2</text>
<rect x="26" y="114" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="41.0" y="132.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-1</text>
<rect x="56" y="114" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="71.0" y="132.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-1</text>
<rect x="86" y="114" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="101.0" y="132.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-2</text>
<rect x="116" y="114" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="131.0" y="132.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-3</text>
<text x="16" y="158" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">深色是负数：每行一段，在右侧</text>
<text x="16" y="176" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">分界列 j：3 → 3 → 2 → 0，只左移</text>
<text x="16" y="194" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor" font-weight="600">答案 1+1+2+4 = 8</text>
</svg>

```python
def count_negatives(grid):
    n = len(grid[0])
    ans, j = 0, n - 1        # j：当前行最后一个非负数
    for row in grid:
        while j >= 0 and row[j] < 0:
            j -= 1           # 分界只会左移，不回头
        ans += n - 1 - j
    return ans
```

**复杂度。** 时间 `O(m+n)`，空间 `O(1)`。

**易错点。**
- 每行把 `j` 重置为 `n-1`：退化成 `O(mn)`，丢掉了列有序这条信息。
- 判断写成 `row[j] <= 0`：`0` 不是负数。

**追问。**
- 只有行有序？：每行二分第一个负数，`O(m log n)`。
- 找某个目标值？：同样从右上角出发，大了左移、小了下移，就是 LC 240。

**同模式。** LC 240 搜索二维矩阵 II、LC 74 搜索二维矩阵、LC 1337 矩阵中战斗力最弱的 K 行
