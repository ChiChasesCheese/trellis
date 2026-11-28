---
id: bagu-sharding-4-global-id
node: a.mysql.sharding
type: qa
step: 3
---
## Q
**分库分表 · 全局 ID、跨分片 join 与分页**｜必会

面试官：「分完之后自增 ID 会冲突，join 和分页也不好做，怎么处理？」

## A
**基本回答。** 全局 ID 用雪花算法（Snowflake）：1 位恒 0、41 位毫秒时间戳、10 位机器号、12 位序列号，各机自己发号不撞号；每机每毫秒 4096 个，整体趋势递增（不是绝对递增），主键插入接近顺序写、页分裂少。跨分片 join 在应用层分别查再合并，或在表里冗余字段；分页和排序让每个分片各取前 offset+limit 条，再在应用层归并。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 252">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">雪花 ID：64 位</text>
<rect x="8" y="22" width="36" height="40" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="26" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1 位</text>
<text x="26" y="53.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">恒 0</text>
<rect x="44" y="22" width="128" height="40" rx="2" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="108" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">41 位</text>
<text x="108" y="53.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">毫秒时间戳</text>
<rect x="172" y="22" width="80" height="40" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="212" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10 位</text>
<text x="212" y="53.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">机器号</text>
<rect x="252" y="22" width="80" height="40" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="292" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">12 位</text>
<text x="292" y="53.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">序列号</text>
<text x="8" y="82" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">每机每毫秒 4096 个，整体趋势递增</text>
<text x="8" y="100" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">41 位毫秒约够用 69.7 年；时钟回拨会重复</text>
<text x="8" y="126" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">深翻页：limit 10 offset 1000</text>
<rect x="8" y="134" width="100" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58" y="145.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分片1</text>
<text x="58" y="160.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">取前 1010 条</text>
<rect x="120" y="134" width="100" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="145.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分片2</text>
<text x="170" y="160.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">取前 1010 条</text>
<rect x="232" y="134" width="100" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282" y="145.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分片3</text>
<text x="282" y="160.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">取前 1010 条</text>
<line x1="58" y1="164" x2="164.133" y2="186.743" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,188.0 162.5,189.7 163.8,183.4" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="164" x2="170" y2="182" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,188.0 166.8,181.0 173.2,181.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="282" y1="164" x2="175.867" y2="186.743" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,188.0 176.2,183.4 177.5,189.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="40" y="188" width="260" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="206" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">应用层归并排序，取第 1001–1010 条</text>
<text x="8" y="240" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">翻得越深，每片取得越多</text>
</svg>
上半是 64 位划分，时间戳在高位所以整体随时间递增，41 位毫秒约够用 69.7 年。下半是深翻页：`limit 10 offset 1000` 每片取前 1010 条，3 片共 3030 条，应用层归并后取第 1001–1010 条，翻得越深越贵。
**时钟回拨。** 机器时钟往回调会发出重复 ID：发号器检测「当前时间小于上次」，回拨小就等待追上，回拨大就拒绝发号并告警，也可借用备用机器号位。
**业务场景。** 主播查「本月收到的全部礼物」翻到几千页，每个分片取前几万条，查询超时；限制深翻页、用游标分页（记住上一页最后的排序值），或改走搜索副本。
**容易错。**
- **以为雪花 ID 绝对递增：** 不同机器同一毫秒的先后不保证。
- **以为分页每片只取 10 条：** 要取前 offset+limit 条。
- **对各分片的 avg 再取平均：** 各片大小不同会算错；应各片返回 `(count, sum)`，再用总 sum 除以总 count。
