---
id: distributed-quorum-not-linearizable
node: distributed.consistency
type: qa
---
## Q
Dynamo-style store, N=3, W=2, R=2 — strict quorums, no sloppiness. Why are reads still not linearizable?

## A
A write lands on replicas **one at a time**, and reads can interleave with the partial write: reader 1's quorum includes an updated replica and returns the new value; a *later* reader 2's quorum hits two not-yet-updated replicas and returns the **old** value — new-then-old violates linearizability even though both quorums were valid.

To fix it, a reader must **synchronously read-repair** the new value to a write quorum before returning, and writers must read the latest state before writing — expensive, and LWW conflict resolution breaks it anyway. That's why quorum overlap gives you "reads see *acknowledged* writes", not linearizability ([[distributed-quorum-math]]).

## Q zh
Dynamo 风格的存储，N=3、W=2、R=2——严格 quorum，没有 sloppy。为什么读仍然不是线性一致的？

## A zh
一次写是**一个一个地**落到各个副本上的，而读可以和这个未完成的写过程交错：读者 1 的 quorum 包含了一个已更新的副本，返回了新值；而*之后*的读者 2 的 quorum 恰好命中了两个还没更新的副本，返回了**旧**值——先新后旧违反了线性一致性，即便这两次 quorum 都是有效的。

要修复这个问题，读者必须在返回之前**同步地把新值 read-repair 到一个写 quorum**，写者也必须在写之前先读到最新状态——代价很高，而且 LWW 冲突解决方式无论如何都会破坏它。这就是为什么 quorum 重叠给你的只是"读能看到*已确认*的写"，而不是线性一致性（[[distributed-quorum-math]]）。
