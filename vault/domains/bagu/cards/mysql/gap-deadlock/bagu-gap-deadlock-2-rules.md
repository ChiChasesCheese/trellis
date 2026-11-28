---
id: bagu-gap-deadlock-2-rules
node: a.mysql.gap-deadlock
type: qa
step: 2
---
## Q
**加锁规则 · 唯一索引和非唯一索引、等值和范围分别锁什么**｜必会

面试官：「RR 下，等值和范围查询，唯一索引和非唯一索引，分别加什么锁？没走索引呢？」

## A
**基本回答。** RR 下加锁的基本单位是 next-key 锁，部分情况会退化。唯一索引等值查询：命中就只加记录锁，没命中就对所在间隙加间隙锁。非唯一索引等值查询：命中的记录加 next-key 锁，再向右多扫一条，对第一个不满足条件的记录前面的间隙加间隙锁，并给对应的主键记录加记录锁。范围查询：扫描到的每条记录都加 next-key 锁，唯一索引的起点命中时退化为记录锁。没有可用索引：全表所有记录和间隙（包括最大值之后的 supremum 伪记录）都被锁，等于锁表。
规则随版本有差异（如 8.0.18 前唯一索引范围查询会多扫一行），以 `performance_schema.data_locks` 为准：`X,REC_NOT_GAP` 是记录锁，`X,GAP` 是间隙锁，`X` 是 next-key 锁。实测 8.0.46（id 为 1、5、10、15）：`id=5` 主键记录锁；`id=6` 主键 10 前的间隙锁；`id>=5 and id<10` 是 5 的记录锁加 10 前的间隙锁。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 238">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">主键 id 有 1、5、10、15：</text>
<rect x="20" y="24" width="28" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="34.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="90" y="24" width="28" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="104.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="160" y="24" width="28" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="174.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10</text>
<rect x="230" y="24" width="28" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="244.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">15</text>
<text x="8" y="70" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">id=5</text>
<rect x="90" y="60" width="28" height="14" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="126" y="72" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">只锁记录 5（REC_NOT_GAP）</text>
<text x="8" y="92" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">id=6</text>
<rect x="118" y="82" width="42" height="14" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="168" y="94" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">10 前的间隙（GAP）</text>
<text x="8" y="114" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">5≤id&lt;10</text>
<rect x="90" y="104" width="70" height="14" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="168" y="116" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">5 的记录锁 + 10 前的 GAP</text>
<text x="8" y="136" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">无索引</text>
<rect x="60" y="126" width="238" height="14" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="8" y="158" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">全部记录和间隙，含 supremum：等于锁全表</text>
<text x="8" y="184" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">非唯一索引 k=20：k 上 20 的 next-key</text>
<text x="8" y="202" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">再向右多扫一条：30 前加 GAP，主键 5 加记录锁</text>
<text x="8" y="220" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">k=25 没命中：只有 30 前的 GAP</text>
</svg>
主键上有 1、5、10、15 四条记录。三条高亮色条分别表示 `id=5`、`id=6`、`5≤id<10` 各自锁住的范围；最长的一条是没有索引时，锁住整张表的所有记录和间隙。下面三行补充了非唯一索引的情形。
**举个例子。** 表 `acct`，id 为 1、5、10、15，k 为 10、20、30、40：
1. **`id=5`：** 唯一索引命中，只锁主键上的记录 5。
2. **`id=6`：** 没命中，6 落在 5 和 10 之间，锁 10 前的 `GAP`。
3. **`id>=5 and id<10`：** 5 命中，退化为记录锁；继续扫到 10 发现不满足，所以在 10 前加间隙锁。
4. **`k=20`：** 非唯一索引，命中 20 加 next-key 锁 `(10,20]`；再向右多扫一条到 30，在 30 前加 `GAP`；回主键给 id=5 加记录锁。
5. **`k=25`：** 没命中，只锁 30 前的 `GAP`。
6. **`note=0`：** `note` 没有索引，扫全表，主键所有记录加 next-key，再加上 supremum，整张表被锁。
**容易错。**
- **以为等值查询只锁一行：** 没命中会锁间隙；非唯一索引还会多锁一段间隙和主键记录。
- **以为 `UPDATE` 没走索引也只改满足条件的行：** 扫描过的所有记录都被锁，等于锁表。
- **照背规则不看 `data_locks`：** 规则随版本有细节差异，以 `data_locks` 实测为准。
- **以为只锁二级索引：** 非唯一索引等值命中后，对应的主键记录也要加记录锁。
**业务场景。** 后台批量 `UPDATE orders SET status=2 WHERE note=0`，`note` 无索引，RR 下锁住全表记录和间隙，下单、支付全部排队超时；改走有索引的列，或在 RC 下分批执行。
