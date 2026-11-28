---
id: bagu-isolation-levels-6-long-txn
node: a.mysql.isolation-levels
type: qa
step: 6
---
## Q
**长事务 · 会带来什么问题，怎么发现和避免**｜追问

面试官：「线上有个事务开了两小时没提交，会有什么后果？怎么发现、怎么避免？」

## A
**基本回答。** 一个事务开了两小时不提交，会带来五类后果：旧版本无法清理，undo 膨胀、版本链变长、查询变慢；行锁不释放，别的事务等到 `innodb_lock_wait_timeout`（默认 50 秒）超时；它持有元数据锁，后面的 DDL 被挡住，而排在 DDL 后面的所有查询又被 DDL 挡住；大事务产生大 binlog，造成主从延迟；它一直占着连接，连接池可能耗尽。发现的办法：查 `information_schema.innodb_trx` 的 `trx_started`，最早开始的就是嫌疑人，并监控 `History list length`。
实验（8.0.46）：开 `START TRANSACTION WITH CONSISTENT SNAPSHOT` 不提交，另一个连接对同一行更新 2 万次，`History list length` 涨到 20002，长事务结束后降回 0。避免：事务内不调远程服务、不等用户输入；批量更新每批几百到几千行；后台任务设事务超时；用框架管理事务防漏 `commit`；必要时 `KILL` 线程。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 220">
<rect x="8" y="10" width="324" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="28.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">长事务：开了快照，一直不提交</text>
<line x1="170" y1="38" x2="170.0" y2="51.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,58.0 166.8,51.0 173.2,51.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="178" y="53" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一行被更新 2 万次</text>
<rect x="8" y="62" width="52" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="34.0" y="79.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">v1</text>
<line x1="60" y1="75" x2="67.0" y2="75.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="74.0,75.0 67.0,78.2 67.0,71.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="74" y="62" width="52" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="100.0" y="79.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">v2</text>
<line x1="126" y1="75" x2="133.0" y2="75.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="140.0,75.0 133.0,78.2 133.0,71.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="140" y="62" width="52" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="166.0" y="79.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">v3</text>
<line x1="192" y1="75" x2="199.0" y2="75.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="206.0,75.0 199.0,78.2 199.0,71.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="206" y="62" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="226.0" y="79.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">…</text>
<line x1="246" y1="75" x2="253.0" y2="75.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="260.0,75.0 253.0,78.2 253.0,71.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="260" y="62" width="72" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="296.0" y="79.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">v20002</text>
<line x1="170" y1="88" x2="170.0" y2="101.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,108.0 166.8,101.0 173.2,101.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="108" width="324" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="126.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">purge 被卡住：旧版本一个都不能清</text>
<text x="8" y="162" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">History list length 涨到 20002</text>
<text x="8" y="182" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">长事务结束后降回 0</text>
<text x="8" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">还会：锁不放、挡 DDL、大 binlog、占连接</text>
</svg>
长事务在快照里一直不结束，同一行被别人更新了 2 万次，每次更新都留下一个旧版本；这些版本都要为那个长事务的读视图保留，所以 purge（后台清理线程）一个都清不掉，History list length 一路涨到 20002。
**举个例子。** 对账明细导出，在事务里一边查一边写文件上传，持续了 40 分钟：
1. **undo 暴涨：** 这 40 分钟里别人对相关行的更新产生的旧版本都要保留，undo 越积越多。
2. **DDL 被卡住：** DBA 这时要加索引，DDL 拿不到元数据锁，在后面排队。
3. **连锁排队：** 对该表的所有新查询又排在 DDL 后面，接口大面积超时。
4. **修复：** 改成分批读取，读完立即提交，事务只活几秒，恢复正常。
**容易错。**
- **以为只读事务不碍事：** 只读事务的读视图也会让旧版本无法清理；开着快照不提交同样会卡住 purge。
- **以为长事务只影响自己：** 它会影响所有对相关表的写入、DDL 和主从延迟。
- **在事务里调用远程服务或等用户输入：** 事务时间不可控，应把耗时操作放到事务外。
- **只设置锁等待超时不查长事务：** 1205 超时多是长事务持锁不放引起的，根因要去找长事务。
