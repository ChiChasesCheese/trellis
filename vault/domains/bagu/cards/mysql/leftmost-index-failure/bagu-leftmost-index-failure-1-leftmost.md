---
id: bagu-leftmost-index-failure-1-leftmost
node: a.mysql.leftmost-index-failure
type: qa
step: 1
---
## Q
**联合索引 · 最左前缀是什么，哪些查询用得上**｜必会

面试官：「订单表有联合索引 `(user_id, status, created_at)`。只带 `status`、带 `user_id` 和 `created_at`、`user_id` 等值加 `status` 范围再加 `created_at`，各能用上几列？」

## A
**基本回答。** 联合索引 `(a, b, c)` 在 B+ 树里先按 a 排序，a 相同再按 b 排，b 也相同再按 c 排。只有从最左开始、连续的列才能用来定位，这就是最左前缀原则：`a=`、`a= and b=`、`a= and b= and c=`、`a=` 加 `b` 范围都能用；只写 `b=` 或 `c=` 不能定位。范围条件之后的列也不能再定位，`a=1 and b>5 and c=3` 里的 c 只能靠索引下推（ICP）在索引里过滤。
例外：MySQL 8.0.13 起最左列不同值很少时有跳跃扫描（Extra `Using index for skip scan`），只是机会性优化，别依赖；PostgreSQL 18 也有 skip scan，前导列基数高时仍会全表扫描。`key_len` 速算：bigint 8、tinyint 1、datetime 5，允许 NULL 再加 1，把用到的列加起来就知道用了几列。
**2026 亮点。** PostgreSQL 18 的 B 树也支持 skip scan，思路同 MySQL：前导列不同值很少时，只带后列的查询可能用上联合索引；前导列基数高时仍多半全表扫描，所以列序仍按「等值、高选择性在前」设计，不靠 skip scan 救场。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 216">
<text x="35" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">user_id</text>
<text x="96" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">status</text>
<text x="158" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">created_at</text>
<rect x="8" y="28" width="62" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="39.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="70" y="28" width="52" height="22" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="96.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="122" y="28" width="72" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="158.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t1</text>
<text x="204" y="43" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">← status=1</text>
<rect x="8" y="50" width="62" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="39.0" y="65.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="70" y="50" width="52" height="22" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="96.0" y="65.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="122" y="50" width="72" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="158.0" y="65.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t3</text>
<text x="204" y="65" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">← status=1</text>
<rect x="8" y="72" width="62" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="39.0" y="87.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="70" y="72" width="52" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="96.0" y="87.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="122" y="72" width="72" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="158.0" y="87.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t2</text>
<rect x="8" y="94" width="62" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="39.0" y="109.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="70" y="94" width="52" height="22" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="96.0" y="109.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="122" y="94" width="72" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="158.0" y="109.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t1</text>
<text x="204" y="109" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">← status=1</text>
<rect x="8" y="116" width="62" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="39.0" y="131.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="70" y="116" width="52" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="96.0" y="131.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="122" y="116" width="72" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="158.0" y="131.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t4</text>
<rect x="8" y="138" width="62" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="39.0" y="153.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<rect x="70" y="138" width="52" height="22" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="96.0" y="153.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="122" y="138" width="72" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="158.0" y="153.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">t2</text>
<text x="204" y="153" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">← status=1</text>
<text x="8" y="178" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">user_id=5 → 连续的前 3 行，能定位</text>
<text x="8" y="198" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">只有 status=1 → 命中散在各处，只能全扫</text>
</svg>
索引 `(user_id, status, created_at)` 排好的样子：先按 user_id 排，同一 user_id 里再按 status 排。`user_id=5` 对应连续的前三行，能直接定位；`status=1` 的行（高亮）散落在各处，没法定位。
**举个例子。** 索引里排好的条目是 `(5,1,t1)`、`(5,1,t3)`、`(5,2,t2)`、`(7,1,t1)`、`(7,2,t4)`、`(9,1,t2)`：
1. **`user_id=5`：** 在树里二分找到 5 开头的位置，连续的前 3 行都满足，直接定位。
2. **`user_id=5 and status=1`：** 在这 3 行里 status=1 是前 2 行，仍然是连续的一小段，两列都用上。
3. **只写 `status=1`：** 满足的行是第 1、2、4、6 行，散在各处，树里没有「status=1 从哪开始」的位置，只能全表扫描。
4. **用 user_id 加 created_at：** 先用 user_id 定位 3 行，这 3 行里 created_at 是 t1、t3、t2，并没有排好（因为中间隔着 status），所以 `created_at` 不能定位，只能逐条过滤。
5. **user_id 等值加 status 范围：** 用 user_id 和 status 范围定位，status 之后的 created_at 同样只能过滤。
**容易错。**
- **以为只要列在索引里就能用：** 必须从最左开始连续才能定位，跳过中间的列，后面的列就只能过滤。
- **以为 `WHERE` 里写的顺序重要：** 优化器会重排条件，`status=1 and user_id=5` 和 `user_id=5 and status=1` 都能用上。
- **以为范围之后的列还能定位：** 范围（`>`、`<`、`between`）会跨过多个值，后面的列不再有序，只能靠 ICP 过滤。
- **依赖跳跃扫描：** 它只在最左列不同值很少时才可能被用上，常用查询仍要单独建索引。
