---
id: amz-dag-runner-code-review-duplicate-edge-indegree
node: amazon.amz-dag-runner
type: qa
step: 7
tags: [grown]
---
## Q
在 Amazon DAG 执行器的代码评审练习里，入度用 len(ds) 数，后继表却用 set(ds) 建，会出什么错？给出具体输入。

## A
输入 {"a": ["b", "b"], "b": []}：a 的入度被数成 2，但 b 完成时只通知 a 一次，入度停在 1，a 永远不就绪，输出 ['b'] 而不是 ['b', 'a']，且不报错。修法：建图时用集合去重，入度取 len(集合)，入度与后继表来自同一份数据。同类 bug 还有：只出现在依赖里的节点不入队；排完不核对数量，环被吞成空列表。
