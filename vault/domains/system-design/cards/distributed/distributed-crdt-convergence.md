---
id: distributed-crdt-convergence
node: distributed.crdt
type: qa
---
## Q
What algebraic properties must a CRDT's merge function have, and what operational freedoms do those properties buy?

## A
Merge must be **commutative** (order doesn't matter), **associative** (grouping doesn't matter), and **idempotent** (merging the same state twice is harmless) — formally, states form a join-semilattice and merge is the least-upper-bound.

That buys: replicas can accept writes **independently with no coordination**, sync **in any order, over any topology, with duplicated or re-sent messages**, and still provably converge to the same state once they've seen the same updates. Conflicts are resolved *by construction* rather than detected and escalated.

The catch: convergence ≠ correctness — the merged result is whatever the type's semantics say (e.g. add-wins), which may not be what the business rule wanted.

## Q zh
CRDT 的合并函数必须具备哪些代数性质？这些性质换来了哪些操作上的自由？

## A zh
合并必须是**交换的**（顺序无关）、**结合的**（分组无关）、**幂等的**（对同一状态合并两次也没有影响）——形式化地说，状态构成一个 join-半格（join-semilattice），合并就是取最小上界（least-upper-bound）。

这换来的是：副本可以**完全不经协调、独立地接受写入**，可以**以任意顺序、经由任意拓扑同步，消息重复或重发也没关系**，并且一旦看到相同的更新集合就能被证明收敛到同一状态。冲突是*由构造保证*被解决的，而不是先检测再上报处理。

要注意：收敛不等于正确——合并出来的结果是这个类型的语义所决定的（例如 add-wins），而这未必是业务规则真正想要的。
