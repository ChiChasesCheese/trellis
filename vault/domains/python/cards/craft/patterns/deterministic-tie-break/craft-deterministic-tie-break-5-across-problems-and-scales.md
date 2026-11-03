---
id: craft-deterministic-tie-break-5-across-problems-and-scales
node: craft.patterns.deterministic-tie-break
type: qa
step: 5
---
## Q
**确定性平局规则 · Top K 高频词、库存分配、等位选桌、任务调度、文件监视里的同一个习惯**｜模式

这些问题都会遇到"几个候选一样好"。它们各自怎么破平局？为什么分布式系统比单机更在乎这件事？

## A
**要点。** 同一个习惯：只要选择可能出现并列，就把平局规则**显式写进排序键**，让结果成为输入内容的纯函数，而不是迭代顺序、哈希、线程调度的副产品。

```python
# LeetCode 692 Top K Frequent Words：频次降序，并列按字典序
heapq.nsmallest(k, counts, key=lambda w: (-counts[w], w))
# inventory-management：余量多的仓库先，并列按仓库名
sorted(slots, key=lambda item: (-item[1].free, item[0]))
# restaurant-waitlist：最小的桌子，并列取编号小的
min(((sizes[t], t) for t in free if sizes[t] >= size), default=None)
# amz-dag-runner：同时就绪的节点按首次出现序号
ready = [self._index[n] for n, c in waiting.items() if c == 0]
```

以上各题的代码是节选：省略了类型标注、文档字符串和 `...` 处的细节，个别行为讲解而合并成一行，不是逐字摘抄。

**见于。** top-k-frequent-words、inventory-management、restaurant-waitlist、amz-dag-runner、notification-service、amz-file-watcher。

**不变的。** 键是元组，主标准在前，平局规则在后；方向相反的项取负；输出前对来自集合的数据排序。**变化的。** 平局规则的业务含义：字典序、编号小优先、先来后到、最少使用。

**信号。** 需求里出现"如果有多个……""并列时……""结果顺序要可预测""测试偶尔失败"；代码里把集合或 `dict.keys()` 的结果直接返回或遍历后输出。

**尺度对照。** 力扣：排序键里写全并列规则（评测器要求唯一答案）。低层设计：全序键，测试可断言整条序列。分布式：复制状态机（多个副本各自执行同样的日志）要求每个副本做出完全相同的选择，所以选择必须是输入的确定函数，不能依赖哈希盐、时钟或遍历顺序；选主时用"节点编号小者胜"打破平局；一致性哈希在两个节点得分相同时也要有固定的破平规则。变化：单机里不确定只是让测试偶尔失败，多副本里不确定会让副本悄悄分叉，而分叉往往要很久之后才被发现。
