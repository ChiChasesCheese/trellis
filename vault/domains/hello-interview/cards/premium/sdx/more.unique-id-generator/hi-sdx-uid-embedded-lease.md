---
id: hi-sdx-uid-embedded-lease
node: more.unique-id-generator
type: qa
step: 2
---
## Q
**发号嵌进进程，协调服务只在启动时用**｜补充 · 发号器（Unique ID Generator） · 必会

面试官：「写入延迟要求 P99 低于 1 ms。发号做成独立服务，每次写入先 RPC 取号，行不行？如果发号逻辑嵌进业务进程，机器号怎么分配，分配用的协调服务整个挂了会怎样？」

## A
**结论。** 独立服务不行。把发号做成库嵌进每个部署单元，生成 ID 是纯内存调用；协调服务只在启动时租一个机器号、后台续租，不在发号路径上。

**要点。**
- **独立服务的代价：** 每次写多一次网络往返，它的延迟和可用性直接叠加在写路径上，正是要避免的同步跨节点依赖。
- **嵌入式：** 发号逻辑做成进程内的库，或做成数据库里的函数，与写入放在一起（Instagram 的做法是发号写成各逻辑分片里的数据库函数）。
- **租约：** 启动时向协调服务（ZooKeeper、etcd 或数据库一行）租一个机器号，后台定期续租。
- **协调服务整个宕机：** 已运行的节点完全不受影响，因为发号从不访问它；受影响的只有新实例起不来。
- **续租持续失败：** 一旦超过租约到期时间，节点必须自己停止发号，因为机器号可能已被回收并分给别的实例，继续发就会产生重复 ID。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 206">
<rect x="10" y="24" width="214" height="110" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="42" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">业务进程</text>
<rect x="22" y="52" width="86" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="65.0" y="74.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写入逻辑</text>
<rect x="122" y="52" width="90" height="36" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="167.0" y="74.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发号库</text>
<polyline points="108,70 122,70" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="122.0,70.0 115.0,66.8 115.0,73.2" style="fill:var(--accent,#3b6fd4)"/>
<text x="22" y="112" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">纯内存调用，P99 远低于 1 ms</text>
<rect x="244" y="52" width="86" height="36" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="287.0" y="74.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">协调服务</text>
<polyline points="212,70 244,70" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="244.0,70.0 237.0,66.8 237.0,73.2" style="fill:var(--accent,#3b6fd4)"/>
<text x="287" y="106" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">启动租号</text>
<text x="287" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">后台续租</text>
<text x="10" y="160" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">协调服务宕机：已运行的节点照常发号</text>
<text x="10" y="178" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">续租失败且超过租约到期：节点自己停发</text>
<text x="10" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">（机器号可能已转给别的实例）</text>
</svg>

**面试里这样说。** 「发号我嵌进每个进程，生成 ID 是纯内存操作。机器号启动时从协调服务租一个、后台续租，协调服务挂了已运行节点不受影响；但续租失败超过租约期，节点要主动停发，避免机器号被重新分配后出现重复。」

**易错。**
- **在每次发号时访问协调服务：** 把它变成写路径上的单点。
- **租约过期后继续发号：** 两个实例用同一个机器号，ID 会重复。
