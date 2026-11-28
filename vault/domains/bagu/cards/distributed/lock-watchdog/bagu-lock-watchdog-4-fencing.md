---
id: bagu-lock-watchdog-4-fencing
node: a.distributed.lock-watchdog
type: qa
step: 4
---
## Q
**fencing token · 怎么用在下游写入上**｜必会

面试官：「怎么彻底防住过期的持有者继续写？fencing token 是什么？」

## A
**基本回答。** 锁服务每次发放锁时返回一个单调递增的数字（token，令牌）。持有者每次写下游都带上它，下游记录见过的最大 token，拒绝比它小的请求。这样即使旧持有者因长 GC 醒来，它带的旧 token 也会被拒绝。SQL 示例放在后面的代码一节。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 268">
<rect x="10" y="6" width="80" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50" y="23" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">持有者 A</text>
<line x1="50" y1="32" x2="50" y2="212" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<rect x="130" y="6" width="80" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="23" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">下游数据库</text>
<line x1="170" y1="32" x2="170" y2="212" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<rect x="250" y="6" width="80" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="290" y="23" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端 B</text>
<line x1="290" y1="32" x2="290" y2="212" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="54" y="54" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">拿到 token 41</text>
<text x="176" y="54" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">拿到 token 42</text>
<text x="176" y="68" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">（B 在 A 之后）</text>
<text x="54" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">长 GC 停顿…</text>
<text x="176" y="108" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">写入 token 42</text>
<line x1="290" y1="114" x2="177" y2="114" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,114 177,110.8 177,117.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="176" y="134" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">记下最大值 42</text>
<text x="54" y="164" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">醒来，写入 token 41</text>
<line x1="50" y1="170" x2="163" y2="170" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,170 163,173.2 163,166.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="176" y="190" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">41 < 42，拒绝</text>
<rect x="6" y="222" width="328" height="36" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="236.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">下游自己比较并拒绝</text>
<text x="170" y="251.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不靠持有者的时钟和自觉</text>
</svg>
A 拿到 41，B 在 A 之后拿到 42 并先写，下游记下最大值 42。A 长 GC 醒来再带 41 来写，41 小于 42，被下游拒绝。判断发生在数据所在的地方。
**代码。** 带 token 的条件更新（B 的写入）：
```sql
UPDATE account SET balance = balance - 100, fence = 42
WHERE id = 7 AND fence < 42;   -- 影响行数为 0 表示这是过期持有者
```
**容易错。**
- **以为只靠锁就够：** 锁会过期，过期的持有者仍可能写，token 才能让下游拒绝。
- **token 只发不校验：** 必须在下游比较并拒绝，才起作用。
- **把 fencing 当成幂等：** fencing 拦旧持有者晚到的写，幂等拦同一请求的重复。
- **以为 Redis 单实例锁就能发 token：** 它本身不提供；ZooKeeper 的 zxid、etcd 的 revision 可以当 token，或靠下游版本号。

**业务场景。** 余额表加一列 `fence`，扣款时带锁的 token。旧持有者在长停顿后醒来，条件更新不命中，扣款没有生效，只需重新读取状态后决定是否重试。
