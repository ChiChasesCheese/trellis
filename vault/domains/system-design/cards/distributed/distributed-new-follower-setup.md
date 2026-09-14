---
id: distributed-new-follower-setup
node: distributed.replication.leader
type: qa
---
## Q
You need to add a new follower to a busy single-leader database without stopping writes. Copying the data files while the leader keeps writing yields a torn, inconsistent copy — what is the standard procedure, and what does it demand from the leader's log?

## A
- **Snapshot at a known log position**: take a consistent snapshot of the leader that is tagged with an exact position in the replication log (Postgres LSN, MySQL binlog coordinates/GTID). Tools like `pg_basebackup` do this without blocking writes.
- **Restore, then replay the delta**: load the snapshot on the new node, connect to the leader, and request every change *since that position*; once the backlog is drained the node is a normal follower.
- **The demand on the leader**: it must retain log segments back to the snapshot position for the whole snapshot-copy-catchup window — if they were purged, you re-seed from scratch.
- Same mechanism handles a **crashed follower rejoining**: it remembers the last position it applied and streams only the gap. Replication is resumable precisely because every change has a durable position in an ordered log.

## Q zh
你要给一个写入繁忙的单主数据库加一个新 follower，且不能停写。在 leader 持续写入时直接拷贝数据文件会得到一份撕裂的、不一致的副本——标准做法是什么？它对 leader 的日志有什么要求？

## A zh
- **在已知日志位点做快照**：对 leader 做一份一致性快照，并且这份快照要绑定复制日志中的精确位置（Postgres 的 LSN、MySQL 的 binlog 坐标/GTID）。`pg_basebackup` 这类工具可以在不阻塞写入的情况下完成。
- **恢复快照，再回放增量**：把快照装载到新节点上，连上 leader，请求*从那个位点开始*的所有变更；追平积压之后，它就是一个普通 follower。
- **对 leader 的要求**：leader 必须把日志段保留到快照位点，覆盖整个"快照—拷贝—追赶"窗口——如果需要的日志段已被清理，就只能从头重新做种。
- 同一套机制也处理 **崩溃后重新加入的 follower**：它记得自己最后应用到的位点，只需补齐缺口。复制之所以可断点续传，正是因为每个变更在有序日志里都有一个持久的位置。
