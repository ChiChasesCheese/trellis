---
id: hi-mock-uber-07-hld-match-accept
node: sd.problem-breakdowns.uber.mock
type: qa
step: 7
---
## Q
**网约车 · 第 7 步 · 高层设计（二）：匹配与司机接单**｜模拟面试

面试官：「叫车之后呢？系统怎么找到司机，司机又怎么接单？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **新增四块：** 「司机客户端、位置服务（Location Service）、匹配服务（Ride Matching Service）、通知服务（Notification Service）。」
- **位置怎么来：** 「司机端一直把当前位置发给位置服务，位置服务先写进数据库，保证库里总有每个司机的最新经纬度。位置表我单独画一个框，因为后面要改它。」
- **匹配：** 「叫车服务建好行程后，转给匹配服务。它用最新位置查最近的空闲司机，按距离、是否空闲、评分排成一个候选名单。排序算法我抽象掉。」
- **通知：** 「通知服务通过 APNs 和 FCM，把订单推给排第一的司机。」
- **接单：** 「司机接受，就 `PATCH /rides/:id`；网关转给叫车服务，状态改成 accepted、写入司机，返回上车点，司机用端上 GPS 导航。」
- **拒绝或没响应：** 「就推给名单里的下一位。」
- **主动留白：** 「这一版有三处我先不管，等下深入讲：位置每秒 200 万次写入；多个匹配实例可能同时问同一个司机；匹配请求会丢。」
**白板。**
**第一张：匹配。**
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
<polyline points="68,100 68,164" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="68,164 64.8,157.0 71.2,157.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="114,184 132,184" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="132,184 125.0,187.2 125.0,180.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="34,204 34,242" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="34,242 30.8,235.0 37.2,235.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="40" y="228" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">写库</text>
<polyline points="68,44 68,72" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="68,72 64.8,65.0 71.2,65.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="18,184 10,184 10,26 18,26" fill="none" stroke-width="1.3" stroke-dasharray="4 3" stroke="currentColor"/>
<polygon points="18,26 11.0,29.2 11.0,22.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="74" y="118" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">POST /fare, /rides</text>
<path d="M18,248 a50,6 0 0 1 100,0 v74 a50,6 0 0 1 -100,0 z" stroke-width="1.2" fill="none" stroke="currentColor"/>
<path d="M18,248 a50,6 0 0 0 100,0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<text x="68" y="266" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="26" y="282" width="84" height="20" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="68" y="296" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Fare 表</text>
<rect x="26" y="304" width="84" height="20" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="68" y="318" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Ride 表</text>
<rect x="222" y="8" width="100" height="36" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="272" y="22.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">司机客户端</text>
<text x="272" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Driver Client</text>
<rect x="222" y="164" width="100" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="272" y="180.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">位置服务</text>
<text x="272" y="195.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Location</text>
<path d="M222,248 a50,6 0 0 1 100,0 v74 a50,6 0 0 1 -100,0 z" stroke-width="1.2" fill="none" stroke="currentColor"/>
<path d="M222,248 a50,6 0 0 0 100,0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<text x="272" y="266" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="230" y="282" width="84" height="22" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="272" y="297" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Location 表</text>
<rect x="222" y="368" width="100" height="60" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="272" y="394.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">匹配服务</text>
<text x="272" y="409.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Matching</text>
<polyline points="272,44 272,72" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="272,72 268.8,65.0 275.2,65.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polyline points="272,100 272,164" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="272,164 268.8,157.0 275.2,157.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="266" y="148" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">POST /drivers/location</text>
<polyline points="272,204 272,242" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="272,242 268.8,235.0 275.2,235.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="278" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">写位置</text>
<polyline points="250,368 250,328" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="250,328 253.2,335.0 246.8,335.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="256" y="352" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">查近邻</text>
<polyline points="112,204 112,222 170,222 170,378 222,378" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="222,378 215.0,381.2 215.0,374.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="164" y="352" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">触发匹配</text>
<text x="8" y="452" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">司机端一直上报位置，位置服务写进库；</text>
<text x="8" y="468" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">叫车服务建好行程后转给匹配服务，</text>
<text x="8" y="484" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">匹配服务按位置查最近的空闲司机</text>
</svg>
白板上新增：司机客户端、位置服务、位置表、匹配服务，以及三条蓝色调用。

**第二张：接单。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 630">
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
<polyline points="68,100 68,164" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="68,164 64.8,157.0 71.2,157.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="114,184 132,184" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="132,184 125.0,187.2 125.0,180.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="34,204 34,242" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="34,242 30.8,235.0 37.2,235.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="40" y="228" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">写库</text>
<polyline points="68,44 68,72" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="68,72 64.8,65.0 71.2,65.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="18,184 10,184 10,26 18,26" fill="none" stroke-width="1.3" stroke-dasharray="4 3" stroke="currentColor"/>
<polygon points="18,26 11.0,29.2 11.0,22.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="74" y="118" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">POST /fare, /rides</text>
<path d="M18,248 a50,6 0 0 1 100,0 v74 a50,6 0 0 1 -100,0 z" stroke-width="1.2" fill="none" stroke="currentColor"/>
<path d="M18,248 a50,6 0 0 0 100,0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<text x="68" y="266" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="26" y="282" width="84" height="20" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="68" y="296" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Fare 表</text>
<rect x="26" y="304" width="84" height="20" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="68" y="318" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Ride 表</text>
<rect x="222" y="8" width="100" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="272" y="22.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">司机客户端</text>
<text x="272" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Driver Client</text>
<rect x="222" y="164" width="100" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="272" y="180.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">位置服务</text>
<text x="272" y="195.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Location</text>
<path d="M222,248 a50,6 0 0 1 100,0 v74 a50,6 0 0 1 -100,0 z" stroke-width="1.2" fill="none" stroke="currentColor"/>
<path d="M222,248 a50,6 0 0 0 100,0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<text x="272" y="266" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="230" y="282" width="84" height="22" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="272" y="297" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Location 表</text>
<rect x="222" y="368" width="100" height="60" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="272" y="394.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">匹配服务</text>
<text x="272" y="409.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Matching</text>
<polyline points="272,44 272,72" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="272,72 268.8,65.0 275.2,65.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="272,100 272,164" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="272,164 268.8,157.0 275.2,157.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="266" y="148" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor">POST /drivers/location</text>
<polyline points="272,204 272,242" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="272,242 268.8,235.0 275.2,235.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="278" y="228" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">写位置</text>
<polyline points="250,368 250,328" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="250,328 253.2,335.0 246.8,335.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="256" y="352" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">查近邻</text>
<polyline points="112,204 112,222 170,222 170,378 222,378" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="222,378 215.0,381.2 215.0,374.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="164" y="352" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor">触发匹配</text>
<text x="74" y="133" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">PATCH /rides/:id</text>
<rect x="222" y="490" width="100" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="272" y="508.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">通知服务</text>
<text x="272" y="523.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">APNs · FCM</text>
<polyline points="322,512 332,512 332,26 322,26" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="322,26 329.0,22.8 329.0,29.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polyline points="272,428 272,490" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="272,490 268.8,483.0 275.2,483.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="278" y="480" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">推送</text>
<text x="8" y="556" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">匹配服务排好候选名单，</text>
<text x="8" y="572" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">通知服务推给第 1 位；司机 PATCH 接单，</text>
<text x="8" y="588" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">叫车服务把状态改为 accepted；</text>
<text x="8" y="604" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">拒绝或没响应就推给下一位</text>
</svg>
白板上新增：通知服务、推送路径（右侧折线回到司机端）、司机的 `PATCH` 调用。
**为什么这样说。** （约 9 分钟，累计第 25 分钟。）面试官看你能不能快速完成这一步：高级候选人要在这里加快速度，把时间留给深入问题。最后一句主动留白很重要，它告诉面试官你已经看出设计的弱点，下一步由你带，而不是等他来找问题。弱的回答是画完就停，等面试官提问。
**面试官可能接着问。**
- 匹配为什么单独成服务？ → 它的负载特点和叫车服务不同：叫车是普通增删改查，匹配要读大量位置、做排序，吃 CPU，要单独扩缩容。
- 怎么实时通知司机？ → 用推送（APNs、FCM），应用在后台也能到达。若面试官想要在线实时通道，可以用长轮询、SSE 或 WebSocket，取舍是连接管理的成本。
- 候选名单怎么排？ → 先按距离，再看是否空闲、评分。具体算法我抽象掉，需要的话可以按接驾预计时间排序。
**常见失分。**
- **画完就停：** 不指出自己设计的缺口，面试官会替你指出来，感觉就差很多。
- **把推送画成接口：** 通知是服务向司机主动推送，不是司机反复轮询。
- **时间花太长：** 高层设计超过 15 分钟，深入问题就讲不完。高级候选人要在这里提速。
