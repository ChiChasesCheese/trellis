---
id: amz-linux-find-traversal-and-judgement-separate
node: amazon.amz-linux-find
type: qa
step: 5
tags: [grown]
---
## Q
在 Linux find 文件搜索设计里，为什么让 FileSearcher 外部遍历，而不是给每个节点加 search(filter) 方法递归搜索？

## A
两个选项：
- 节点上加 `search`：经典组合模式写法，但遍历策略（深度还是广度、跟不跟随链接、剪枝）被固化进每个节点类。
- 节点只是数据，遍历集中在 `FileSearcher.find`。

选后者：遍历策略正是面试官最爱追问的变化点，集中在一处，所有变化只影响一个类。

也不用访问者模式（Visitor）：这里只有一种操作，「对结果做什么」是调用方消费迭代器的事。
