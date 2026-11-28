---
id: hi-fix-component-cost-05-uber-driver-geo
node: fix.component-cost
type: qa
step: 5
---
## Q
**Uber · 加组件：Redis 里的司机位置**｜补强

面试官：「司机每 5 秒上报一次位置，叫车时要找附近的司机。你怎么存？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **算写入量：** 「假设 100 万在线司机，每 5 秒一次：1,000,000 ÷ 5 = 每秒 20 万次。」
- **先说库的版本：** 「写主库每秒 20 万次，而且每条数据 5 秒就作废，不值得持久化。」
- **职责：** 「我加 Redis 的地理索引：上报时 GEOADD，叫车时 GEOSEARCH 找附近的司机。」
- **新问题：** 「数据是短命的：司机掉线后位置还留着，叫车会匹配到幽灵；Redis 重启也会丢。」
- **处理：** 「每个司机记 last_seen，清理任务删掉超过 15 秒的，查询时也过滤。重启丢了没关系，司机 5 秒内重新上报就长回来。」
- **分片：** 「单实例按每秒 10 万次算（这是假设，要压测）：20 万次至少 2 个，留余量取 4；按地理格分，不按整座城市。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 358">
<rect x="8" y="8" width="324" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">司机 App</text>
<text x="170" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每 5 秒上报一次位置</text>
<rect x="8" y="80" width="324" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="96.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">位置服务</text>
<text x="170" y="111.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">GEOADD + 记 last_seen</text>
<path d="M8,158 a77,6 0 0 1 154,0 v68 a77,6 0 0 1 -154,0 z" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<path d="M8,158 a77,6 0 0 0 154,0" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="85" y="176" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis · 城市 A</text>
<path d="M178,158 a77,6 0 0 1 154,0 v68 a77,6 0 0 1 -154,0 z" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<path d="M178,158 a77,6 0 0 0 154,0" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="255" y="176" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis · 城市 B</text>
<rect x="14" y="190" width="142" height="22" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="85" y="205" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">drivers · 地理索引</text>
<rect x="184" y="190" width="142" height="22" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="255" y="205" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">drivers · 地理索引</text>
<polyline points="60,48 60,80" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="60,80 56.8,73.0 63.2,73.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="66" y="68" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">POST /location</text>
<polyline points="80,120 80,152" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="80,152 76.8,145.0 83.2,145.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polyline points="250,120 250,152" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="250,152 246.8,145.0 253.2,145.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="8" y="264" width="324" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="280.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">清理任务</text>
<text x="170" y="295.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">删掉 last_seen 超过 15 秒的司机</text>
<polyline points="170,264 170,232" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,232 173.2,239.0 166.8,239.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="328" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">上报写入：100 万司机 ÷ 5 秒 = 20 万次/秒</text>
<text x="8" y="346" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">单实例按 10 万/秒（假设）：至少 2 个，留余量取 4</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 112">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">我要写在组件旁边的四行</text>
<rect x="8" y="26" width="324" height="76" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">加：Redis 地理索引，存司机位置</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">为了：GEOSEARCH 找附近的司机</text>
<text x="18" y="75.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">新问题：数据短命，司机掉线留下幽灵</text>
<text x="18" y="90.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">处理：last_seen 清理；重启 5 秒内自己长回</text>
</svg>
白板上：上报路径写入两个 Redis 分片，清理任务旁路扫描；下面是写入量算式。
**为什么这样说。** （约 1 分钟。）面试官看你有没有区分「持久化的数据」和「短命的数据」。强的回答说位置 5 秒就作废，所以放在内存里，并说清掉线和重启怎么收口。弱的回答是把位置写进数据库。
**面试官可能接着问。**
- 为什么不持久化位置？ → 5 秒就过期，持久化的成本大于价值。行程和结算才是要持久化的数据，写数据库。
- 司机在两个格子的交界处？ → 查询时把相邻的格子一起查。
- 热点城市一个实例扛不住？ → 分片键用地理格而不是城市，把热点城市的格子分散到多个实例上。
**常见失分。**
- **把位置写主库：** 写入量和数据寿命都不匹配。
- **忘了清理：** 掉线的司机会被一直匹配。
- **不说重启：** 内存数据丢了，要说明为什么没关系。
