---
id: bagu-tx-lua-pipeline-1-tx-lua-pipeline
node: b.redis.tx-lua-pipeline
type: qa
step: 1
---
## Q
**事务、Lua 与 pipeline · 各保证什么**｜必会

面试官：「Redis 事务能回滚吗？Lua 脚本为什么能保证原子？pipeline 又是什么，和事务、mget 有什么区别？」

## A
**基本回答。** `MULTI`/`EXEC` 把命令排队后连续执行，中间不会插入别人的命令，但没有回滚：入队时语法错，整个 `EXEC` 被丢弃（EXECABORT）；运行时类型错只失败那一条，其余照常（如对字符串 `LPUSH` 报 WRONGTYPE）。Redis 认为命令错误是编程错误，应在开发期发现。`WATCH` 是乐观锁：被监视的 key 在 `EXEC` 前被改，整个事务放弃，业务重试。事务里命令只是排队，读不到值就没法判断，所以「判断库存再扣减」要用 Lua：脚本整体在单线程里原子执行，期间不处理别的命令。pipeline 只是批量发送、批量读回，省网络往返，不保证原子，别人的命令可以插进来；`MGET` 是单条命令，原子取多个 key。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 226">
<text x="8" y="42" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">事务</text>
<rect x="70" y="26" width="54" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="97" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">MULTI</text>
<rect x="130" y="26" width="58" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="159" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SET a 1</text>
<rect x="194" y="26" width="70" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="229" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">LPUSH a x</text>
<rect x="270" y="26" width="48" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="294" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">EXEC</text>
<text x="8" y="68" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">LPUSH 报 WRONGTYPE，只失败它，不回滚</text>
<text x="8" y="108" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Lua</text>
<rect x="70" y="92" width="262" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="201" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">一段脚本：读库存 → 判断 → 扣减</text>
<text x="8" y="134" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">脚本跑完前，别的客户端命令排队</text>
<text x="8" y="172" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">pipeline</text>
<rect x="70" y="156" width="50" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="95" y="172" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">GET a</text>
<rect x="126" y="156" width="50" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="151" y="172" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SET b</text>
<rect x="182" y="156" width="76" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="220" y="172" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">别人的命令</text>
<rect x="264" y="156" width="50" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="289" y="172" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">GET c</text>
<text x="8" y="198" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">一次发出、一次读回，省网络往返</text>
<text x="8" y="216" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">中间可穿插别人的命令，不保证原子</text>
</svg>
三行从上到下：事务是排好队一起执行，但出错不回滚；Lua 是一整段逻辑在服务端不被打断地跑完；pipeline 只是把多条命令一次发出去，高亮处是别人的命令可以插进来。
**业务场景。** 库存 5、每次扣 3：Lua 写成「够就 `DECRBY`，否则返回 -1」，第一次扣完剩 2，第二次读到 2 返回 -1。若写成先 `GET` 再 `SET`，两个客户端同时读到 5，各扣 3，卖出 6 件，超卖。领券的「判库存、扣库存、记用户已领」三步原子用 Lua；pipeline 用来批量预热缓存。
**容易错。**
- **以为 Lua 可以随便写长：** 脚本期间全库不处理别的命令，超过 `busy-reply-threshold`（默认 5 秒）其他客户端收到 BUSY，只能 `SCRIPT KILL`；Cluster 下脚本里的 key 必须同槽。
