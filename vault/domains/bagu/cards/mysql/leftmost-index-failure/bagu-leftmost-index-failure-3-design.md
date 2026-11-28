---
id: bagu-leftmost-index-failure-3-design
node: a.mysql.leftmost-index-failure
type: qa
step: 3
---
## Q
**索引设计 · 列的顺序怎么定，ORDER BY 要不要写 DESC**｜追问

面试官：「联合索引列顺序怎么排？查询 `WHERE user_id=? ORDER BY created_at DESC`，索引里 `created_at` 要不要建降序？索引越多越好吗？」

## A
**基本回答。** 联合索引的列顺序按优先级来排：先满足最常见查询的最左前缀；等值条件的列放前面、范围条件的列放后面；多个等值列里区分度高的放前面；排序列放在等值列之后，让索引天然有序，避免 filesort（额外排序）。`ORDER BY created_at DESC` 不必把 `created_at` 建成降序：升序索引可以反向扫描（Extra 显示 `Backward index scan`）。索引也不是越多越好，每多一个，写入就多一份维护。
8.0 起有真正的降序索引，用于混合方向 `ORDER BY status DESC, created_at ASC`：升序的 `(user_id, status, created_at)` 会 `Using filesort`，要建 `(user_id, status DESC, created_at)`。找无用索引用 `sys.schema_unused_indexes`，找冗余前缀索引用 `sys.schema_redundant_indexes`，如已有 `(user_id, created_at)` 就不需要单独的 `(user_id)`。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 222">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">联合索引 (user_id, status, created_at)</text>
<rect x="8" y="26" width="100" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58.0" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">等值列</text>
<text x="58.0" y="57.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">user_id =</text>
<rect x="112" y="26" width="100" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="162.0" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">等值列</text>
<text x="162.0" y="57.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">status =</text>
<rect x="216" y="26" width="116" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="274.0" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">范围列 / 排序列</text>
<text x="274.0" y="57.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">created_at</text>
<text x="8" y="88" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">等值在前、范围在后、排序列放最后</text>
<rect x="8" y="100" width="324" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="117.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">同一 user_id 内 created_at 从小到大排好</text>
<line x1="324" y1="144" x2="23.0" y2="144.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="16.0,144.0 23.0,140.8 23.0,147.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="166" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ORDER BY created_at DESC：从大端反向扫</text>
<text x="8" y="186" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Backward index scan，不用建降序索引</text>
<text x="8" y="206" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">混合方向才需要 8.0 的降序索引</text>
</svg>
上方三个格子是联合索引的列，从左到右依次是等值列、等值列、范围或排序列；中间的长条表示同一个 user_id 下 created_at 从小到大排好，`DESC` 就是从大的一端往回读（箭头向左），所以不需要建降序索引。
**举个例子。** 订单表常见两个查询：「某用户最近订单」和「某用户某状态的订单」：
1. **用户最近订单：** `WHERE user_id=? ORDER BY created_at DESC`，已有 `(user_id, created_at)`：定位到该用户那一段，从最新一端反向读，没有 filesort。
2. **用户某状态订单：** `WHERE user_id=? AND status=? ORDER BY created_at DESC`：两个等值列在前、排序列在最后，用 `(user_id, status, created_at)` 一次定位，也是反向扫描。
3. **冗余判断：** 已有 `(user_id, created_at)`，再建 `(user_id)` 就是冗余，因为前者的最左前缀已经覆盖了它。
4. **混合方向：** 若要 `ORDER BY status DESC, created_at ASC`，升序的 `(user_id, status, created_at)` 会 `Using filesort`；建 `(user_id, status DESC, created_at)` 就没有。
**容易错。**
- **以为倒序一定要降序索引：** 升序索引可以反向扫描，只有混合方向才需要 8.0 的降序索引。
- **以为索引越多越好：** 每个索引都占空间、拖慢写入、占缓冲池，优化器还更容易选错。
- **把区分度高的列一律放最前：** 要先满足最常见查询的最左前缀，其次才是区分度；范围列也不要放在等值列前面。
- **在 5.7 上建降序索引：** 5.7 及以前会解析 `DESC` 但忽略，等于没建。
