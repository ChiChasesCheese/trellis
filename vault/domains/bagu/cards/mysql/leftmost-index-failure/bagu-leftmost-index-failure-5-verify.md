---
id: bagu-leftmost-index-failure-5-verify
node: a.mysql.leftmost-index-failure
type: qa
step: 5
---
## Q
**验证 · 怎么确认一条 SQL 走没走索引**｜追问

面试官：「怎么确认一条 SQL 用没用上索引、用到联合索引几列？EXPLAIN 显示用了索引就一定快吗？」

## A
**基本回答。** 用 `EXPLAIN` 看：`key` 是实际用的索引（为空就是没用）；`type` 从好到坏依次是 `const`/`eq_ref`、`ref`、`range`、`index`、`ALL`；`key_len` 用来算用了联合索引的几列；`rows` 是预估要扫的行数；`Extra` 里看有没有 `Using filesort`、`Using temporary`，以及 `Using index`、`Using index condition`。8.0.18 起还有 `EXPLAIN ANALYZE`，它真正执行语句，给出每一步的实际行数和耗时。EXPLAIN 只是估算，显示用了索引不等于一定快，要同时看扫描行数和返回行数。
`key_len` 是用到的索引前缀总字节数：bigint 8、tinyint 1、datetime 5，`varchar(20)` 在 utf8mb4 下是 20×4+2=82，允许 NULL 再加 1。慢日志里 `Rows_examined` 远大于 `Rows_sent`（扫 10 万行只返回 1 行）说明索引没起到过滤作用。`optimizer_trace` 看优化器为何不选某个索引，`sys.statements_with_full_table_scans` 列出全表扫描语句，统计信息过期就 `ANALYZE TABLE`。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 208">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">索引 (user_id, status, created_at)</text>
<rect x="8" y="26" width="120" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="68.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">user_id 8B</text>
<rect x="128" y="26" width="90" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="173.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">status 1B</text>
<rect x="218" y="26" width="114" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="275.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">created_at 5B</text>
<line x1="8" y1="74" x2="128" y2="74" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="134" y="78" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">key_len=8 → 用 1 列</text>
<line x1="8" y1="92" x2="218" y2="92" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="224" y="96" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">=9 → 2 列</text>
<line x1="8" y1="110" x2="332" y2="110" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="8" y="130" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">key_len=14 → 3 列（假设都 NOT NULL）</text>
<text x="8" y="156" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">bigint 8、tinyint 1、datetime 5</text>
<text x="8" y="176" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">varchar(20) utf8mb4：20×4+2=82</text>
<text x="8" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">允许 NULL 的列再加 1 字节</text>
</svg>
把联合索引每一列的字节数首尾相接：`key_len=8` 只用了 user_id 一列，`key_len=9` 用了两列，14 是三列都用上（假设都是 NOT NULL）。
**举个例子。** 评审对账查询，索引是 `(user_id, status, created_at)`：
1. **看到 key：** `key` 是 `idx_user_status`，看起来用上了索引，似乎正常。
2. **看 key_len：** 只有 8，对照图就是只用到 `user_id` 一列，`status` 和后面的列都没参与定位。
3. **看 rows：** 预估 5 万行，说明 `user_id` 这一列把范围缩得不够小。
4. **修正：** 补全条件并调整列顺序后重新 EXPLAIN，`rows` 降到 40。
5. **效果：** 对账从几分钟缩到几秒。
6. **再验证：** 用 `EXPLAIN ANALYZE` 对比估算行数和实际行数，确认优化器没有被过期统计信息误导。
**容易错。**
- **看到 `key` 有值就放心：** 还要看 `key_len` 用了几列、`rows` 有多大、Extra 有没有 `Using filesort`。
- **把 EXPLAIN 当成实际执行：** EXPLAIN 只是估算，不执行语句；要真实数据用 `EXPLAIN ANALYZE`（会真正执行，慢查询要小心）。
- **key_len 忘了 NULL 和字符集：** 允许 NULL 要加 1；`varchar` 的字节数随字符集变，utf8mb4 下是 4 倍字符数再加 2。
- **统计信息过期不处理：** `rows` 偏差大时，先 `ANALYZE TABLE` 刷新统计信息。
