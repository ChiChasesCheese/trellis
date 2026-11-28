---
id: lct-learn-sliding-window-3-6
node: sliding-window.3.6
type: qa
step: 1
---
## Q
**滑动窗口与双指针 › 单序列双指针 › 矩阵上的双指针**｜学习卡

套路是什么？

## A
**一句话。** 行列都递增的矩阵里，右上角是所在行的最大、所在列的最小：与目标比一次就排除一整行或一整列，指针只往左或往下，`O(m+n)`。

下图：LC 240，右上角是行最大、列最小，每比一次排除一整行或一整列。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 175">
<rect x="20" y="20" width="40" height="36" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="40" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="60" y="20" width="40" height="36" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="80" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">4</text>
<rect x="100" y="20" width="40" height="36" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="120" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">7</text>
<rect x="140" y="20" width="40" height="36" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="160" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">11</text>
<rect x="20" y="56" width="40" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="40" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="60" y="56" width="40" height="36" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="80" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">5</text>
<rect x="100" y="56" width="40" height="36" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="120" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">8</text>
<rect x="140" y="56" width="40" height="36" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="160" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">12</text>
<rect x="20" y="92" width="40" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="40" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="60" y="92" width="40" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="100" y="92" width="40" height="36" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="120" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">9</text>
<rect x="140" y="92" width="40" height="36" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="160" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">16</text>
<rect x="20" y="128" width="40" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="40" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10</text>
<rect x="60" y="128" width="40" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">13</text>
<rect x="100" y="128" width="40" height="36" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="120" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">14</text>
<rect x="140" y="128" width="40" height="36" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="160" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">17</text>
<text x="195" y="34" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">target = 5，从右上角出发</text>
<text x="195" y="58" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">11 &gt; 5：排除整列，左移</text>
<text x="195" y="76" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">7 &gt; 5：排除整列，左移</text>
<text x="195" y="94" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">4 &lt; 5：排除整行，下移</text>
<text x="195" y="112" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">5：找到</text>
<text x="195" y="140" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">虚框 = 已排除</text>
</svg>

```python
def search_matrix(matrix, target):  # LC 240
    row, col = 0, len(matrix[0]) - 1    # 右上角
    while row < len(matrix) and col >= 0:
        x = matrix[row][col]
        if x == target:
            return True
        if x > target:              # 本列 row 以下全 >= x，排除整列
            col -= 1
        else:                       # 本行 col 以左全 <= x，排除整行
            row += 1
    return False
```

**要点。**
- 为什么对？：右上角往左变小、往下变大，比较一次就能确定排除哪一边；左下角同理，左上和右下角则排除不了任何一边。
- 计数类变体怎么改？：把“找到”换成整列或整行计数（如 LC 1351 统计有序矩阵中的负数），走法不变。

**易错点。**
- 从左上角出发：`matrix = [[1,4],[2,5]]`、`target = 5`，`1 < 5` 往右往下都可能通向 `5`。
- 指针走反：`x > target` 应向左，`x < target` 应向下；`[[1,4,7],[2,5,8],[3,6,9]]`、`target = 5` 路径是 `7 → 4 → 5`。
- 空矩阵：`matrix = []` 或 `[[]]` 应返回 `False`，要先判断。

**对应题目。** LC 240 搜索二维矩阵 II
