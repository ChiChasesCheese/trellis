---
id: bagu-keys-scan-1-keys-vs-scan
node: b.redis.keys-scan
type: qa
step: 1
---
## Q
**KEYS 与 SCAN · 为什么线上不能用 KEYS**｜追问

面试官：「运营想统计某活动前缀的 key 数量，直接 KEYS 一下可以吗？SCAN 有什么特点，怎么批量删除？」

## A
**基本回答。** 不可以。`KEYS` 是 O(N)，单线程遍历整个键空间，期间所有请求排队；200 万个 key 一次阻塞约 83 毫秒（量级），越多越久。`SCAN cursor MATCH p COUNT n` 用游标分批，返回「新游标 + 一批 key」，游标回到 0 才结束。`COUNT` 只是每次迭代扫多少个槽的提示，不是返回条数；`MATCH` 在扫描之后过滤，所以常有空批次，只要游标不是 0 就要继续。保证：遍历全程一直存在的 key 一定返回，期间新增或删除的可能出现也可能不出现；rehash 期间同一个 key 可能返回多次，业务要去重、处理幂等。大集合用 `SSCAN`、`HSCAN`、`ZSCAN`。批量删某前缀：从库 `SCAN` 出 key，主库 `UNLINK` 分批删（先摘 key、内存释放交后台线程），每批几百个，批间 sleep，可重复执行，不要 `KEYS`，也不对大集合用 `DEL`。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 212">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">KEYS：一把扫完整个键空间</text>
<rect x="8" y="22" width="324" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">单线程扫 200 万个 key，阻塞约 83 毫秒</text>
<text x="8" y="68" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">这段时间其他请求全部排队</text>
<text x="8" y="96" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">SCAN：游标分批，每批之间别人可以插进来</text>
<rect x="8" y="106" width="76" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="46" y="120.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SCAN 0</text>
<text x="46" y="135.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">得到游标 17</text>
<line x1="84" y1="124" x2="98" y2="124" stroke-width="1.2" stroke="currentColor"/>
<polygon points="98,124 91,127.2 91,120.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="98" y="106" width="76" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="136" y="120.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SCAN 17</text>
<text x="136" y="135.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">得到游标 52</text>
<line x1="174" y1="124" x2="188" y2="124" stroke-width="1.2" stroke="currentColor"/>
<polygon points="188,124 181,127.2 181,120.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="188" y="106" width="76" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="226" y="120.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SCAN 52</text>
<text x="226" y="135.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">得到游标 0</text>
<line x1="264" y1="124" x2="278" y2="124" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="278,124 271,127.2 271,120.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="278" y="106" width="54" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="305" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">结束</text>
<text x="8" y="166" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">可能返回重复 key，要去重、处理幂等</text>
<text x="8" y="184" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">MATCH 在扫描之后过滤，可能返回空批次</text>
<text x="8" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">游标回到 0 才结束，不看批次是否为空</text>
</svg>
上半 `KEYS` 一次占满主线程；下半 `SCAN` 每次拿上次游标继续，其间别的请求可以插进来。
**业务场景。** 运营直接 `KEYS` 统计活动前缀，主库阻塞数秒，支付回调超时；改成 `SCAN MATCH act:2026:* COUNT 100` 分批统计：某批可能返回游标 37 和 0 个 key（不匹配），不能当结束，一直扫到游标 0，所有批次的 key 放集合去重后再计数。
**容易错。**
- **以为 COUNT 是返回条数。**
- **以为空数组就是扫完了。**
- **以为 SCAN 不会重复，或能给某一刻的快照。**
