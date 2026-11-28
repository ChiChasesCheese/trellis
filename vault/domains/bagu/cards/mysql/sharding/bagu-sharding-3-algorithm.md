---
id: bagu-sharding-3-algorithm
node: a.mysql.sharding
type: qa
step: 5
---
## Q
**分库分表 · 分片算法与扩容**｜追问

面试官：「取模、一致性哈希、预分逻辑片，你选哪个？扩容时各有什么问题？」

## A
**基本回答。** 取模最简单、分布均匀，但改库数几乎全量迁移（3 库改 4 库约四分之三的行要搬）；一致性哈希扩容只动环上相邻一段，但负载不均，要加虚拟节点；常用做法是预分 2^n 个逻辑分片（如 32 库 × 32 表 = 1024 张表），再映射到较少的物理机，扩容只搬整个逻辑库，路由规则不变。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 256">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">取模：3 库改 4 库，约 3/4 的行要换位置</text>
<text x="8" y="37" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">id</text>
<rect x="44" y="22" width="34" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="61" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="80" y="22" width="34" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="97" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="116" y="22" width="34" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="133" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="152" y="22" width="34" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="169" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="188" y="22" width="34" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="205" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="224" y="22" width="34" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="241" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="260" y="22" width="34" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="277" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="296" y="22" width="34" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="313" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<text x="8" y="61" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">%3</text>
<rect x="44" y="46" width="34" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="61" y="60" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="80" y="46" width="34" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="97" y="60" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="116" y="46" width="34" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="133" y="60" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="152" y="46" width="34" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="169" y="60" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="188" y="46" width="34" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="205" y="60" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="224" y="46" width="34" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="241" y="60" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="260" y="46" width="34" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="277" y="60" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="296" y="46" width="34" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="313" y="60" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="8" y="85" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">%4</text>
<rect x="44" y="70" width="34" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="61" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="80" y="70" width="34" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="97" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="116" y="70" width="34" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="133" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="152" y="70" width="34" height="20" rx="2" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="169" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="188" y="70" width="34" height="20" rx="2" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="205" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="224" y="70" width="34" height="20" rx="2" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="241" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="260" y="70" width="34" height="20" rx="2" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="277" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="296" y="70" width="34" height="20" rx="2" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="313" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="8" y="112" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">逻辑分片：32 库 × 32 表，id = 259</text>
<rect x="8" y="120" width="150" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="83" y="139" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">id % 32 = 3 → 库 3</text>
<rect x="182" y="120" width="150" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="257" y="139" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">id / 32 % 32 = 8 → 表 8</text>
<text x="8" y="174" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">扩容：只搬整个逻辑库，路由规则不变</text>
<rect x="8" y="182" width="100" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58" y="194.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">机器 A</text>
<text x="58" y="209.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">库 0–31</text>
<line x1="108" y1="198" x2="136" y2="198" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="142.0,198.0 135.0,201.2 135.0,194.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="146" y="182" width="88" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="190" y="194.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">机器 A</text>
<text x="190" y="209.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">库 0–15</text>
<rect x="244" y="182" width="88" height="32" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="288" y="194.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">机器 B</text>
<text x="288" y="209.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">库 16–31</text>
<text x="8" y="238" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">迁整库、改配置里的库地址即可</text>
</svg>
上半：同一个 id 在 3 库和 4 库下落点不同，深色格是换了位置的。中下：路由 `id % 32` 取库、`id / 32 % 32` 取表，id=259 落在库 3、表 8；扩容时把库 16–31 整个搬到新机器，路由不变。
**容量与代价。** 1024 张表 × 500 万行约 50 亿行；每库 1000–1500 写 QPS，32 库约 3.2–4.8 万（量级估算，要压测）。起步时 32 个库可以放在同一台 MySQL 上。代价是改表结构要对所有分片执行，连接数和运维成本增加。
**扩容步骤。** 给要迁走的库建从库，追平后短暂停写或切换路由，把配置里的库地址指向新机器，再清理原库多余的分片；切换前校验数据一致并灰度。
**业务场景。** 直播间礼物流水原来 3 库取模，大促前扩到 4 库：前 8 个 id 里只有 id 0、1、2 落点不变，5 个要搬。逻辑分片方案只需把库 16–31 迁走，id=259 仍是库 3、表 8，应用代码不改。
**容易错。**
- **以为一致性哈希最好：** 迁移量小但负载不均，业务库更常用预分逻辑片。
- **起步分片数定太小：** 以后改分片数要重新分布全部数据。
- **以为逻辑分片要一开始买很多机器：** 可以先放同一台，之后再迁。
