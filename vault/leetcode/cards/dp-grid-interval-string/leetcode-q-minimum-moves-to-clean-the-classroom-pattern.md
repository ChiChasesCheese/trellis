---
id: leetcode-q-minimum-moves-to-clean-the-classroom-pattern
node: dp-grid-interval-string.matrix
type: qa
anki: 1788391211799
tags: [lc::3568, leetcode, pattern, recall]
---
## Q
网格中要收集若干目标点（用bitmask记录进度），且存在有限资源随移动消耗、特定格子可重置资源，求收集完所有目标的最少步数——该用什么状态设计做BFS？

## A
状态扩展为 (位置, 已收集目标的bitmask, 剩余资源)。每层BFS步数+1，转移时：踩到普通格资源-1，踩到重置格资源恢复满值，踩到目标格则bitmask或上对应位；用dict记录每个(位置,bitmask)组合下见过的最大剩余资源，只有当新状态的剩余资源严格更多时才允许入队（同一位置+同一收集进度，资源少的分支必被资源多的分支支配，直接剪掉）；一旦新bitmask等于全集，当前步数即为答案。资源耗尽(e==0)的状态不再扩展。

**Evidence**

best.get((ni, nj, nmask), -1) >= ne: continue；nmask == full: return step；ne = e - 1 if ch != 'R' else energy

[原文 ↗](obsidian://open?vault=lc&file=questions%2F3568%20-%20Minimum%20Moves%20to%20Clean%20the%20Classroom)
