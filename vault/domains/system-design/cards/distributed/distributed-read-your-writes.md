---
id: distributed-read-your-writes
node: distributed.consistency
type: qa
---
## Q
A user saves their profile, refreshes, and sees the old version (read hit a lagging replica). Name the missing guarantee and three ways to provide it without making all reads strong.

## A
**Read-your-writes (read-after-write) consistency** — a session-level guarantee, weaker than linearizability.

- **Route the writer's reads to the leader** for data they may have modified (or for N seconds after their last write).
- **Session token / monotonic timestamp**: client carries the LSN/version of its last write; a replica serves the read only if it has caught up to it (else wait or forward).
- **Client-side echo**: update local/app cache with the written value and serve the user's own view from it.

Scope it to the session — other users seeing the update a second late is usually fine.

## Q zh
一个用户保存了他的资料，刷新页面后看到的却是旧版本（读命中了一个延迟的副本）。说出缺失的那个保证，以及三种能提供它、又不必让所有读都变强一致的办法。

## A zh
**Read-your-writes（写后读一致性）**——一种会话级别的保证，比线性一致性弱。

- **把写入者自己的读路由到 leader**（针对他们可能修改过的数据，或者在他们最后一次写入之后的 N 秒内）。
- **会话 token / 单调时间戳**：客户端携带自己最后一次写入的 LSN/版本号；只有当某个副本已经追上这个版本时才由它提供这次读（否则等待或转发）。
- **客户端侧回显**：用刚写入的值更新本地/应用缓存，用户自己的视图就从这个缓存提供。

把范围限定在会话级别就够了——其他用户晚一秒看到这次更新通常没问题。
