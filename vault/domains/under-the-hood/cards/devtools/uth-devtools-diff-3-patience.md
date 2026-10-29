---
id: uth-devtools-diff-3-patience
node: devtools.diff
type: qa
step: 3
---
## Q
**patience diff：先锚定唯一行**｜Git · diff-algorithm · 2.56

挪动一个函数后，默认 diff 有时把一堆 `}` 配错位置，`--patience` 为什么更好看？

## A
**结构。** patience：先找两个文件里各只出现一次的行，取它们配对后的最长递增子序列做锚点；锚点之间递归，没有唯一行的区间退回 Myers。

**细节。**

- 选项：`--diff-algorithm=myers|minimal|patience|histogram`，默认 `myers`
- `histogram` 是 patience 的扩展，支持“出现次数少”的行
- 唯一行（函数签名之类）比 `}`、空行更能代表“真正没变的代码”

**为什么。** Myers 只追求最少行数，不管可读性，大量重复的行会被随意配对；用唯一行当锚点，更符合人对“哪里没变”的直觉。

**对应 LeetCode：** LC 300 最长递增子序列 · LC 354 俄罗斯套娃信封问题
