---
id: bagu-deep-pagination-1-offset-keyset
node: b.mysql.deep-pagination
type: qa
step: 1
---
## Q
**深分页 · 为什么慢、怎么优化**｜必会

面试官：「`LIMIT 1000000, 20` 为什么慢？怎么优化？游标分页为什么要带唯一键？」

## A
**基本回答。** 它要先取出前 100 万零 20 行再丢掉前 100 万行，走二级索引时每行还要回表。优化：游标分页（记住上一页最后一条，`WHERE id < :last ORDER BY id DESC LIMIT 20`）、延迟关联（先在覆盖索引上取 id，再回表）、限制最大页数。
实测（MySQL 8.0.46，640 万行）：`LIMIT 1000000, 20` 约 1.6 秒，延迟关联约 0.18 秒，游标分页约 1.4 毫秒且与页码无关。排序列不唯一要带唯一键，否则同值行会漏或重：`ORDER BY created_at DESC, id DESC`，条件 `created_at < :t OR (created_at = :t AND id < :id)`，索引 `(created_at, id)`。搜索场景用 Elasticsearch 的 `search_after`，原理相同。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 242">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">LIMIT 1000000, 20：先扫再丢</text>
<rect x="8" y="22" width="256" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="136" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">前 100 万行：读出来再丢掉</text>
<rect x="268" y="22" width="64" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="300" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">要的 20</text>
<text x="8" y="68" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">约 1.6 秒（640 万行实测）</text>
<text x="8" y="96" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">游标分页：从上一页最后一条直接定位</text>
<rect x="8" y="104" width="130" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="73" y="121" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">上一页最后一条 id</text>
<line x1="138" y1="117" x2="158" y2="117" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="158,117 151,120.2 151,113.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="158" y="104" width="174" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="245" y="121" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">索引定位，只读 20 行</text>
<text x="8" y="150" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">约 1.4 毫秒，与页码无关</text>
<text x="8" y="178" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">延迟关联：先在覆盖索引上取 id</text>
<rect x="8" y="186" width="150" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83" y="203" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">覆盖索引扫出 id</text>
<line x1="158" y1="199" x2="176" y2="199" stroke-width="1.2" stroke="currentColor"/>
<polygon points="176,199 169,202.2 169,195.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="176" y="186" width="156" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254" y="203" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只对 20 个 id 回表</text>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">约 0.18 秒，仍要扫过前面的索引项</text>
</svg>
三种做法从上到下：偏移分页要读出前 100 万行再丢掉；游标分页用上一页最后一条的 id 直接在索引里定位；延迟关联先在覆盖索引上只取 id，最后只回表这一页的 20 行。
**举个例子。** 一个信息流按 `(created_at, id)` 倒序翻页：
1. **第一页：** `ORDER BY created_at DESC, id DESC LIMIT 20`，最后一条是 `created_at = 10:00:05`、`id = 905`。
2. **第二页：** 条件写成 `created_at < '10:00:05' OR (created_at = '10:00:05' AND id < 905)`，同样 `LIMIT 20`，索引 `(created_at, id)` 直接定位。
3. **为什么要带 id：** 假设 10:00:05 这一秒有 3 条，id 为 907、905、903，第一页已经返回了 907 和 905。只写 `created_at < t` 会漏掉 903；写 `created_at <= t` 会把 907、905 又返回一遍。
4. **对比偏移分页：** 翻到第 5 万页时 `LIMIT 1000000, 20` 约 1.6 秒，游标约 1.4 毫秒。
5. **翻页时有新文章插入：** 偏移分页的页码是按位置算的，新文章让后面的行整体后移，同一条会重复出现；游标是按值定位的，不受插入影响。
**容易错。**
- **以为加索引就能解决深分页：** 有索引也一样，偏移量大时仍要扫过前面所有索引项（走二级索引还要回表），仍是 O(offset)。
- **以为延迟关联是常数时间：** 它仍是 O(offset)，只是不回表，约 0.18 秒。
- **以为游标分页可以跳页：** 不能，只能上一页下一页。
- **排序列不唯一时只用它做游标：** 同值的行会漏或重，要带唯一键。
- **写成元组比较：** `(created_at, id) < (:t, :id)` 在 MySQL 里不走范围扫描，要展开成 OR。
