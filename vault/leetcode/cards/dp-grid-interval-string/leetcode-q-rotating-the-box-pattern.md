---
id: leetcode-q-rotating-the-box-pattern
node: dp-grid-interval-string.matrix
type: qa
anki: 1787102261632
tags: [lc::1861, leetcode, pattern, recall]
---
## Q
行内重力模拟题（如 1861. Rotating the Box）：石头受重力下落、遇障碍物停住，如何用一次遍历模拟每一行的下落结果？

## A
从右往左扫描该行，维护一个 write 指针表示“下一个石头可以落到的最右空位”。遇到 '*' 时把 write 重置为 col-1（障碍物左侧）；遇到 '#' 时把该石头移到 write 位置（原地置为 '.'，write 位置置为 '#'），并 write -= 1；遇到 '.' 不做任何事。这是单行内的双指针/分组处理：以障碍物为分组边界，每组内石头整体“靠右堆叠”。时间复杂度 O(m*n)。旋转矩阵时再套用 90 度顺时针公式 res[j][m-1-i] = box[i][j]。

**Evidence**

```
for row in box:
    write = n - 1
    for col in range(n - 1, -1, -1):
        if row[col] == '*':
            write = col - 1
        elif row[col] == '#':
            row[col] = '.'
            row[write] = '#'
            write -= 1
```

[原文 ↗](obsidian://open?vault=lc&file=questions%2F1861%20-%20Rotating%20the%20Box)
