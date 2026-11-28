---
id: bagu-lock-choice-1-redis-zk-db
node: b.distributed.lock-choice
type: qa
step: 1
---
## Q
**分布式锁选型 · Redis、ZooKeeper、数据库怎么选**｜追问

面试官：「Redis 锁、ZooKeeper 锁、数据库锁，你怎么选？乐观锁和悲观锁又怎么选？」

## A
**基本回答。** 先问「重复执行一次，代价是什么」。代价只是多发一条通知，用 Redis 锁，快，极小概率重复可接受；代价是重复扣款，必须用数据库唯一键或状态机条件更新兜底，锁只是优化；选主或要求互斥正确性，用 ZooKeeper / etcd：它们用共识协议（ZAB、Raft，多数节点确认才算数）保证抢锁结果所有人看到同一个，用临时节点或租约，持有者会话断开自动释放，临时顺序节点加 watch 天然公平；代价是每次写都过半数确认，吞吐比 Redis 低数倍到一个数量级。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 252">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">先问：重复执行一次，代价是什么？</text>
<rect x="6" y="30" width="130" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71.0" y="49.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">代价小</text>
<text x="71.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">多发一条通知</text>
<line x1="138" y1="52" x2="174" y2="52" stroke-width="1.2" stroke="currentColor"/>
<polygon points="174.0,52.0 167.0,55.2 167.0,48.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="176" y="30" width="158" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255.0" y="49.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis 锁</text>
<text x="255.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">快，极小概率重复可接受</text>
<rect x="6" y="92" width="130" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71.0" y="111.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">代价大</text>
<text x="71.0" y="126.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">重复扣款</text>
<line x1="138" y1="114" x2="174" y2="114" stroke-width="1.2" stroke="currentColor"/>
<polygon points="174.0,114.0 167.0,117.2 167.0,110.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="176" y="92" width="158" height="44" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="255.0" y="111.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">唯一键 / 条件更新兜底</text>
<text x="255.0" y="126.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">锁只是优化</text>
<rect x="6" y="154" width="130" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71.0" y="173.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">要选主</text>
<text x="71.0" y="188.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">或互斥必须正确</text>
<line x1="138" y1="176" x2="174" y2="176" stroke-width="1.2" stroke="currentColor"/>
<polygon points="174.0,176.0 167.0,179.2 167.0,172.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="176" y="154" width="158" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255.0" y="173.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ZooKeeper / etcd</text>
<text x="255.0" y="188.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">共识协议，线性一致</text>
<text x="8" y="224" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">能一条 UPDATE 解决的，就不用锁：</text>
<text x="8" y="242" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">SET count=count-1 WHERE count&gt;0</text>
</svg>
从上往下是三种代价：代价小用 Redis，代价大靠唯一键或条件更新兜底，要选主或互斥必须正确才用 ZooKeeper / etcd；最底下一行提醒：能用一条 UPDATE 解决的，根本不用锁。
**容易错。**
- **多实例一定要分布式锁：** 能用唯一键、条件更新解决的就不用锁。扣库存写 `UPDATE stock SET count = count - 1 WHERE sku_id = ? AND count > 0`，检查和扣减在一条语句里，影响行数 1 才成功，行锁已经排好队；库存只剩 1 时第二个请求影响行数 0，下单失败。
- **Redis 锁能保证正确性：** 主从切换会丢锁，TTL 到期也会让两个客户端同时持锁，它只是把重复概率降得很低。
- **RedLock 值得上：** 它多付出多倍实例和往返，仍解决不了时钟与进程暂停，也没有 fencing；效率型用单实例锁，正确性型用共识系统或数据库约束。
- **ZooKeeper 一定比 Redis 好：** 它更正确，但写吞吐低数倍到一个数量级，还要多运维一个集群。
- **乐观锁一定更快：** 冲突多时大家反复重试，反而浪费；冲突多的场景悲观锁更稳。

**业务场景。** 重复推送一条站内通知，Redis 锁足够；打赏扣款重复了就是真金白银，靠流水号唯一索引兜底。
