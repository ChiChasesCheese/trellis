---
id: bagu-replication-lag-1-lag-read-your-write
node: b.mysql.replication-lag
type: qa
step: 1
---
## Q
**主从延迟 · 读写分离下读到旧数据**｜追问

面试官：「用户刚充值完再刷新，余额没变，是为什么？主从延迟怎么产生、怎么处理？」

## A
**基本回答。** 主库提交写 binlog，从库 I/O 线程拉到 relay log，SQL 线程回放，回放跟不上就延迟，读从库就读到旧数据。处理：关键读强制走主库；写后一小段时间内同一用户读主库；或等从库追上某个 GTID 位点再读。
并行复制：5.7 起按组提交并行回放；8.0.46 实测默认 `replica_parallel_workers=4`、`LOGICAL_CLOCK`；`WRITESET` 并行度更高，但要自己把 `binlog_transaction_dependency_tracking` 设成它（默认 `COMMIT_ORDER`）。主库宕机：选 GTID 最新的从库升主，其他从库改指向它（MHA、Orchestrator 或云厂商高可用）；异步复制可能丢最后几个事务，金融场景用半同步或 MGR。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 224">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">主库写入 → 从库回放</text>
<rect x="8" y="22" width="88" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="52" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主库</text>
<text x="52" y="53.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写 binlog</text>
<line x1="96" y1="42" x2="112" y2="42" stroke-width="1.2" stroke="currentColor"/>
<polygon points="112,42 105,45.2 105,38.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="112" y="22" width="104" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="164" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">从库 I/O 线程</text>
<text x="164" y="53.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">拉到 relay log</text>
<line x1="216" y1="42" x2="232" y2="42" stroke-width="1.2" stroke="currentColor"/>
<polygon points="232,42 225,45.2 225,38.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="232" y="22" width="100" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="282" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SQL 线程</text>
<text x="282" y="53.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回放跟不上</text>
<text x="8" y="88" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">用户刚充值，马上刷新（余额数字为假设）</text>
<text x="8" y="108" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1. 写主库：余额 100 → 150</text>
<text x="8" y="126" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2. 读从库：还没回放，读到 100</text>
<text x="8" y="154" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">关键读强制走主库</text>
<text x="8" y="172" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">写后一小段时间内，同一用户读主库</text>
<text x="8" y="190" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">或等从库追上某个 GTID 位点再读</text>
<text x="8" y="214" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">半同步：保证从库收到 binlog，不保证回放完</text>
</svg>
主库写 binlog，从库 I/O 线程把它拉成 relay log，SQL 线程再回放；高亮的 SQL 线程回放不及时，就是主从延迟。下半部分是用户刚充值就读到旧余额的过程，以及三种处理办法。
**举个例子。** 用户充值后马上刷新：
1. **写主库：** 用户充值，主库提交，余额从 100 变 150（假设值），写入 binlog。
2. **从库没跟上：** 从库 I/O 线程已经把 binlog 拉过来了，但 SQL 线程正忙着回放前面一个更新百万行的大事务，这条充值要排在后面。
3. **读到旧数据：** 用户刷新，请求被读写分离路由到从库，读到 100，以为钱没到账。
4. **办法一：** 余额页的读强制走主库，读到 150。
5. **办法二：** 充值成功后的一小段时间内，这个用户的所有读都走主库。
6. **办法三：** 主库返回这次写入的 GTID，读从库之前先等从库追上这个 GTID 再读。
7. **扣款校验：** 无论哪种办法，真正扣款前的余额校验都走主库，不能依赖可能过期的从库。
**容易错。**
- **以为半同步就消除了延迟：** 它保证从库「收到」binlog，不保证「回放完」，读从库仍可能读到旧值。
- **以为延迟只是网络问题：** 更常见的是主库大事务、从库回放慢、从库上有慢查询。
- **以为并行复制默认就是最优：** `WRITESET` 并行度更高，但要自己把 `binlog_transaction_dependency_tracking` 设成它，默认是 `COMMIT_ORDER`。
- **以为异步复制不丢事务：** 主库宕机时，还没传到从库的最后几个事务会丢。
- **所有读都放从库：** 余额这类读到旧值会出业务问题，要走主库。
