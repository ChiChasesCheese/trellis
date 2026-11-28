---
id: bagu-count-ddl-1-count-online-ddl
node: b.mysql.count-ddl
type: qa
step: 1
---
## Q
**count 计数与大表加字段 · 为什么慢、怎么不影响线上**｜追问

面试官：「`count(*)`、`count(1)`、`count(字段)` 有什么区别，为什么慢？给十亿行的大表加字段怎么做才不影响线上？」

## A
**基本回答。** InnoDB 有 MVCC（多版本并发控制，每个事务看到自己那一份快照），不同事务同一时刻看到的行数可能不同，所以引擎不存总行数，`count(*)` 只能现数，优化器会选最小的二级索引来扫。`count(*)` 和 `count(1)` 一样快，`count(字段)` 还要判断 NULL，更慢。大表加字段：8.0.12+ 用 `ALGORITHM=INSTANT` 只改元数据，秒级；否则用在线 DDL（`INPLACE`）；超大表用 gh-ost 或 pt-online-schema-change。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 222">
<text x="10" y="16" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">gh-ost：影子表 + binlog 追增量 + 原子改名</text>
<rect x="10" y="28" width="76" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="48" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">原表 t</text>
<text x="48" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线上读写</text>
<rect x="138" y="28" width="64" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="54" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">gh-ost</text>
<rect x="254" y="28" width="76" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="292" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">影子表</text>
<text x="292" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">已加新列</text>
<text x="112" y="52" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">binlog</text>
<line x1="86" y1="60" x2="138" y2="60" stroke="currentColor" stroke-width="1.2"/>
<polygon points="138,60 131.7,63.0 131.7,57.0" fill="currentColor"/>
<text x="228" y="52" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">回放</text>
<line x1="202" y1="60" x2="254" y2="60" stroke="currentColor" stroke-width="1.2"/>
<polygon points="254,60 247.7,63.0 247.7,57.0" fill="currentColor"/>
<text x="10" y="98" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1. 建影子表并加列</text>
<text x="10" y="116" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">2. 分批复制旧数据，同时追 binlog 里的新变更</text>
<text x="10" y="134" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">3. 追平后短暂 RENAME，原子切换</text>
<text x="10" y="152" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">pt-osc 用触发器同步增量，gh-ost 不用</text>
<rect x="10" y="168" width="320" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="184.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8.0.12+ INSTANT：只改元数据，秒级</text>
<text x="170" y="199.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">仍要拿元数据锁，只是持锁极短</text>
</svg>
左上是 gh-ost 的三步：读 binlog 的增量变更、回放到影子表、最后改名切换；最下面一格是 INSTANT 的捷径。
**举个例子。** 提交记录表有十亿行，要加一列、还要显示总提交数：
1. **先查长事务：** 发现有一个跑了半小时的报表事务，等它结束，否则 DDL 会排在它后面，连带堵住所有查询。
2. **设短超时：** 把 `lock_wait_timeout` 调成几秒，拿不到锁就报错退出，下次再试，不拖累线上。
3. **加列走 INSTANT：** 执行 `ALTER TABLE ... ADD COLUMN ..., ALGORITHM=INSTANT`，元数据一改完就返回，秒级。
4. **改列类型走 gh-ost：** 同一张表改列类型时 INSTANT 报错「需要重建表」，改用 gh-ost：建影子表、分批复制、读 binlog 追增量，追平后原子改名。
5. **总数不现数：** 界面上的总提交数读汇总表或 Redis 里的缓存值，不再每次翻页都 `count(*)`。
**容易错。**
- **以为 count(1) 比 count(*) 快：** 两者一样快，都只是数行。
- **以为 INSTANT 完全不拿锁：** 它仍要拿元数据锁，只是持锁极短；前面有长事务照样会排队。
- **以为所有 DDL 都能 INSTANT：** 修改列类型这类要重建表的操作不行，要走 INPLACE 或 gh-ost。
- **直接在线上 ALTER 十亿行表：** 没查长事务、没设 `lock_wait_timeout`，一个长事务就能让所有查询排队。
