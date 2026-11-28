---
id: hi-sdx-ride-surge-precompute
node: sd.problem-breakdowns.uber.more
type: qa
step: 3
---
## Q
**动态加价：先算好再查表**｜补充 · 网约车（Uber） · 追问

面试官：「高峰期每秒约 1389 次叫车请求（4000 万单/天 ÷ 86400 × 3 的峰值系数）。动态加价的倍率，是每次请求时现算供需比，还是提前算好？」

## A
**结论。** 提前算好。供需比是对最近一段窗口内司机位置和未接订单的聚合，几秒内几乎不变；每次请求都现算，是在为几乎相同的结果反复付出昂贵的聚合成本。让流处理持续按格（H3）聚合，把「格 → 倍率」写进缓存，估价请求只做一次键查找。

**要点。**
- **流水线：** 位置和叫车事件进 Kafka，流处理（如 Flink）按 H3 格做滑动窗口，供给是空闲司机数，需求是最近的叫车数，两者相除得到倍率。
- **请求路径：** 估价时按乘客所在格读一次缓存，毫秒级，成本与请求量无关。
- **倍率要平滑：** 限制每个窗口的最大变化幅度，并参考邻格。六边形格到六个邻格的距离相同，比较供需梯度时没有方向偏差。
- **价格锁进估价：** 估价时把倍率写进 Fare，叫车只带 fareId，乘客看到的价格不会因为倍率变化而变。
- **流水线落后时：** 缓存带 TTL，数据过旧就退回基础价或上一个值，不退回现算。

**为什么。** 把「算」和「查」拆开：写路径持续、批量地更新，读路径只做一次查找。一个变化慢、算得贵、读得多的值，就该这样处理。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 286">
<rect x="20" y="10" width="170" height="32" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="105" y="30" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">司机位置 / 叫车事件</text>
<rect x="20" y="70" width="170" height="32" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<rect x="28" y="89" width="27.8" height="7" fill="none" stroke-width="1" stroke="currentColor"/>
<rect x="58.8" y="89" width="27.8" height="7" fill="none" stroke-width="1" stroke="currentColor"/>
<rect x="89.6" y="89" width="27.8" height="7" fill="none" stroke-width="1" stroke="currentColor"/>
<rect x="120.4" y="89" width="27.8" height="7" fill="none" stroke-width="1" stroke="currentColor"/>
<rect x="151.2" y="89" width="27.8" height="7" fill="none" stroke-width="1" stroke="currentColor"/>
<text x="105" y="83" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Kafka</text>
<rect x="20" y="130" width="170" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="105" y="148.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">流处理（如 Flink）</text>
<text x="105" y="163.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">按 H3 格滑动窗口聚合</text>
<path d="M20,208 a80,6 0 0 1 160,0 v32 a80,6 0 0 1 -160,0 z" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<path d="M20,208 a80,6 0 0 0 160,0" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="100" y="223.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">缓存：格 → 倍率</text>
<text x="100" y="238.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">带 TTL</text>
<rect x="244" y="214" width="84" height="32" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="286" y="234" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">估价请求</text>
<polyline points="105,42 105,70" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="105,70 101.8,63.0 108.2,63.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="105,102 105,130" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="105,130 101.8,123.0 108.2,123.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="100,174 100,202" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="100,202 96.8,195.0 103.2,195.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="108" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">写倍率</text>
<polyline points="244,230 180,230" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="180,230 187.0,226.8 187.0,233.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="212" y="222" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">GET 格</text>
<text x="8" y="272" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">供需比几秒内几乎不变：持续算好，请求只查表</text>
</svg>

**面试里这样说。** 「峰值约 1389 次请求每秒，但每个格的供需比几秒才变一次，所以我不现算。事件进 Kafka，用 Flink 按 H3 格做滑动窗口算倍率，写进缓存，估价时只读一次。倍率在估价时写进 Fare，叫车用 fareId 取价，乘客看到的价格不会变。」

**易错。**
- **每次请求现算：** 同一个格同一个窗口的聚合被重复计算成千上万次。
- **倍率不锁进估价：** 乘客下单时价格又变了，投诉和纠纷由此而来。
- **邻格倍率不平滑：** 街对面价格相差很多，边界上出现价格悬崖。
