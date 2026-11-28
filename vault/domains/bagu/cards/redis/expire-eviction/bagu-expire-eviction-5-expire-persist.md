---
id: bagu-expire-eviction-5-expire-persist
node: a.redis.expire-eviction
type: qa
step: 5
---
## Q
**过期与持久化、主从 · 过期 key 怎么处理**｜追问

面试官：「过期的 key 在 RDB、AOF、主从复制里怎么处理？从库读到过期 key 返回什么？」

## A
**基本回答。** 过期只有主库一个人说了算。RDB：生成时跳过过期 key；加载时主库忽略，从库全部加载（从库以主库的 `DEL` 为准）。AOF：key 被删除时追加一条 `DEL`（异步释放是 `UNLINK`），重写时不写过期 key；`EXPIRE` 传播时被改写成绝对时间的 `PEXPIREAT`，所以重放 AOF 或从库回放延迟都不会让过期时间重新计时，也因此主从系统时钟要同步。主从：主库删除后向从库传 `DEL`，从库不主动删，这样复制链路上只有一份删除决策，不因时钟差异而不一致，代价是从库内存里可能暂留已逻辑过期的 key；从库读到逻辑已过期的 key，3.2 之后返回空，3.2 之前照样返回值。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="110" y="6" width="120" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="22" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主库</text>
<text x="170" y="37" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">到期才决定删</text>
<line x1="140" y1="46" x2="78" y2="96" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="78,96 81.4,89.1 85.5,94.1" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="96" y="66" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">DEL</text>
<line x1="200" y1="46" x2="262" y2="96" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="262,96 254.5,94.1 258.6,89.1" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="238" y="66" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">DEL</text>
<rect x="8" y="96" width="140" height="62" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="78" y="115.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">AOF</text>
<text x="78" y="130.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">追加 DEL</text>
<text x="78" y="145.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">重写不写过期 key</text>
<rect x="192" y="96" width="140" height="62" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="262" y="115.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">从库</text>
<text x="262" y="130.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不自己删</text>
<text x="262" y="145.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">等主库传 DEL</text>
<line x1="262" y1="158" x2="262" y2="180" stroke-width="1.2" stroke="currentColor"/>
<polygon points="262,180 258.8,173.0 265.2,173.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="192" y="180" width="140" height="66" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="262" y="201.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">从库读到过期 key</text>
<text x="262" y="216.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3.2 之后返回空</text>
<text x="262" y="231.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3.2 之前照样返回值</text>
<rect x="8" y="180" width="140" height="78" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="78" y="200" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">RDB</text>
<text x="78" y="215" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">生成时跳过过期 key</text>
<text x="78" y="230" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">加载：主库忽略</text>
<text x="78" y="245" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">从库全部加载</text>
</svg>
主库到期才决定删，删了向 AOF 追加 `DEL`、向从库传 `DEL`；从库自己不删，但读到过期 key 时 3.2 之后返回空；RDB 在生成和加载时各有处理。
**业务场景。** 读写分离，写主库读从库「奖励是否已领取」：主库 `SET claimed:u1 1 EX 86400` 传给从库的是 `PEXPIREAT <绝对时间戳>`；到期瞬间主库还没删，从库收到读请求，3.2 及之后返回空，与主库一致；若还是 3.0 版本，从库仍返回 `1`，应用会误以为用户已领过，导致重复发奖。
**容易错。**
- **以为从库自己会删过期 key。**
- **以为 RDB 里不可能有过期 key：** 生成之后到加载之前 key 可能已过期。
- **以为所有版本从库都返回空。**
