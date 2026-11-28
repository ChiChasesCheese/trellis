---
id: bagu-project-deepdive-3-stability
node: a.agent.project-deepdive
type: qa
step: 3
---
## Q
**稳定性 · 工具失败、超时、模型不可用**｜必会

面试官：「Agent 调用的工具超时了，或者模型服务挂了，你怎么保证系统稳定？」

## A
**基本回答。** 按故障对象分别设计：
- 工具超时：写操作视为结果未知，复用同一个 `actionId` 作幂等键，先查状态再决定重试，仍不明确就对账或转人工。
- 重试：指数退避加抖动，各层共享总截止时间和重试预算，避免次数相乘。
- 持续不可用：熔断，停止发请求，按风险降级——备用模型（先用同一套评测验证）、缓存、部分结果、转人工。
- 写操作遇到模型不可用，暂停，不降级执行（模型变弱会同时影响工具选择和参数）。
- 慢工具用独立并发舱壁（bulkhead，每类工具各自的并发额度）隔离；Trace 区分 `FAILED`、`TIMED_OUT_UNKNOWN`、`SUCCEEDED`，也区分降级完成和正常完成。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 314">
<rect x="40" y="8" width="260" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="27.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写操作超时：结果未知</text>
<line x1="170" y1="38" x2="170.0" y2="47.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="170,54 166.8,47.0 173.2,47.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="40" y="54" width="260" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="73.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">拿同一个 actionId 查状态</text>
<line x1="100" y1="84" x2="63.8" y2="108.1" stroke="currentColor" stroke-width="1.2"/>
<polygon points="58,112 62.0,105.5 65.6,110.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="84" x2="170.0" y2="105.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="170,112 166.8,105.0 173.2,105.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="240" y1="84" x2="276.2" y2="108.1" stroke="currentColor" stroke-width="1.2"/>
<polygon points="282,112 274.4,110.8 278.0,105.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="112" width="96" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56.0" y="130.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">已成功</text>
<text x="56.0" y="145.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回填单号</text>
<rect x="112" y="112" width="116" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="130.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">没成功</text>
<text x="170.0" y="145.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">同幂等键重发</text>
<rect x="236" y="112" width="96" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="284.0" y="130.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不明确</text>
<text x="284.0" y="145.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">对账或转人工</text>
<text x="8" y="184" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">模型服务持续不可用</text>
<rect x="40" y="194" width="260" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="213.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">熔断：停止发请求</text>
<line x1="100" y1="224" x2="87.3" y2="240.5" stroke="currentColor" stroke-width="1.2"/>
<polygon points="83,246 84.7,238.5 89.8,242.4" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="240" y1="224" x2="252.7" y2="240.5" stroke="currentColor" stroke-width="1.2"/>
<polygon points="257,246 250.2,242.4 255.3,238.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="246" width="150" height="52" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83.0" y="268.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读类、低风险</text>
<text x="83.0" y="283.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">备用模型、缓存、人工</text>
<rect x="182" y="246" width="150" height="52" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="257.0" y="268.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写操作</text>
<text x="257.0" y="283.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">暂停，不降级执行</text>
</svg>
上半是写操作超时后的三条出路，核心是先拿同一个 actionId 查状态；下半是模型持续不可用时，读类可以降级，写操作必须暂停。
**容易错。**
- **超时就重发：** 第一次可能已经成功，重发会重复退款。
- **各层各自重试：** 三层各重试 3 次最坏是 27 次，要共享总截止时间和预算。
- **持续故障还在重试：** 只会拉长响应、耗尽预算，要熔断。
- **模型挂了就换个模型继续写：** 换的模型没验证过，工具选择和参数可能出错；写操作要暂停。
**业务场景。** 打赏退款生成 `actionId=A17`，调渠道退款接口等 8 秒无响应，Trace 记 `TIMED_OUT_UNKNOWN`；Agent 不重发，按 A17 查，渠道返回已退款成功、单号 RF-9，回填工单，用户只退一次；若查到没成功，才用同一个 A17 重发。
