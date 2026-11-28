---
id: hi-sdx-arch-faas-db-pressure
node: more.architecture
type: qa
step: 9
---
## Q
**函数无限扩张压垮数据库**｜补充 · 服务架构：微服务、服务发现、Serverless · 追问

面试官：「流量突增，FaaS 平台一下拉起 3000 个并发函数实例，后面的数据库被打趴了。结构性的问题是什么？两个标准解法？」

## A
**结论。** FaaS 的并发几乎瞬间扩出来，账户并发配额远高于数据库能承受的连接数；而关系库等下游的连接数和并发有硬上限，每个实例还各开自己的连接，伤害成倍放大。两个解法：限制并发并在触发源和函数之间放队列削峰；用连接代理（RDS Proxy、PgBouncer）把成千上万的实例连接复用成少量真实连接。

**要点。**
- **错配：** 实例无状态，各开各的连接。PostgreSQL 默认最多 100 个连接，3000 个实例一到就耗尽。
- **限制并发：** 给函数设最大并发（预留并发），超出的排队，而不是都冲向数据库。
- **队列削峰：** 队列放在触发器和函数之间，函数按队列的消费速度被调用，突发被缓冲而不是放大。
- **连接代理：** 连接池放在函数外面；事务级复用要注意依赖会话状态的功能会失效。
- **相关限制：** 单次执行有上限（Lambda 15 分钟）、不能持有长连接，WebSocket 要用托管网关。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 252">
<rect x="8" y="8" width="150" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="83.0" y="29.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">突增：3000 个并发实例</text>
<polyline points="83,42 83.0,63.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="83,70 79.8,63.0 86.2,63.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="92" y="62" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">各开一个连接</text>
<rect x="8" y="70" width="150" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="83.0" y="91.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库连接上限 100</text>
<text x="8" y="128" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">失败：连接耗尽，库被打垮</text>
<line x1="8" y1="142" x2="332" y2="142" stroke-width="1" stroke="currentColor" opacity="0.4" stroke-dasharray="3 3"/>
<rect x="8" y="156" width="76" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="46.0" y="171.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队列</text>
<text x="46.0" y="186.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">削峰</text>
<polyline points="84,175 93.0,175.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="100,175 93.0,178.2 93.0,171.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="100" y="156" width="76" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="138.0" y="171.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">限并发</text>
<text x="138.0" y="186.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">函数</text>
<polyline points="176,175 185.0,175.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="192,175 185.0,178.2 185.0,171.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="192" y="156" width="70" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="227.0" y="171.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">连接</text>
<text x="227.0" y="186.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">代理</text>
<polyline points="262,175 271.0,175.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="278,175 271.0,178.2 271.0,171.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="278" y="156" width="54" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="305.0" y="179.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<text x="8" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">队列控制进入速率，代理把几千个</text>
<text x="8" y="240" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">实例的连接复用成少量真实连接</text>
</svg>

**面试里这样说。** 「Serverless 把我的瓶颈变成了下游的灾难。我会给函数设最大并发，前面放队列做缓冲，数据库前面放连接代理，把几千个实例复用成几十个真实连接。」

**易错。**
- **只加大数据库规格：** 连接数上限和并发峰值都没变，只是推迟了崩溃。
- **在每个函数实例里建连接池：** 每个实例一个池，池再多也只是多占连接。
