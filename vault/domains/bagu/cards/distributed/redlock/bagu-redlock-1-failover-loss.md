---
id: bagu-redlock-1-failover-loss
node: a.distributed.redlock
type: qa
step: 1
---
## Q
**主从切换 · 单实例 Redis 锁为什么会丢**｜必会

面试官：「Redis 做了主从，主库挂了切到从库，分布式锁会失效吗？为什么？」

## A
**基本回答。** 会。客户端 A 在主库加锁成功，主库确认之后才异步复制给从库。主库在复制前宕机，从库升为新主，新主上没有这把锁，客户端 B 对同一资源加锁也成功，两个客户端同时持锁。
**一句话记住。** 主库是总经理，从库是秘书，加锁就是总经理在登记簿上写「会议室被 A 订了」。登记要稍后才抄给秘书；总经理刚写完就突然离职，秘书接班，登记簿里没有这条，B 来订，照样订成功了。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 244">
<rect x="6" y="14" width="68" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="40" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端 A</text>
<line x1="74" y1="32" x2="93" y2="32" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="100,32 93,35.2 93,28.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="100" y="14" width="90" height="36" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="145" y="28.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主库</text>
<text x="145" y="43.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">有这把锁</text>
<line x1="190" y1="32" x2="220" y2="32" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="220" y1="32" x2="223" y2="32" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="230,32 223,35.2 223,28.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="230" y="14" width="104" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282" y="28.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">从库</text>
<text x="282" y="43.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">没有这把锁</text>
<text x="170" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">复制前主库宕机</text>
<line x1="282" y1="50" x2="282" y2="93" stroke-width="1.2" stroke="currentColor"/>
<polygon points="282,100 278.8,93 285.2,93" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="288" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">升主</text>
<rect x="6" y="100" width="68" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="40" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端 B</text>
<text x="80" y="112" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SET NX → OK</text>
<line x1="74" y1="124" x2="223" y2="124" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="230,124 223,127.2 223,120.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="230" y="100" width="104" height="36" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="282" y="114.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新主库</text>
<text x="282" y="129.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">没有这把锁</text>
<text x="8" y="172" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">A、B 同时持锁</text>
<text x="8" y="194" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">复制是异步的：写入成功不等于已到从库</text>
<text x="8" y="216" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">单机重启：AOF everysec 掉电可能丢约 1 秒</text>
<text x="8" y="236" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">缓解：宕机节点至少等一个 TTL 再加入</text>
</svg>
A 在主库拿到锁，复制还没送到从库主库就宕机，从库升主；B 在新主库上 `SET NX` 照样成功，A 和 B 同时持锁。
**讲明白。**
- **根源是异步复制：** Redis 复制是异步的，写入返回成功，不等于已经到达从库，所以切换时最近的写入会丢。
- **锁偏偏是最近的写入：** 锁刚加上不久，就是「最近的写入」，最容易在切换时丢掉。
- **后果：** 新主上没有这把锁，B 对同一资源加锁也成功，两个客户端同时持锁，互斥失效。
- **单机重启也会丢锁：** 默认 AOF（追加写日志文件）是 `everysec`，每秒刷一次盘，掉电后可能丢最近约 1 秒的写入，锁的 key 就没了。
- **缓解办法是延迟重启：** 宕机的节点至少等一个 TTL 之后再重新参与，这样它忘掉的锁都已经过期。
- **适用范围：** 这类问题只有效率型场景（偶尔重复无所谓）可以接受，正确性型场景（重复会出错）需要更强的方案。
**举个例子。** 发奖励任务拿锁，主从切换：
1. **A 加锁：** 在主库 `SET lock:reward:9 uuid-A NX PX 30000` 返回 OK，A 开始给用户发奖励。
2. **主库宕机：** 锁的写入还没复制给从库。
3. **从库升主：** 新主上没有 `lock:reward:9`。
4. **B 加锁：** 在新主上 `SET NX` 成功。
5. **结果：** 两台机器同时给同一个用户发奖励。
**容易错。**
- **以为有了主从加哨兵，锁就高可用了：** 高可用的是服务，不是锁的互斥性；异步复制下切换会丢锁。
- **只想到主从切换：** 单机重启在 AOF `everysec` 下也会丢约 1 秒的写入。
- **以为重启后立刻加入就行：** 宕机节点应至少等一个 TTL 再参与，否则它忘掉的锁会被重复授予。
- **在正确性场景里直接用：** 资金和数据的正确性需要更强的方案，不能只靠这把锁。
**业务场景。** 主从切换的瞬间，刚拿到锁的发奖励任务锁丢了。另一台机器也拿到同一把锁，两台机器同时给同一个用户发放了奖励。
**系统设计。** [[links.job-scheduler-cron-history|分布式任务调度器（含 cron 与一年执行历史）]]：面试官问「调度器主节点切换时，任务会不会被执行两次」，答锁在切换时可能丢，所以任务本身要幂等，而不是只靠锁。
**可能问法。**
- Redis 分布式锁有什么缺陷？ → 主从异步复制，主库在锁复制到从库前宕机，从库升主后没有这把锁，别人也能加锁成功；单机重启在默认 AOF `everysec` 下掉电可能丢最近约 1 秒的写入；带 TTL 的锁遇到长 GC、进程暂停也会出现两个持有者。只有效率型场景可接受，正确性型要更强的方案。
- 主从切换会丢锁吗？ → 会。A 在主库加锁成功，主库返回后才异步复制给从库；主库在复制前宕机，从库升为新主，新主上没有这把锁，B 加锁也成功，两个客户端同时持锁。缓解办法是延迟重启：宕机的节点至少等一个 TTL 之后再重新参与。
