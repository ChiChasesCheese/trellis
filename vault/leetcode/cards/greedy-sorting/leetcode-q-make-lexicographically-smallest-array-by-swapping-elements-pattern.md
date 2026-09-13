---
id: leetcode-q-make-lexicographically-smallest-array-by-swapping-elements-pattern
node: greedy-sorting.sorting
type: qa
anki: 1788391211300
tags: [lc::2948, leetcode, pattern, recall]
---
## Q
遇到「若两元素满足某条件（如差值 ≤ limit）则可以交换」这类题目，如何设计算法？

## A
先问自己：这个「可交换」关系是否具有传递性？如果是，说明这本质是一个图的连通性问题：
1. 将满足条件的元素视为连通块（可用并查集，或排序后利用「相邻差 ≤ limit」的性质做一次线性扫描来划分连续区间）；
2. 由于相邻交换可以生成块内任意排列，同一连通块内的元素可以自由重排；
3. 对每个连通块内部按贪心策略重排（如排序后依次填回原位置），从而得到全局最优解（如字典序最小）。
该模式可复用于同类题目，例如 1202. Smallest String With Swaps（直接给出 pairs，图结构更明显）。

**Evidence**

题解注释："交换的传递性...这是个图的连通性问题"；"排序后连通块 = 连续区间...只需一次线性扫描"；"块内任意排列（相邻交换生成全排列）"；"以后看到「可以交换满足某条件的元素」，第一反应就问自己「这个关系传递吗？」传递 → 并查集 / 连通块 → 块内自由重排 → 贪心"。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F2948%20-%20Make%20Lexicographically%20Smallest%20Array%20by%20Swapping%20Elements)
