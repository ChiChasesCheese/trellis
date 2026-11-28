---
id: bagu-short-link-1-design
node: b.scenario.short-link
type: qa
step: 1
---
## Q
**短链接系统 · 短码生成、跳转与热点**｜追问

面试官：「设计一个短链接服务：整体流程是什么？短码怎么生成，哈希、自增、雪花各有什么问题？热点链接怎么扛，怎么防被穷举？」

## A
**基本回答。** 写：长链接入库，取全局唯一数字 ID（号段取号：每个写实例一次向中心领一段连续编号，本地依次发放，中心只在领号时被访问），转 Base62（0-9、a-z、A-Z）得短码，存映射。读远多于写，重点在缓存：先本地缓存、再 Redis，未命中查库并回填，返回 302。哈希截断会撞码：6 位 Base62 共 62^6 ≈ 568 亿，但随机放 100 万条期望就有约 9 对撞码（生日悖论），撞了要重试；自增或号段 ID 唯一，转出的码必然唯一，7 位约 3.5 万亿；雪花 64 位转 Base62 要 11 位，太长。301 会被浏览器永久缓存，之后不再经过服务，统计不到点击也改不了目标；要统计或改目标用 302。访问呈 Zipf 分布，热点放进程内本地缓存再叠 Redis，不存在的码也缓存空值，防穿透。连续 ID 转出的短码相邻可猜，要置换或加盐打散并限流；过期短码回收要谨慎，避免旧链接指向新内容。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">写：长链接 → 短码</text>
<rect x="6" y="22" width="62" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="37.0" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">长链接</text>
<rect x="86" y="22" width="82" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="127.0" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">号段取 ID</text>
<rect x="186" y="22" width="62" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="217.0" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Base62</text>
<rect x="266" y="22" width="68" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="300.0" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">存映射</text>
<line x1="68" y1="37" x2="85" y2="37" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85.0,37.0 78.0,40.2 78.0,33.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="168" y1="37" x2="185" y2="37" stroke-width="1.2" stroke="currentColor"/>
<polygon points="185.0,37.0 178.0,40.2 178.0,33.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="248" y1="37" x2="265" y2="37" stroke-width="1.2" stroke="currentColor"/>
<polygon points="265.0,37.0 258.0,40.2 258.0,33.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="72" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">例：ID 1000000007 → 短码 15FTGn</text>
<text x="8" y="100" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">读：访问短码，逐层查</text>
<rect x="6" y="110" width="76" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="44.0" y="129.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">本地缓存</text>
<rect x="104" y="110" width="60" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="134.0" y="129.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis</text>
<rect x="186" y="110" width="70" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="221.0" y="129.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="278" y="110" width="56" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="306.0" y="129.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">302</text>
<line x1="82" y1="125" x2="103" y2="125" stroke-width="1.2" stroke="currentColor"/>
<polygon points="103.0,125.0 96.0,128.2 96.0,121.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="164" y1="125" x2="185" y2="125" stroke-width="1.2" stroke="currentColor"/>
<polygon points="185.0,125.0 178.0,128.2 178.0,121.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="256" y1="125" x2="277" y2="125" stroke-width="1.2" stroke="currentColor"/>
<polygon points="277.0,125.0 270.0,128.2 270.0,121.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="160" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">未命中才往右查；空值也缓存防穿透</text>
<text x="8" y="184" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">301：浏览器永久缓存，统计不到点击</text>
<text x="8" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">302：每次经过服务，可统计、可改目标</text>
<text x="8" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6 位 Base62 ≈ 568 亿个码；7 位 ≈ 3.5 万亿</text>
<text x="8" y="246" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">哈希截断：100 万条期望约 9 对撞码</text>
</svg>
上半部分是写：长链接拿号段发的 ID，转 Base62 短码，存映射。下面是读：本地缓存、Redis、数据库，返回 302。
**举个例子。** 号段取到 1000000007，反复除以 62 取余得 `15FTGn`，存 `15FTGn → 长链接`；首次访问本地缓存和 Redis 都没有，查库后回填并返回 302。运营推送后同一条被访问上亿次，本地缓存命中，数据库几乎不接读流量；访问不存在的码，空值缓存一小会儿，坏码反复来也不打库。
**容易错。**
- **用 301 又想统计点击：** 浏览器记住跳转，点击数统计不到。
- **忘了缓存空值：** 不存在的码每次都打到数据库。
