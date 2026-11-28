---
id: bagu-bitmap-hll-geo-1-bitmap-hll-geo
node: b.redis.bitmap-hll-geo
type: qa
step: 1
---
## Q
**Bitmap、HyperLogLog、Geo · 去重计数的取舍**｜追问

面试官：「直播间当日 UV、用户签到、附近的人，分别用 Redis 的什么结构？误差和内存各是多少？」

## A
**基本回答。** 签到、活跃用 Bitmap：用户 ID 就是位号，`SETBIT` 置 1，`BITCOUNT` 数人数，`BITOP` 对多日按位与或做交并（「连续两天活跃」就是两天求与）；`SETBIT` 到第 1 亿位约 12.5MB，ID 稀疏（如雪花 ID）时位数组要开到最大 ID 那么长，非常浪费。UV 近似去重用 HyperLogLog：`PFADD`、`PFCOUNT`，固定约 12KB，标准误差 0.81%；不存元素，对元素取哈希、数前导零个数（越多说明见过越多不同元素，像连续抛出很多正面），分到 16384 个桶各存最大值，取调和平均估数，所以不能列出元素也不能删除，`PFMERGE` 合并多天后不会重复计数；100 万个不同元素可能估出 1005024，误差约 0.5%。要精确名单用 Set，但百万元素就上百 MB。附近的人用 Geo：`GEOADD` 把经纬度转成 geohash 当 ZSet 的 score，`GEOSEARCH` 按半径或范围查，底层就是 ZSet。金额、对账不能有误差的统计不能用 HyperLogLog。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 256">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Bitmap：第 id 位等于 1，表示这个用户已签到</text>
<rect x="8" y="22" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="20" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="20" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="34" y="22" width="24" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="46" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="46" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="60" y="22" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="72" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="72" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<rect x="86" y="22" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="98" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="98" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<rect x="112" y="22" width="24" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="124" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="124" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<rect x="138" y="22" width="24" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="150" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="150" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<rect x="164" y="22" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="176" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="176" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<rect x="190" y="22" width="24" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="202" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="202" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7</text>
<rect x="216" y="22" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="228" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="228" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">8</text>
<rect x="242" y="22" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="254" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">9</text>
<rect x="268" y="22" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="280" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="280" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10</text>
<rect x="294" y="22" width="24" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="306" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="306" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">11</text>
<text x="8" y="90" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">HyperLogLog：只存统计量，固定约 12KB</text>
<rect x="8" y="98" width="56" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="36" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">元素</text>
<line x1="64" y1="116" x2="78" y2="116" stroke-width="1.2" stroke="currentColor"/>
<polygon points="78,116 71,119.2 71,112.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="78" y="98" width="112" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="134" y="112.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">哈希后数</text>
<text x="134" y="127.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">前导零个数</text>
<line x1="190" y1="116" x2="204" y2="116" stroke-width="1.2" stroke="currentColor"/>
<polygon points="204,116 197,119.2 197,112.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="204" y="98" width="100" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="254" y="112.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">16384 个桶</text>
<text x="254" y="127.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">各存最大值</text>
<text x="8" y="154" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">调和平均 → 估出不同元素数，标准误差 0.81%</text>
<text x="8" y="182" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Geo：底层是 ZSet，score 就是 geohash</text>
<rect x="8" y="190" width="84" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50" y="204.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">GEOADD</text>
<text x="50" y="219.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">经度 纬度</text>
<line x1="92" y1="208" x2="106" y2="208" stroke-width="1.2" stroke="currentColor"/>
<polygon points="106,208 99,211.2 99,204.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="106" y="190" width="84" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="148" y="204.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">geohash</text>
<text x="148" y="219.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">一个整数</text>
<line x1="190" y1="208" x2="204" y2="208" stroke-width="1.2" stroke="currentColor"/>
<polygon points="204,208 197,211.2 197,204.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="204" y="190" width="112" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="260" y="204.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ZSet</text>
<text x="260" y="219.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">member + score</text>
<text x="8" y="246" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">GEOSEARCH 按半径或范围查附近的人</text>
</svg>
三块是三种结构的核心：Bitmap 一排位，HyperLogLog 16384 个桶只存最大前导零数，Geo 的 geohash 作 ZSet 的 score。
**业务场景。** 直播间当日 UV 用 HyperLogLog，占 12KB、误差约 0.81%；对账要列出每个观众时改用 Set 或 Bitmap，多付内存。
**容易错。**
- **以为 HyperLogLog 能列出元素或是精确的。**
- **以为 Bitmap 对任何 ID 都省。**
- **以为 Geo 是新的底层结构。**
