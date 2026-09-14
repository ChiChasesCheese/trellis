---
id: leetcode-q-stone-game-v-mistake
node: dp-game-probability.game-theory
type: qa
anki: 1787102794960
tags: [lc::1563, leetcode, mistake, recall]
---
## Q
在 Stone Game V 的 L[l][l]、R[l][l] 初始化时，容易把它们错写成什么？为什么是错的？

## A
容易错写成 0。因为 f[l][l]（长度为1的区间，游戏已结束）确实是 0，但 L[l][l]、R[l][l] 存的不是 f 值本身，而是“这一段的 sum + f”，即单独一块石头的价值 stoneValue[l]。若误设为 0，会导致所有单块候选值凭空消失，后续查表结果偏小。

**Evidence**

代码注释：“长度为 1 的区间：f 已经是 0（游戏结束，拿不到分），但 L/R 不是 0 —— 它俩存的是「这一段的 sum + f」，即 stoneValue[l]。这里最容易写错成 0，然后所有单块候选凭空消失。”

[原文 ↗](obsidian://open?vault=lc&file=questions%2F1563%20-%20Stone%20Game%20V)
