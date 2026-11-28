---
id: bagu-redlock-4-choose
node: a.distributed.redlock
type: qa
step: 4
---
## Q
**效率型与正确性型 · 怎么选型**｜必会

面试官：「那你的系统里，分布式锁到底该怎么选？」

## A
**基本回答。** 先问「重复执行的代价是什么」。效率型（偶尔重复无所谓，如重复发通知、重复计算缓存）：单实例 Redis 锁加合理 TTL 就够，RedLock 过重。正确性型（重复会造成资金或数据错误）：用 ZooKeeper 或 etcd 这类有共识算法的系统加 fencing token，或者把正确性交给数据库约束与幂等。业界实践里，RedLock 用得并不多。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<rect x="60" y="8" width="220" height="34" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="29" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">重复执行的代价是什么？</text>
<line x1="130" y1="42" x2="91.1" y2="79.2" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86,84 88.9,76.9 93.3,81.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="210" y1="42" x2="248.9" y2="79.2" stroke-width="1.2" stroke="currentColor"/>
<polygon points="254,84 246.7,81.5 251.1,76.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="34" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">小</text>
<text x="306" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">大</text>
<rect x="6" y="84" width="160" height="84" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="107.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">偶尔重复无所谓</text>
<text x="86" y="122.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">重发通知、重算缓存</text>
<text x="86" y="137.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">→ 单实例 Redis 锁</text>
<text x="86" y="152.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+ 合理 TTL</text>
<rect x="174" y="84" width="160" height="84" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="254" y="107.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">重复会造成资金错误</text>
<text x="254" y="122.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">→ ZooKeeper / etcd</text>
<text x="254" y="137.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+ fencing token</text>
<text x="254" y="152.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">或 数据库约束+幂等</text>
<rect x="6" y="186" width="328" height="50" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="170" y="207.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">RedLock 多数情况不值得：</text>
<text x="170" y="222.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">多倍实例，却解决不了时钟与暂停</text>
</svg>
从顶部的问题出发，代价小走左边，用单实例 Redis 锁；代价大走右边，用共识系统加 fencing token，或交给数据库。底下的虚线框说明为什么 RedLock 夹在中间两头不讨好。
**容易错。**
- **一上来就问用 Redis 还是 ZooKeeper：** 先问重复执行的代价。
- **把资金安全全押在锁上：** 锁会过期、会丢，要有数据库约束兜底。
- **觉得 RedLock 比单实例锁就安全了：** 它多付出了实例和往返，却解决不了时钟与进程暂停，也没有 fencing。
- **正确性型场景还只用 Redis 锁：** 主从切换丢锁、TTL 到期后的进程暂停，都会出现两个持有者。

