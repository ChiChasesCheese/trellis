---
id: bagu-fencing-token-1-reject-stale
node: b.distributed.fencing-token
type: qa
step: 1
---
## Q
**Fencing Token · 租约之外为什么还要令牌**｜追问

面试官：「Leader 选举已经加了租约，为什么还要 fencing token？三个实例的定时任务，怎么保证只有一个在执行？」

## A
**基本回答。** 租约只能让失联持有者的资格过期，管不住它停顿后醒来继续写。fencing token 是每次获得权限时递增的号：写资源必须带上，资源端记住见过的最大号，拒绝更小的。校验在资源端做，光生成号没有用。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 252">
<rect x="15" y="6" width="70" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50.0" y="22.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A</text>
<rect x="135" y="6" width="70" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="22.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B</text>
<rect x="250" y="6" width="80" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="290.0" y="22.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">资源端</text>
<line x1="50" y1="30" x2="50" y2="238" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="170" y1="30" x2="170" y2="132" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="290" y1="30" x2="290" y2="238" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="50" y="52" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">拿到 token=10</text>
<text x="6" y="74" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">停顿，租约过期</text>
<text x="170" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">拿到 token=11</text>
<line x1="170" y1="126" x2="288" y2="126" stroke-width="1.2" stroke="currentColor"/>
<polygon points="288.0,126.0 281.0,129.2 281.0,122.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="230" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写 token=11 ✓</text>
<text x="334" y="148" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">记住最大号：11</text>
<text x="50" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">醒来</text>
<line x1="50" y1="190" x2="288" y2="190" stroke-width="1.2" stroke="currentColor"/>
<polygon points="288.0,190.0 281.0,193.2 281.0,186.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="184" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">带 token=10 写入</text>
<line x1="288" y1="214" x2="52" y2="214" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<polygon points="52.0,214.0 59.0,210.8 59.0,217.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="208" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">拒绝：10 &lt; 11 ✗</text>
<text x="8" y="244" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">比较与更新必须在资源端原子完成</text>
</svg>
A 拿到 token=10 后停顿，租约过期；B 拿到 11 并写入，资源端记住 11；A 醒来带着 10 来写，资源端发现 10 < 11，拒绝。
**容易错。**
- **以为有租约就够了：** 持有者可能刚好长时间 GC 停顿，自己不知道租约（lease，限时授权）已过期，醒来接着写；租约只能回收资格，拦不住这笔迟到的写，要靠 token 在资源端拒绝。
- **只生成 token 不校验：** 资源端不比较，号再大也没用。
- **先查后写：** 比较和更新不是一步，两个请求仍可能交叉，要用一条条件语句：`UPDATE t SET v = ?, token = ? WHERE id = ? AND token < ?`，影响行数 0 即被拒绝。
- **以为 Redis 锁天然带 token：** ZooKeeper 有 zxid 或 znode 版本，etcd 有 revision，Redis 没有，要每次加锁自己 INCR，主从切换后计数可能回退；资源端也要能条件写，不支持就不适合承担正确性型的锁。

**业务场景。** 每日对账任务的旧 Leader 因长时间停顿失去租约，醒来仍往结果表写；结果表带 token 字段，旧号写入被拒绝。
