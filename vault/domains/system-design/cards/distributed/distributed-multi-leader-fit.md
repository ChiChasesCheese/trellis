---
id: distributed-multi-leader-fit
node: distributed.replication.multi-leader
type: qa
---
## Q
When is multi-leader replication the right call despite its conflict problem, and what are the main conflict-resolution options?

## A
Right call when writes must be accepted in **multiple locations independently**: multi-region apps writing locally (cross-region RTT too high for one leader), offline-capable clients (calendar/notes apps), collaborative editing.

Conflicts are inherent — the same key can be written concurrently on two leaders:
- **LWW (last-write-wins)** — simple, but silently drops one write and trusts clocks.
- **CRDTs / mergeable types** — counters, sets, text that merge deterministically.
- **App-level resolution** — keep siblings and merge on read, or route conflicts to custom logic.

Best mitigation: partition so each record has a **home leader** (e.g. user's region), making conflicts rare by construction.

## Q zh
在什么情况下多主复制是正确选择（尽管有冲突问题）？主要冲突解决选项是什么？

## A zh
当必须在**多个位置独立接受**写入时才是正确选择：多地区应用本地写入（跨地区 RTT 太高以至于无法用单主），离线无能力的客户端（日历/笔记应用），协作编辑。

冲突是固有的 — 同一个 key 可以在两个主上并发写入：
- **LWW（last-write-wins）** — 简单，但静默丢弃一个写入并信任时钟。
- **CRDTs / 可合并类型** — 计数器、集合、文本能确定性合并。
- **应用级解决** — 保存兄弟版本在读时合并，或路由冲突到自定义逻辑。

最佳缓解：分区使每条记录有**主页主**（如用户的地区），这样通过构造使冲突变稀少。
