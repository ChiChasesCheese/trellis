---
id: async-rebalancing-protocols
node: async.log
type: qa
---
## Q
A consumer group of 50 members hiccups every deploy: all consumption stops for seconds. What causes the pause, and what are the modern mitigations?

## A
**Eager rebalancing** is stop-the-world: any membership change makes *every* member revoke *all* partitions, rejoin, and wait for reassignment — a full pause plus state-reload for stateful consumers.

Mitigations:
- **Incremental cooperative rebalancing**: only partitions that actually move are revoked; everyone else keeps consuming through the rebalance.
- **Static membership** (`group.instance.id`): a restarting member reclaims its old partitions within the session timeout with **no rebalance at all** — built for rolling deploys.
- KRaft-era **KIP-848 broker-coordinated protocol**: assignment computed server-side, per-member incremental updates, no global sync barrier.

## Q zh
50 个成员的 consumer group 在每次部署时打嗝：所有消费停止几秒。什么导致暂停，现代缓解方法是什么？

## A zh
**Eager rebalancing** 是停全世界：任何成员变化使*每个*成员撤销*所有* partition，重新加入，等待重新分配 — 完整暂停加上有状态 consumer 的状态重加载。

缓解方法：
- **增量合作 rebalancing**：只有实际移动的 partition 被撤销；其他人通过 rebalance 继续消费。
- **静态成员**（`group.instance.id`）：重启的成员在 session timeout 内不经过任何 rebalance 就**reclaim 旧 partition** — 为滚动部署而生。
- KRaft 时代**KIP-848 broker 协调协议**：分配在服务器端计算，per-member 增量更新，无全局同步屏障。
