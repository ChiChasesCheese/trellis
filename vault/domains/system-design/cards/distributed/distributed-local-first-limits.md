---
id: distributed-local-first-limits
node: distributed.crdt
type: qa
---
## Q
A local-first app (Automerge/Yjs-style) writes to the local replica and syncs in the background. What does the server shrink to, and which requirements force real server-side logic back in?

## A
The server shrinks to a **dumb relay + durable store of encrypted ops/states** — it never resolves conflicts, because CRDT merge runs on every client; clients get zero-latency writes, offline operation, and multi-device sync for free ([[distributed-multi-leader-fit]]: this is multi-leader with merge by construction).

Forced back to a coordinating server (or consensus):

- **Global invariants**: unique usernames, seat sold once, balance ≥ 0 — CRDTs converge but can't enforce "at most one".
- **Authoritative side effects**: payments, emails — must happen exactly once, somewhere.
- **Metadata growth**: tombstones/edit history need compaction, and text CRDTs pay per-character metadata.

Interview line: CRDTs remove coordination from *data merging*, not from *invariants*.

## Q zh
一个本地优先（local-first）应用（Automerge/Yjs 风格）写到本地副本，然后在后台同步。服务器缩小成了什么？哪些需求会把真正的服务器端逻辑逼回来？

## A zh
服务器缩小成了一个**傻瓜式中继 + 加密后的操作/状态的持久存储**——它从不解决冲突，因为 CRDT 合并在每个客户端上运行；客户端因此免费获得零延迟写入、离线可用、多设备同步（[[distributed-multi-leader-fit]]：这就是通过构造实现合并的多主复制）。

会把逻辑逼回一个协调服务器（或共识）的情况：

- **全局不变量**：唯一的用户名、一个座位只卖一次、余额 ≥ 0——CRDT 能收敛，但没法强制"至多一个"。
- **权威性的副作用**：支付、发邮件——必须在某处恰好发生一次。
- **元数据增长**：墓碑/编辑历史需要压缩，文本类的 CRDT 要为每个字符付出元数据代价。

面试要点：CRDT 把协调从*数据合并*中拿掉了，但没有把它从*不变量*中拿掉。
