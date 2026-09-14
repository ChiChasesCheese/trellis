---
id: distributed-fencing-tokens
node: distributed.consensus
type: qa
---
## Q
A client holds a distributed-lock lease, pauses for a 20s GC, then resumes and writes — but its lease expired and another client took the lock. How do fencing tokens prevent the corruption, and why can't the client fix this itself?

## A
The lock service issues a **monotonically increasing token** with every lock grant. The *protected resource* (storage) records the highest token it has seen and **rejects writes carrying a lower token** — so the paused client's stale-token write bounces.

The client can't fix it alone: it cannot atomically "check lease still valid, then write" — arbitrary pauses (GC, page fault, network delay) can strike **between** the check and the write. Safety must be enforced at the resource. Corollary: a lock/lease without downstream fencing checks is only advisory, never a safety mechanism.

## Q zh
一个客户端持有一个分布式锁的租约，暂停了 20 秒（GC 导致），恢复后继续写入——但它的租约早已过期，另一个客户端已经拿到了锁。fencing token 是怎样防止数据损坏的？为什么客户端自己没法解决这个问题？

## A zh
锁服务在每次授予锁时都会签发一个**单调递增的令牌**。*受保护的资源*（存储层）记录它见过的最大令牌，并**拒绝携带更小令牌的写入**——于是那个暂停过的客户端带着过期令牌的写入就会被弹回。

客户端自己没法解决这个问题：它无法原子地做到"先检查租约仍然有效，再写入"——任意的暂停（GC、缺页、网络延迟）都可能发生在检查和写入**之间**。安全性必须在资源这一端强制执行。推论：一个没有下游 fencing 检查的锁/租约只是一种建议性机制，永远不是安全机制。
