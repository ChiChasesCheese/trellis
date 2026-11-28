---
id: hi-sdx-repl-topologies
node: more.replication
type: qa
step: 1
---
## Q
**复制的三种拓扑：单主、多主、无主**｜补充 · 复制 · 必会

同一份数据要存在多个副本上。写请求可以怎样分给这些副本？单主、多主、无主各自怎么工作，代价是什么，怎么选？

## A
**结论。** 区别只在「谁有资格接受写」：单主只有一个 leader 接受写，其余副本（follower）照它的日志复制；多主有几个 leader 各自接受写，再互相异步同步；无主没有 leader，写和读都发给多个副本，靠法定人数（quorum）保证有重叠。默认用单主，另外两种是为了单主做不到的事：就近写、离线写、节点随时可挂。

**要点。**
- **单主：** 所有写的顺序都由 leader 决定，没有写冲突；leader 是写入瓶颈，也是单点，挂了要选出新的 leader（故障转移）；follower 可以分担读。MySQL、PostgreSQL 的主从复制都是这种。
- **多主：** 典型场景是每个机房一个 leader，用户就近写；还有离线可写的手机应用，每台设备相当于一个 leader。好处是写不用跨机房，断网也能写。
- **无主：** Dynamo、Cassandra 的做法。N 个副本，写成功 W 个就算成功，读 R 个取最新的；R+W>N 时（例如 N=3、W=2、R=2）读到的副本里必有一个收到过这次写。
- **怎么选：** 能接受单个写入点就单主；写必须就近或离线可写，才用多主，并先想好冲突怎么合并；要「任意一个节点挂了也能写」且接受最终一致，才用无主。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 326">
<text x="8" y="22" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">单主</text>
<rect x="60" y="30" width="44" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="82" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写</text>
<rect x="130" y="30" width="60" height="28" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="160" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">leader</text>
<polyline points="104,44 130,44" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="130,44 123.0,47.2 123.0,40.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="240" y="14" width="90" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="285" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">follower</text>
<rect x="240" y="50" width="90" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="285" y="67" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">follower</text>
<polyline points="190,44 240,28" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="240,28 234.3,33.2 232.4,27.1" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="190,44 240,62" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="240,62 232.3,62.6 234.5,56.6" style="fill:var(--accent,#3b6fd4)"/>
<text x="212" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">follower 复制 leader 的日志</text>
<polyline points="8,98 332,98" fill="none" stroke-width="1" stroke-dasharray="2 4" stroke="currentColor" opacity="0.5"/>
<text x="8" y="118" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">多主</text>
<rect x="30" y="134" width="96" height="28" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="78" y="152" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">leader A</text>
<rect x="214" y="134" width="96" height="28" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="262" y="152" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">leader B</text>
<polyline points="126,148 214,148" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="214,148 207.0,151.2 207.0,144.8" style="fill:var(--accent,#3b6fd4)"/>
<polygon points="126,148 133.0,144.8 133.0,151.2" style="fill:var(--accent,#3b6fd4)"/>
<text x="170" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">互相异步同步</text>
<text x="78" y="182" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">机房 A 就近写</text>
<text x="262" y="182" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">机房 B 就近写</text>
<polyline points="8,196 332,196" fill="none" stroke-width="1" stroke-dasharray="2 4" stroke="currentColor" opacity="0.5"/>
<text x="8" y="216" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">无主</text>
<rect x="30" y="258" width="60" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="60" y="276" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端</text>
<rect x="240" y="218" width="80" height="26" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="280" y="235" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">副本 1</text>
<rect x="240" y="250" width="80" height="26" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="280" y="267" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">副本 2</text>
<rect x="240" y="282" width="80" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="280" y="299" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">副本 3</text>
<polyline points="90,272 240,231" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="240,231 234.1,235.9 232.4,229.8" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="90,272 240,263" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="240,263 233.2,266.6 232.8,260.2" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="90,272 240,295" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="240,295 232.6,297.1 233.6,290.8" style="fill:var(--accent,#3b6fd4)"/>
<text x="170" y="316" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">N=3：写到 2 个（W=2）即成功</text>
</svg>

**面试里这样说。** 「默认单主：一个 leader 决定写入顺序，follower 分担读。只有写必须就近落地或要离线可写，我才用多主，并且先定好冲突的合并规则；要节点随时可挂、接受最终一致的存储，我用 Dynamo 风格的无主加 quorum。」

**易错。**
- **把多主当成单主的加强版：** 多主会带来写冲突，自增主键、唯一约束这些单写者的假设都要重新设计。
- **以为 R+W>N 就是强一致：** 它只保证读得到已确认的写，读与读之间的先后没有保证。
