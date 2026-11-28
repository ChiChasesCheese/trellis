---
id: hi-fix-recon-sweep-02-sweep-selection
node: fix.recon-sweep
type: qa
step: 2
---
## Q
**回调是常态路径 · 扫描选谁**｜补强

面试官：「你说每天跑一个扫描任务，兜底丢失的回调。它到底扫哪些行？这张表一年有五亿行。」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **选择规则写成一条查询：** 「status = 'pending'，并且 created_at 早于 1 小时前。webhook 通常几分钟内到，1 小时还没到才算可疑；1 小时是我的假设，随平台的说法改。」
- **1 小时以上的 pending 有多少：** 「每天 1,430,000 笔转账，假设 1% 会超过 1 小时，约 14,300 笔。」
- **索引：** 「在 (status, created_at) 上建索引，查询是对 pending 的一次范围扫描，只读这 14,300 笔；没有它，就是在一年 5.2 亿行的表上全表扫描。」
- **分批：** 「按 created_at 排序，每批 500 行，记住游标，约 29 批；任务中断了可以从游标继续。」
- **每一行怎么处理：** 「有 vendor_transfer_id 就按它问平台，没有就按我方引用号 transaction_id 问；拿到终态，套用 webhook 同一个事务。」
- **幂等：** 「扫描和 webhook 同时处理一行也没关系：两边都是 WHERE status = 'pending' 的条件更新，只有一个影响 1 行。」
**白板。**
```
CREATE INDEX ON transactions
  (status, created_at);

SELECT id, vendor_transfer_id, created_at
FROM transactions
WHERE status = 'pending'
  AND created_at
      < now() - interval '1 hour'
  AND created_at >= $cursor
ORDER BY created_at
LIMIT 500;
-- 游标用 >=：同一时刻的行不漏，
-- 重查一行无害，因为处理是幂等的
```

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 216">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">扫描选谁：三个条件</text>
<rect x="8" y="26" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">status = 'pending'</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">只看还没收尾的</text>
<rect x="8" y="78" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="96.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">created_at &lt; now() − 1 小时</text>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">webhook 通常几分钟内到；</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1 小时没到才算可疑（我的假设）</text>
<rect x="8" y="145" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="163.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">按 created_at 排序，每批 500</text>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">记住游标，下一批从游标之后取</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">14,300 笔 ÷ 500 ≈ 29 批</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 164">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">有没有 (status, created_at) 索引</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">没有索引</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">扫 520,000,000 行/年（≈ 260 GB）</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">每天一次全表，数据库被拖住</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">有索引</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">范围扫描：status = pending 且够老</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">只读约 14,300 个索引项和对应的行</text>
</svg>
白板上：三个条件，旁边是有无索引的对比。
**为什么这样说。** （约 1 分钟。）面试官在看「扫一下」能不能变成一条他能读的查询。强的回答给出条件、索引和批次，并说出每天大概扫多少行；弱的回答是「定时扫 pending 的」，没有说怎么找、找多少。
**面试官可能接着问。**
- 这个索引会不会拖慢写入？ → 每笔转账会改一次 status，索引多一次维护；可以改成只含 pending 行的部分索引，它很小，终态行不在里面。
- 扫描时 pending 行被 webhook 改掉了呢？ → 查询看到的是旧状态，处理时条件更新影响 0 行，当作已处理，没有副作用。
- 为什么要 created_at < 1 小时？ → 没有它，会把刚创建、正在处理的行也去问平台，白白消耗额度。
**常见失分。**
- **扫全表：** 一年 5.2 亿行，一次扫描就拖慢线上。
- **没有排序和游标：** 中途失败只能从头来。
- **条件里没有龄：** 扫描把正常在处理的行也都问一遍。
