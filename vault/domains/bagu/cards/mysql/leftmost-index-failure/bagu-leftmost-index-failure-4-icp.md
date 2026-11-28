---
id: bagu-leftmost-index-failure-4-icp
node: a.mysql.leftmost-index-failure
type: qa
step: 4
---
## Q
**索引下推 · 它在联合索引里起什么作用**｜追问

面试官：「什么是索引下推（ICP）？和覆盖索引有什么区别？」

## A
**基本回答。** 索引下推（index condition pushdown，简称 ICP，5.6 起）是把一部分 WHERE 条件交给存储引擎：遍历二级索引时，先用索引里已有的列过滤，满足了才回表去取整行。没有 ICP 时，引擎只按能定位的条件取一行就回表，把整行交给 server 层再过滤，不满足的行回表就白做了。用上 ICP 时 Extra 显示 `Using index condition`。
验证（8.0.46）：EXPLAIN 显示 `Using index condition`；`SET optimizer_switch='index_condition_pushdown=off'` 关掉后变成 `Using where`。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没有 ICP</text>
<rect x="8" y="22" width="100" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58.0" y="36.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">取 user_id=5</text>
<text x="58.0" y="51.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5000 条</text>
<line x1="108" y1="40" x2="113.0" y2="40.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="120.0,40.0 113.0,43.2 113.0,36.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="120" y="22" width="100" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="36.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回表 5000 次</text>
<text x="170.0" y="51.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">（随机访问）</text>
<line x1="220" y1="40" x2="225.0" y2="40.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="232.0,40.0 225.0,43.2 225.0,36.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="232" y="22" width="100" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282.0" y="36.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">server 层过滤</text>
<text x="282.0" y="51.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只剩 20 条</text>
<text x="8" y="88" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">有 ICP</text>
<rect x="8" y="96" width="100" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58.0" y="110.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">取 user_id=5</text>
<text x="58.0" y="125.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">索引里先过滤</text>
<line x1="108" y1="114" x2="113.0" y2="114.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="120.0,114.0 113.0,117.2 113.0,110.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="120" y="96" width="100" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="110.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只剩 20 条</text>
<text x="170.0" y="125.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回表 20 次</text>
<line x1="220" y1="114" x2="225.0" y2="114.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="232.0,114.0 225.0,117.2 225.0,110.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="232" y="96" width="100" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282.0" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">返回 20 条</text>
<text x="8" y="160" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">ICP：回表之前，先用索引里已有的列过滤</text>
<text x="8" y="180" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">EXPLAIN 的 Extra：Using index condition</text>
<text x="8" y="200" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">关闭 ICP 后变成 Using where</text>
</svg>
第一行是没有 ICP：先取出 user_id=5 的 5000 条，每条都回表，到 server 层才发现只有 20 条满足；第二行是有 ICP：在索引里就把 created_at 不满足的过滤掉，只回表 20 次。
**举个例子。** 某用户有 5000 条订单，只有 20 条满足 `created_at` 条件，索引是 `(user_id, status, created_at)`，查询没带 `status`：
1. **定位：** 用 `user_id=5` 在索引里找到这 5000 条，`created_at` 因跳过 status 不能继续定位。
2. **没有 ICP：** 5000 条每条都回表取整行，交给 server 层才过滤出 20 条，回表了 5000 次。
3. **有 ICP：** 引擎在索引里直接看每条的 `created_at`，满足的才回表，只回表 20 次。
4. **看 EXPLAIN：** 有 ICP 是 `Using index condition`；关掉后是 `Using where`，回表次数回到 5000。
**容易错。**
- **把 ICP 当成不回表：** ICP 仍然回表，只是回表前先过滤；不回表的是覆盖索引（`Using index`）。
- **以为 ICP 能让不连续的列用来定位：** `created_at` 跳过 `status` 仍然不能定位，只是能在索引里过滤。
- **以为主键索引也有 ICP：** 只作用于二级索引，聚簇索引上整行都在，本来就不需要回表。
- **条件列不在索引里也想下推：** 条件用到的列必须在索引里，否则引擎看不到。
