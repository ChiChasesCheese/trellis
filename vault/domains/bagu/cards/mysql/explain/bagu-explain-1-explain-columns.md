---
id: bagu-explain-1-explain-columns
node: b.mysql.explain
type: qa
step: 1
---
## Q
**EXPLAIN · 看哪几列**｜必会

面试官：「一条慢 SQL，EXPLAIN 的输出你最先看哪几列？Using filesort 和 Using temporary 意味着什么？」

## A
**基本回答。** 先看 `type`（访问方式，好到坏是 const、eq_ref、ref、range、index、ALL，至少要到 range），再看 `key`（实际用的索引，NULL 表示没用）、`rows`（预估扫描行数）和 `Extra`。`Using index` 是覆盖索引，好；`Using filesort`（额外排序）和 `Using temporary`（临时表）要警惕。
`type` 档位：`const` 主键或唯一索引等值、最多一行；`eq_ref` 连表按主键或唯一索引匹配一行；`ref` 普通索引等值；`range` 索引范围；`index` 扫完整棵索引；`ALL` 全表。`filtered` 是过滤后剩余百分比，`rows × filtered` 约是传给下一步的行数。`Using where` 是 Server 层过滤。`rows` 来自统计信息，不准就 `ANALYZE TABLE`；8.0.18+ 的 `EXPLAIN ANALYZE` 会真正执行并给出实际行数和耗时。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 258">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">type 访问方式：从好到坏</text>
<rect x="8" y="22" width="50" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="33" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">const</text>
<rect x="62" y="22" width="50" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="87" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">eq_ref</text>
<rect x="116" y="22" width="50" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="141" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ref</text>
<rect x="170" y="22" width="50" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="195" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">range</text>
<rect x="224" y="22" width="50" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="249" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">index</text>
<rect x="278" y="22" width="50" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="303" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ALL</text>
<line x1="8" y1="60" x2="332" y2="60" stroke-width="1.2" stroke="currentColor"/>
<polygon points="332,60 325,63.2 325,56.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="195" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">至少要到 range</text>
<text x="8" y="104" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">key：实际用的索引，NULL 表示没用</text>
<text x="8" y="122" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">rows：预估扫描行数，来自统计信息</text>
<text x="8" y="140" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">Extra：Using index 是覆盖索引，好</text>
<text x="8" y="158" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Using filesort、Using temporary 要警惕</text>
<text x="8" y="184" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">WHERE user_id = 7 ORDER BY created_at</text>
<text x="8" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">建联合索引 (user_id, created_at)</text>
<rect x="8" y="212" width="148" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="82" y="226.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">没索引：ALL</text>
<text x="82" y="241.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Using filesort</text>
<line x1="156" y1="230" x2="180" y2="230" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="180,230 173,233.2 173,226.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="180" y="212" width="152" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="256" y="226.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">联合索引：ref</text>
<text x="256" y="241.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">没有 filesort</text>
</svg>
上半部分按 type 从好到坏排开，高亮的 range 是及格线；中间四行是 key、rows、Extra 的读法；下半部分是消除 filesort 的典型做法：让过滤列和排序列组成联合索引。
**举个例子。** 一条慢查询的排查：
1. **先跑 EXPLAIN：** 一条按 `amount` 过滤再按 `created_at` 排序的查询，在 20 万行的表上显示 `type = ALL`、Extra 里有 `Using filesort`。
2. **读结果：** `ALL` 说明全表扫描，没有可用的索引；`Using filesort` 说明扫出来后还要额外排一遍。
3. **改法：** 业务上常查某个用户的订单并按时间排序，写成 `WHERE user_id=7 ORDER BY created_at`，并建联合索引 `(user_id, created_at)`。
4. **再跑 EXPLAIN：** 同一个 `user_id` 下的行在索引里已经按 `created_at` 排好，直接顺着读，变成 `type = ref`，没有 filesort。
5. **估算传给下一步的行数：** 假设 `rows` 是 1000、`filtered` 是 10%，约 100 行传给下一步（假设值，只为说明算法）。
6. **怀疑估算不准：** 先 `ANALYZE TABLE` 刷新统计信息，再用 `EXPLAIN ANALYZE` 看实际行数和耗时。
**容易错。**
- **以为 Using filesort 一定用磁盘文件：** 它只表示需要额外排序，数据少时排序可能在内存里完成，但仍然是额外开销。
- **以为 type=ALL 就是没建索引：** 也可能是索引失效，或者优化器判断全表更便宜。
- **以为 rows 是精确值：** 它来自统计信息，是预估。
- **只调 SQL 写法不看索引：** 缺联合索引时，改写法解决不了 filesort。
- **混淆两种 Using index：** 前者是覆盖索引，后者是索引下推。
