---
id: distributed-lamport-vs-vector
node: distributed.time.clocks
type: qa
---
## Q
Lamport timestamps vs vector clocks: what question can a vector clock answer that a Lamport clock cannot, and what does that cost?

## A
**"Were these two events concurrent?"** Lamport clocks (single counter: bump on local event, take max+1 on receive) guarantee only one direction: A happened-before B ⇒ L(A) < L(B). The converse fails — L(A) < L(B) tells you nothing; the events may be concurrent.

Vector clocks (one counter per node) capture causality exactly: A → B iff V(A) ≤ V(B) elementwise; **incomparable vectors = concurrent** — which is what Dynamo-style stores need to detect conflicting siblings instead of silently ordering them.

Cost: O(number of nodes) per timestamp, carried on every message, and pruning entries of departed nodes is awkward. Use Lamport when you just need *some* total order; vectors when you must *detect* conflicts.

## Q zh
Lamport 时间戳和向量时钟——向量时钟能回答哪个 Lamport 时钟回答不了的问题？代价是什么？

## A zh
**"这两个事件是并发的吗？"** Lamport 时钟（单个计数器：本地事件时自增，收到消息时取 max+1）只能保证一个方向：A happened-before B ⇒ L(A) < L(B)。反过来不成立——L(A) < L(B) 什么都说明不了；这两个事件可能是并发的。

向量时钟（每个节点一个计数器）能精确捕捉因果关系：A → B 当且仅当 V(A) ≤ V(B)（逐元素比较）；**无法比较的向量 = 并发**——这正是 Dynamo 风格的存储用来检测冲突的兄弟版本、而不是悄悄给它们排序所需要的东西。

代价：每个时间戳的开销是 O(节点数)，要随每条消息一起携带，而且清理已离开节点的条目很麻烦。只需要*某种*全序时用 Lamport；必须*检测*冲突时用向量时钟。
