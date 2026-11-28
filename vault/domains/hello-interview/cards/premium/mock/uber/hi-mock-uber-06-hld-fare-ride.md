---
id: hi-mock-uber-06-hld-fare-ride
node: sd.problem-breakdowns.uber.mock
type: qa
step: 6
---
## Q
**网约车 · 第 6 步 · 高层设计（一）：估价与叫车**｜模拟面试

面试官：「很好，现在开始画高层设计，从第一条功能开始。」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先定打法：** 「我按功能一条条往上叠，先让功能跑通，再用非功能需求带出深入问题。」
- **画四个框：** 「乘客客户端、API 网关、叫车服务（Ride Service）、数据库；叫车服务还要调第三方地图 API。」
- **网关做什么：** 「它是入口，负责鉴权、限流，再按路径把请求路由到对应的微服务。」
- **走估价：** 「乘客输入起终点，客户端 `POST /fare`；网关鉴权限流后转给叫车服务；叫车服务调地图 API 拿距离和耗时，套定价模型算出估价和 ETA；写一条 Fare；沿原路返回给客户端。定价模型我抽象成一个函数，不展开。」
- **数据库先不纠结：** 「Fare 和 Ride 是普通事务数据，量不大，PostgreSQL 或 DynamoDB 都行，我先写一个『数据库』。」
- **走叫车：** 「乘客确认后 `POST /rides` 带 fareId。不用加新服务，只在库里加一张 Ride 表：叫车服务建一行，关联这条 Fare，状态 requested。」
- **下一步：** 「然后它触发匹配。这一步下一张图画；现在先这样，它能丢请求，等深入时我再处理。」
**白板。**
**第一张：估价。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 404">
<rect x="18" y="8" width="100" height="36" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="68" y="22.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">乘客客户端</text>
<text x="68" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Rider Client</text>
<rect x="18" y="72" width="304" height="28" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">API 网关 · 鉴权 · 限流 · 路由</text>
<rect x="18" y="164" width="96" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="66" y="180.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">叫车服务</text>
<text x="66" y="195.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Ride Service</text>
<rect x="132" y="164" width="72" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="168" y="180.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">地图 API</text>
<text x="168" y="195.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">距离耗时</text>
<path d="M18,248 a50,6 0 0 1 100,0 v74 a50,6 0 0 1 -100,0 z" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<path d="M18,248 a50,6 0 0 0 100,0" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="68" y="266" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="26" y="282" width="84" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="68" y="296" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Fare 表</text>
<polyline points="68,44 68,72" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="68,72 64.8,65.0 71.2,65.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="74" y="62" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">① POST /fare</text>
<polyline points="68,100 68,164" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="68,164 64.8,157.0 71.2,157.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="74" y="138" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">② 转发</text>
<polyline points="114,184 132,184" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="132,184 125.0,187.2 125.0,180.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polyline points="34,204 34,242" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="34,242 30.8,235.0 37.2,235.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="40" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">④ 写 Fare</text>
<polyline points="18,184 10,184 10,26 18,26" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="18,26 11.0,29.2 11.0,22.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="116" y="176" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">③</text>
<text x="8" y="352" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">① 乘客发起估价  ② 网关鉴权限流后转发</text>
<text x="8" y="368" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">③ 查地图得距离和耗时，再套定价模型</text>
<text x="8" y="384" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">④ 写入 Fare  ⑤ 虚线：沿原路返回 Fare</text>
</svg>
白板上新增：客户端、网关、叫车服务、地图 API、数据库（含 Fare 表），以及五步编号。

**第二张：叫车。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 520">
<rect x="18" y="8" width="100" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="68" y="22.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">乘客客户端</text>
<text x="68" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Rider Client</text>
<rect x="18" y="72" width="304" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">API 网关 · 鉴权 · 限流 · 路由</text>
<rect x="18" y="164" width="96" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="66" y="180.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">叫车服务</text>
<text x="66" y="195.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Ride Service</text>
<rect x="132" y="164" width="72" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="168" y="180.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">地图 API</text>
<text x="168" y="195.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">距离耗时</text>
<path d="M18,248 a50,6 0 0 1 100,0 v74 a50,6 0 0 1 -100,0 z" stroke-width="1.2" fill="none" stroke="currentColor"/>
<path d="M18,248 a50,6 0 0 0 100,0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<text x="68" y="266" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="26" y="282" width="84" height="20" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="68" y="296" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Fare 表</text>
<rect x="26" y="304" width="84" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="68" y="318" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Ride 表</text>
<polyline points="68,44 68,72" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="68,72 64.8,65.0 71.2,65.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="74" y="52" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">POST /fare</text>
<text x="74" y="66" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">⑥ POST /rides</text>
<polyline points="68,100 68,164" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="68,164 64.8,157.0 71.2,157.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="114,184 132,184" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="132,184 125.0,187.2 125.0,180.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="34,204 34,242" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="34,242 30.8,235.0 37.2,235.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="40" y="218" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">写 Fare</text>
<text x="40" y="234" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">⑦ 写 Ride</text>
<polyline points="18,184 10,184 10,26 18,26" fill="none" stroke-width="1.3" stroke-dasharray="4 3" stroke="currentColor"/>
<polygon points="18,26 11.0,29.2 11.0,22.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="222" y="368" width="100" height="60" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="272" y="394.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">匹配服务</text>
<text x="272" y="409.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">下一步画</text>
<polyline points="112,204 112,222 170,222 170,378 222,378" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="222,378 215.0,381.2 215.0,374.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="164" y="352" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">⑧ 触发匹配</text>
<text x="8" y="452" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">⑥ 乘客确认估价，只带 fareId</text>
<text x="8" y="468" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">⑦ 叫车服务建一行 Ride，状态 requested，</text>
<text x="8" y="484" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">   关联这条 Fare</text>
<text x="8" y="500" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">⑧ 然后触发匹配（虚线，下一步画）</text>
</svg>
白板上新增：库里的 Ride 表、两条标蓝的叫车调用，和一个虚线的匹配服务，留给下一步。
**为什么这样说。** （约 6 分钟，累计第 16 分钟。）面试官看你是不是按需求一条条往上叠，每画一个框都知道它做什么，数据怎么流。强的回答边画边讲，并且主动说出「这里还有个坑，留到深入讲」。弱的回答一上来就把 Kafka、Redis、缓存全画上，却讲不清最基本的请求怎么走。
**面试官可能接着问。**
- Fare 为什么要落库？ → 乘客是对着一个估价叫车的，叫车时我按 fareId 回库读价格，防止客户端篡改；落库后还能设过期时间。
- 地图 API 慢或挂了呢？ → 给调用设超时；超时就用按直线距离估算的价格或缓存的热门路线兜底。估价不要求精确，叫车才要求。
- 叫车服务触发匹配时崩了呢？ → 现在会丢，这是已知缺口。深入三我用队列解决：先入队，匹配成功才确认。
**常见失分。**
- **一上来画满：** 还没讲清请求怎么走，就画 Kafka、Redis，面试官看到的是堆砌，不是推理。
- **网关一笔带过：** 画了不说它做什么，面试官很可能追问。至少说出鉴权、限流、路由。
- **客户端传价格：** 叫车时让客户端带估价，等于让用户自己定价。
