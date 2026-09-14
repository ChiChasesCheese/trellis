---
id: leetcode-q-valid-sudoku-pattern
node: dp-grid-interval-string.matrix
type: qa
anki: 1788391210999
tags: [lc::36, leetcode, pattern, recall]
---
## Q
如何判断一个 9x9 数独局部（行/列/3x3宫）是否合法？

## A
用三组 defaultdict(set)：rows[i]、cols[j]、secs[(i//3,j//3)]。遍历所有格子(i,j)，跳过'.'；若当前数字已存在于对应 row/col/sec 的 set 中则不合法，否则将该数字加入三个 set。时间复杂度 O(81)，用宫索引 (i//3, j//3) 是关键技巧。

**Evidence**

My Solution 代码使用 defaultdict(set) 分别追踪 rows、cols、secs，并用 sec = (i // 3, j // 3) 计算 3x3 宫索引

[原文 ↗](obsidian://open?vault=lc&file=questions%2F36%20-%20Valid%20Sudoku)
