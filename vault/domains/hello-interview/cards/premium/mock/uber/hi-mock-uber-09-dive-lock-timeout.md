---
id: hi-mock-uber-09-dive-lock-timeout
node: sd.problem-breakdowns.uber.mock
type: qa
step: 9
---
## Q
**网约车 · 第 9 步 · 深入二：一个司机一次一单，不响应就换人**｜模拟面试

面试官：「匹配服务有很多个实例。两个订单同时看中同一个司机会怎样？另外，如果司机收到请求后一直不响应呢？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **规则：** 一个订单一次只问一位司机，一个司机一次只收一个订单，司机有 10 秒决定；和订票时座位在结账期间被临时占住是同类问题。
- **方案一，应用层锁加自己计时（否）：** 多个实例没有协调可能同时锁同一司机；加锁的实例崩溃锁没人释放；实例越多越糟。
- **方案二，数据库状态（可行但不选）：** 司机状态 available / outstanding_request / accepted 切换，事务保证只有一个实例改成功；但 10 秒超时靠服务内存计时器，重启即丢、状态永远改不回；加定时扫描能补，但有额外复杂度和释放延迟。
- **方案三，Redis 分布式锁（选）：** 键 `driver:{id}`，值写订单号，`SET NX EX 10`：抢到才发请求，10 秒后自己过期；接受就改库并删锁，超时不用管。锁只活 10 秒，Redis 故障恢复快（Sentinel 切换），最坏几秒内同一司机被问两次。
- **锁不是最后防线：** 带过期的锁只保证大多数时候互斥；司机第 10.5 秒才点接受，锁可能已被下一单拿走。所以接单时 `UPDATE rides SET driver_id=?, status='accepted' WHERE id=? AND status='requested'`，影响 0 行就告诉司机这单已失效；锁值带订单号，只认当前订单的锁，客户端倒计时设得比 TTL 略短。
- **但锁不会换人：** TTL 只放锁，不去问下一位；「等 10 秒、没响应换人」另要机制。
- **方案四，延迟队列：** 发请求时投一条 10 秒后可见的消息，到期检查订单是否未分配、转下一位；难点是司机恰好在到期前接受时，迟到消息不能误改派，取消和竞态要自己处理。
- **方案五，持久化执行（选）：** 整个匹配建成一个 Temporal 工作流：发给第 1 位、设 10 秒超时；接受就结束，拒绝或超时转下一位；名单用完或满 60 秒报失败。状态持久，服务崩溃后从断点继续；代价是多一套系统，但丢单直接损失收入。工作流代码必须确定（崩溃后另一进程从头重放，已有历史的步骤取历史结果），时间、随机数、网络请求要放进 activity。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 620">
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
<rect x="222" y="8" width="100" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="272" y="22.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">司机客户端</text>
<text x="272" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Driver Client</text>
<rect x="222" y="164" width="100" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="272" y="180.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">位置服务</text>
<text x="272" y="195.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Location</text>
<path d="M18,248 a50,6 0 0 1 100,0 v74 a50,6 0 0 1 -100,0 z" stroke-width="1.2" fill="none" stroke="currentColor"/>
<path d="M18,248 a50,6 0 0 0 100,0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<text x="68" y="266" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="26" y="282" width="84" height="20" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="68" y="296" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Fare 表</text>
<rect x="26" y="304" width="84" height="20" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="68" y="318" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Ride 表</text>
<path d="M222,248 a50,6 0 0 1 100,0 v74 a50,6 0 0 1 -100,0 z" stroke-width="1.2" fill="none" stroke="currentColor"/>
<path d="M222,248 a50,6 0 0 0 100,0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<text x="272" y="266" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis</text>
<rect x="230" y="282" width="84" height="20" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="272" y="296" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">drivers:geo</text>
<rect x="230" y="304" width="84" height="20" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="272" y="318" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">drivers:ts</text>
<rect x="222" y="368" width="100" height="96" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="272" y="383" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">匹配服务</text>
<rect x="230" y="414" width="84" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="272" y="432.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Temporal</text>
<text x="272" y="447.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">工作流</text>
<polyline points="68,44 68,72" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="68,72 64.8,65.0 71.2,65.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="272,44 272,72" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="272,72 268.8,65.0 275.2,65.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="68,100 68,164" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="68,164 64.8,157.0 71.2,157.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="272,100 272,164" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="272,164 268.8,157.0 275.2,157.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="266" y="148" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor">POST /drivers/location</text>
<text x="74" y="118" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">POST /fare, /rides</text>
<text x="74" y="133" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">PATCH /rides/:id</text>
<polyline points="114,184 132,184" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="132,184 125.0,187.2 125.0,180.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="34,204 34,242" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="34,242 30.8,235.0 37.2,235.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="40" y="228" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">写库</text>
<polyline points="18,184 10,184 10,26 18,26" fill="none" stroke-width="1.3" stroke-dasharray="4 3" stroke="currentColor"/>
<polygon points="18,26 11.0,29.2 11.0,22.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="272,204 272,242" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="272,242 268.8,235.0 275.2,235.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="278" y="228" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">GEOADD</text>
<polyline points="250,368 250,328" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="250,328 253.2,335.0 246.8,335.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="256" y="352" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">GEOSEARCH</text>
<polyline points="112,204 112,222 170,222 170,378 222,378" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="222,378 215.0,381.2 215.0,374.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="164" y="352" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor">启动工作流 / 接单信号</text>
<rect x="222" y="490" width="100" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="272" y="508.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">通知服务</text>
<text x="272" y="523.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">APNs · FCM</text>
<polyline points="322,512 332,512 332,26 322,26" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="322,26 329.0,22.8 329.0,29.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="272,464 272,490" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="272,490 268.8,483.0 275.2,483.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="278" y="480" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">推送</text>
<path d="M18,374 a50,6 0 0 1 100,0 v64 a50,6 0 0 1 -100,0 z" stroke-width="1.2" fill="none" stroke="currentColor"/>
<path d="M18,374 a50,6 0 0 0 100,0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<text x="68" y="398" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis 司机锁</text>
<text x="68" y="413" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">driver:{id}</text>
<text x="68" y="428" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">TTL 10 秒</text>
<polyline points="222,412 118,412" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="118,412 125.0,408.8 125.0,415.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="405" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SET NX EX 10</text>
<text x="8" y="556" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">以 rideId 为工作流 ID，一单只有一个工作流：</text>
<text x="8" y="572" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">发给第 1 位 → 等 10 秒 → 接受则结束，</text>
<text x="8" y="588" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">拒绝或超时就下一位；名单用完或满 60 秒报失败</text>
</svg>
白板上新增：匹配服务框里的 Temporal 工作流；启动和接单信号走原来那条路径。

**常见失分。**
- **只说加分布式锁：** 没说 TTL、崩溃释放、迟到的接单。
- **把 TTL 当换人机制：** TTL 只放锁，换人靠计时器或工作流。
- **依赖内存计时器：** 服务一重启就丢，最常见的坑。
- **忽略条件更新：** 锁过期与迟到点击的竞态只能靠写入时的条件检查兜底。
