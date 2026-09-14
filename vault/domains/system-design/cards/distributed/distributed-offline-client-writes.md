---
id: distributed-offline-client-writes
node: distributed.replication.multi-leader
type: qa
---
## Q
Why is an offline-capable mobile/desktop app a multi-leader system, and which two schema decisions does that force on you?

## A
Every device has a full local replica that **accepts writes while disconnected** and syncs later — that is exactly multi-leader, with the peculiar property that **replication lag is unbounded** (days, if the phone is in a drawer) and the "leader count" equals the user's device count.

Forced decisions:

- **Client-generated ids** (UUID/ULID, or `(device_id, local_seq)`) — server auto-increment ids can't be assigned offline, and two devices would mint the same one.
- **Mutations as intents, not absolute state** — store `add 2 to quantity` or a CRDT/OT operation rather than `quantity = 5`, so two devices' offline edits both survive the merge.

What stays impossible: **global invariants** (uniqueness, non-negative balance) cannot be checked offline, so those operations must be *provisional locally and confirmed by the server*, with a visible rollback path in the UI.

## Q zh
为什么一个支持离线的手机/桌面应用本质上是一个多主系统？这又强制你做出哪两个 schema 决策？

## A zh
每台设备都持有一份完整的本地副本，能在**断网时接受写入**，之后再同步——这正是多主复制，只是有一个特别之处：**复制延迟没有上界**（如果手机被扔在抽屉里，可能是几天），而"leader 的数量"就等于用户的设备数量。

被迫做出的决策：

- **客户端生成 id**（UUID/ULID，或 `(device_id, local_seq)`）——服务器的自增 id 没法在离线时分配，两台设备也会分配出同一个 id。
- **把变更记录为意图，而不是绝对状态**——存 "给 quantity 加 2" 或一个 CRDT/OT 操作，而不是 `quantity = 5`，这样两台设备各自的离线编辑才能在合并后都保留下来。

始终做不到的：**全局不变量**（唯一性、余额非负）没法离线校验，所以这类操作必须*在本地是临时性的，由服务器确认*，并且在 UI 上要有可见的回滚路径。
