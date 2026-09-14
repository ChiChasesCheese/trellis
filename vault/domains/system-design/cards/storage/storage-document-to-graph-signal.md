---
id: storage-document-to-graph-signal
node: storage.nosql
type: qa
---
## Q
Your data began as neat tree-shaped documents (user → orders → items). What change in the data's *shape* signals that a graph model now fits better than documents — and why can't documents absorb the change?

## A
The signal is **many-to-many connections proliferating**: entities start linking across trees (users referencing users, items shared by orders, organizations ↔ people ↔ events), and queries start caring about the *links themselves*, traversed in both directions.

Documents can't absorb this because a document is a **tree with one root**:

- A cross-tree link is just a stored ID — following it means another query, and the *reverse* direction ("who references me?") has no home at all without a hand-maintained mirror.
- Embedding instead of linking duplicates the shared entity into every parent, recreating update anomalies.

A graph model makes vertices and edges first-class and **homogeneous** — anything may connect to anything, new relationship types need no schema surgery. Rule of thumb: mostly one-to-many or no relationships → document; dense many-to-many → graph (simple, fixed-depth many-to-many still sits fine in relational — see [[storage-graph-db-fit]]).

## Q zh
你的数据一开始是整洁的树形文档（user → orders → items）。数据*形状*上出现什么变化，就说明 graph 模型比文档更合适了 — 为什么文档吸收不了这种变化？

## A zh
信号是**many-to-many 连接的激增**：实体开始跨树互相链接（用户引用用户、商品被多个订单共享、组织 ↔ 人 ↔ 事件），而且查询开始关心*链接本身*，并要双向遍历。

文档吸收不了这一点，因为文档是**只有一个根的树**：

- 跨树链接只是一个存下来的 ID — 沿着它走意味着再发一次查询，而*反向*（"谁引用了我？"）在不手工维护镜像的情况下根本无处安放。
- 用嵌入代替链接，会把共享实体复制进每个父节点，重新制造更新异常。

Graph 模型把顶点和边当作一等公民且**同质对待** — 任何东西可以连接任何东西，新的关系类型不需要动 schema。经验法则：以 one-to-many 或无关系为主 → 文档；稠密的 many-to-many → graph（简单、固定深度的 many-to-many 放在关系型里也没问题 — 见 [[storage-graph-db-fit]]）。
