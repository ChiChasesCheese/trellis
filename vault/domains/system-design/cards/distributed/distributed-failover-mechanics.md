---
id: distributed-failover-mechanics
node: distributed.replication.leader
type: qa
---
## Q
Walk through automatic leader failover in leader-follower replication, and name the three classic hazards.

## A
Steps: **detect** leader death (heartbeat timeout), **elect** the most up-to-date follower as new leader, **reconfigure** so clients and followers point at it.

- **Lost writes**: with async replication the new leader may lack the old leader's last acknowledged writes; discarding them breaks anything that already consumed them (GitHub incident: reused auto-increment IDs made a Redis cache serve wrong users' data).
- **Split brain**: the old leader comes back still thinking it leads; without fencing/STONITH both accept writes and diverge.
- **Bad timeout choice**: too short → needless failovers exactly when the system is slow under load, making the outage worse; too long → longer downtime.

That's why teams often keep failover **manual** for the system of record.

## Q zh
走一遍主从复制中的自动 leader 故障转移，并说出三个经典的隐患。

## A zh
步骤：**检测** leader 死亡（心跳超时）、**选举**最新的 follower 作为新 leader、**重新配置**让客户端和 follower 都指向它。

- **写丢失**：在异步复制下，新 leader 可能缺少旧 leader 最后确认过的写入；丢弃这些写入会破坏任何已经消费过它们的东西（GitHub 的一次事故：复用的自增 ID 导致 Redis 缓存把数据提供给了错误的用户）。
- **脑裂（split brain）**：旧 leader 恢复后仍然以为自己是 leader；如果没有 fencing/STONITH，两边都会接受写入并各自分叉。
- **超时选择不当**：太短 → 恰好在系统因负载变慢时触发不必要的故障转移，让故障更严重；太长 → 停机时间更长。

这就是为什么很多团队对于系统记录（system of record）常常保留**手动**故障转移。
