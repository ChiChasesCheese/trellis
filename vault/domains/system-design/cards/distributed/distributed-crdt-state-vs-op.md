---
id: distributed-crdt-state-vs-op
node: distributed.crdt
type: qa
---
## Q
State-based vs operation-based CRDTs — what does each ship over the network, and what does each demand from the delivery channel?

## A
- **State-based (CvRDT)**: ship the whole state (or a **delta**) and merge. Demands almost nothing from the network — duplicates, reordering, and lost messages are all fine (idempotent merge + gossip retries) — but full states get big, hence delta-CRDTs.
- **Operation-based (CmRDT)**: ship each operation once; concurrent ops must commute. Cheaper on the wire but demands **reliable, exactly-once, causally ordered delivery** — a duplicated increment double-counts, a remove arriving before its add corrupts state — so you need a causal broadcast layer per replica pair.

Rule of thumb: gossip/edge sync with flaky links → state/delta-based; a sync engine already maintaining ordered per-peer logs (Automerge, Yjs-style) → op-based.

## Q zh
状态型（state-based）和操作型（operation-based）CRDT——各自在网络上传输什么？各自对传输通道有什么要求？

## A zh
- **状态型（CvRDT）**：传输整个状态（或者一个**delta**）然后合并。对网络几乎没有要求——消息重复、乱序、丢失都没关系（幂等合并 + gossip 重试）——但完整状态会很大，这也是为什么会有 delta-CRDT。
- **操作型（CmRDT）**：每个操作只传输一次；并发的操作必须满足可交换性。在带宽上更省，但要求**可靠、恰好一次、按因果顺序投递**——一次重复的递增会导致双计，一个 remove 先于它的 add 到达会破坏状态——所以每一对副本之间都需要一层因果广播机制。

经验法则：链路不稳定的 gossip/边缘同步 → 用 state/delta-based；已经维护了按对等方排序日志的同步引擎（Automerge、Yjs 一类）→ 用 op-based。
