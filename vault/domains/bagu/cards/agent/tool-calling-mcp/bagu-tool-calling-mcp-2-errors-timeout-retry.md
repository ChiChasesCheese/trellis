---
id: bagu-tool-calling-mcp-2-errors-timeout-retry
node: a.agent.tool-calling-mcp
type: qa
step: 2
---
## Q
**工具失败 · 参数错误、超时、重试怎么设计**｜必会

面试官：「模型传错了参数，或者工具调用超时，你怎么处理？能直接重试吗？」

## A
**基本回答。** 按错误类型分别处理。参数错误：服务端校验后把具体错误（字段和原因）回给模型，只让它修正这一部分，最多重试 1 到 2 次，仍失败就降级（追问用户或转人工）。超时：只读工具设较短超时并有限重试；写操作超时是「结果未知」，先按幂等键查状态，不盲目重试。参数错、没权限这类确定性错误立即失败，限流和瞬时网络错误才在预算内退避重试。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 238">
<text x="72" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">错误类型</text>
<text x="256" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">怎么处理</text>
<rect x="4" y="24" width="136" height="42" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="72.0" y="49.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">参数错误</text>
<rect x="176" y="24" width="160" height="42" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256.0" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回给模型：字段 + 原因</text>
<text x="256.0" y="56.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只修这一处，最多 1~2 次</text>
<line x1="140" y1="45" x2="170.0" y2="45.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="176.0,45.0 170.0,48.0 170.0,42.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="4" y="74" width="136" height="42" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="72.0" y="91.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">没权限等</text>
<text x="72.0" y="106.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">确定性错误</text>
<rect x="176" y="74" width="160" height="42" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256.0" y="91.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">立即失败</text>
<text x="256.0" y="106.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">重试结果不会变</text>
<line x1="140" y1="95" x2="170.0" y2="95.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="176.0,95.0 170.0,98.0 170.0,92.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="4" y="124" width="136" height="42" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="72.0" y="149.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">限流、瞬时网络错</text>
<rect x="176" y="124" width="160" height="42" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256.0" y="141.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">预算内退避重试</text>
<text x="256.0" y="156.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">各层共享总截止时间</text>
<line x1="140" y1="145" x2="170.0" y2="145.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="176.0,145.0 170.0,148.0 170.0,142.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="4" y="174" width="136" height="42" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="72.0" y="199.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写操作超时</text>
<rect x="176" y="174" width="160" height="42" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="256.0" y="191.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">结果未知：先查状态</text>
<text x="256.0" y="206.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">按幂等键，不盲目重试</text>
<line x1="140" y1="195" x2="170.0" y2="195.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="176.0,195.0 170.0,198.0 170.0,192.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="232" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">仍失败 → 降级：追问用户或转人工</text>
</svg>
左边是错误的种类，右边是对应的处理；只有最后一行是写操作超时，不能盲目重试。
**容易错。**
- **所有失败都重试：**确定性错误重试一万次结果也一样。
- **写操作超时直接重发：**可能已经执行，重发就是重复退款或重复下单。
- **失败时让模型自由发挥：**不明确告诉模型「当前无法完成」，它会编造业务事实；也不要静默补默认值。
- **各层重试各算各的：**SDK、网关、工具层层重试，次数相乘，要共享总截止时间。
**业务场景。** 直播间下单后用户问「货到哪了」，物流查询工具超时：Agent 如实回复「物流系统繁忙」，不让模型根据订单号猜一个到达时间。
