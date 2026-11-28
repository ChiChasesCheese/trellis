---
id: bagu-lock-zookeeper-1-ephemeral-sequential
node: b.distributed.lock-zookeeper
type: qa
step: 1
---
## Q
**ZooKeeper 锁 · 临时顺序节点、Watch 与集群角色**｜追问

面试官：「怎么用 ZooKeeper 实现分布式锁？为什么只监听前一个节点？ZooKeeper 里的 Leader、Follower、Observer 和 ZAB 是怎么回事？」

## A
**基本回答。** 在持久节点 `/locks` 下创建临时顺序节点（EPHEMERAL_SEQUENTIAL）。序号最小的拿到锁，其余的只在前一个节点上注册 Watch，前驱被删除时收到通知，再检查自己是不是最小。释放就是删节点；客户端崩溃，会话过期，节点自动消失，锁不会永久被占（Redis 靠 TTL 防死锁，这里靠会话）。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<rect x="80" y="6" width="180" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="170.0" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">/locks（持久节点）</text>
<rect x="10" y="48" width="140" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="80.0" y="66.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">lock-0000000000</text>
<rect x="190" y="48" width="140" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="260.0" y="66.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端 A：持有锁</text>
<line x1="150" y1="62" x2="190" y2="62" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<rect x="10" y="100" width="140" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80.0" y="118.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">lock-0000000001</text>
<rect x="190" y="100" width="140" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260.0" y="118.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端 B：等待</text>
<line x1="150" y1="114" x2="190" y2="114" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<rect x="10" y="152" width="140" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80.0" y="170.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">lock-0000000002</text>
<rect x="190" y="152" width="140" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260.0" y="170.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端 C：等待</text>
<line x1="150" y1="166" x2="190" y2="166" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="80" y1="32" x2="80" y2="48" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="60" y1="152" x2="60" y2="128" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="60.0,128.0 63.2,135.0 56.8,135.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="68" y="144" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">C 只盯 B</text>
<line x1="60" y1="100" x2="60" y2="76" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="60.0,76.0 63.2,83.0 56.8,83.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="68" y="92" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">B 只盯 A</text>
<text x="8" y="204" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">A 释放 → 只唤醒 B，不惊动 C</text>
<text x="8" y="224" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">A 崩溃 → 会话过期 → 节点自动消失</text>
</svg>
三个客户端各在 `/locks` 下建了一个带序号的节点，A 的序号最小所以持锁；B 只盯 A，C 只盯 B，A 释放时只有 B 被唤醒。
**容易错。**
- **以为所有人都监听锁节点：** 那样释放时全员被同时唤醒再争抢，是羊群效应（herd effect），大量请求打向 ZooKeeper；每人只盯前一个节点，每次只唤醒一个。
- **以为拿到通知就等于拿到锁：** 通知只说明前驱没了，醒来后要再检查自己是不是最小。
- **以为 Watch 会一直有效：** Watch 是一次性的，触发后要重新注册。
- **以为会话没断就绝对安全：** GC 停顿或网络分区可能让会话过期而旧客户端不知道，要加 fencing token。
- **以为 Observer 和 Follower 一样：** Observer 不投票，只扩读，不参与写的多数确认，所以再多也不拖慢写提交；Follower 越多要等的票越多。

**业务场景。** 定时结算任务部署 3 个实例只能一个执行：各实例创建临时顺序节点，序号最小的是主；主实例宕机，会话过期，下一个自动接任。
