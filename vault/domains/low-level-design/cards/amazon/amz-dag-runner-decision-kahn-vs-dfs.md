---
id: amz-dag-runner-decision-kahn-vs-dfs
node: amazon.amz-dag-runner
type: qa
step: 5
tags: [grown]
---
## Q
在 Amazon DAG 执行器里，拓扑排序选 Kahn 算法还是 DFS 后序？各自代价是什么？

## A
DFS 后序：代码短，遇到灰色节点即环；但 Python 递归默认深度约 1000，长依赖链会 RecursionError，改显式栈就不短了，平局顺序也难规定。Kahn：迭代无栈深问题，且「就绪节点集合」正好是第 4 关并行调度需要的概念，两关共用入度表；代价是卡住后要另外找环。选 Kahn。
