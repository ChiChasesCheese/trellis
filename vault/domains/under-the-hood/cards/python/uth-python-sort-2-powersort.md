---
id: uth-python-sort-2-powersort
node: python.sort
type: qa
step: 2
---
## Q
**该先归并哪两个 run**｜Python · CPython 3.11 起

Timsort 把数据切成许多 run 压进一个栈，什么时候合并、先合并哪两个？3.11 改了什么？

## A
**结构。** 待合并的 run 放在栈里；发现新 run 时先合并栈顶相邻的 run，再入栈。

**细节。**

- 3.10 及以前的规则基于斐波那契式的不变式；研究者做机器证明时发现它并不总成立。
- 3.11 起换成 Powersort（Munro 与 Wild）：给 run 算 power，即它在一棵想象的二叉归并树里的深度。
- 栈里 power 严格递减，深度更大的相邻 run 先合并。

**为什么。** 相当于用近似最优二叉搜索树决定合并顺序，对任意 run 长度分布都近似最优，规则也简单。

**对应 LeetCode：** LC 23 合并 K 个升序链表 · LC 21 合并两个有序链表
