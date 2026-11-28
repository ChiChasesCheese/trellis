---
id: hi-c-sd-long-running-tasks-x04-heartbeat-interval
node: sd.patterns.long-running-tasks.exam
type: qa
step: 4
---
## Q
**长任务 · 心跳间隔设多长**｜考点 · 必会

心跳 3 秒与 5 分钟各有什么问题？你怎么选？

## A
- **太短（3 秒）：** 大量无谓消息；垃圾回收暂停等短暂停顿就把仍在运行的任务误判为失败，造成重复执行。
- **太长（5 分钟）：** 工作者崩溃后任务要等很久才被重新分发。
- **选择：** 在用户能容忍的额外延迟内取尽量长的间隔，一般 10 到 30 秒起步。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 116">
<g stroke="currentColor" stroke-width="1.2" fill="none">
<line x1="20" y1="60" x2="320" y2="60"/>
<line x1="40" y1="52" x2="40" y2="68"/>
<line x1="300" y1="52" x2="300" y2="68"/>
</g>
<g stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="120" y="52" width="80" height="16"/>
</g>
<g font-size="12" font-family="sans-serif" fill="currentColor">
<g text-anchor="middle">
<text x="40" y="40">3 秒</text><text x="160" y="40">10 到 30 秒</text><text x="300" y="40">5 分钟</text>
<text x="160" y="106">可容忍延迟内尽量长</text>
</g>
<text x="10" y="86">消息多，GC 停顿被误判</text>
<text x="330" y="86" text-anchor="end">崩溃后久等</text>
</g>
</svg>

- **相关配置：** SQS 的可见性超时、RabbitMQ 的心跳间隔、Kafka 的会话超时。
- **注意：** 因为可能误判，任务必须幂等。
