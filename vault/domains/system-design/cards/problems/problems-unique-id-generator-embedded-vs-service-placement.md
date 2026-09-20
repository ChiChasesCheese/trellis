---
id: problems-unique-id-generator-embedded-vs-service-placement
node: problems.foundations.unique-id-generator
type: qa
step: 3
tags: [grown]
---
## Q
In a unique ID generator design with a sub-1ms P99 latency requirement, why does running ID generation as a separate network service (called via RPC on every write) undermine the design's own goal, and what placement does the design use instead?

## A
A separate ID-generation service means every business write now makes an extra network round trip whose latency and availability get added directly onto the write's critical path — this reintroduces exactly the kind of synchronous cross-node dependency the design was built to avoid in the first place. Instead, the design embeds the generation logic as a library inside each deployment unit's own process (or pushes it further down, e.g. as a database function colocated with the write, as Instagram does), so id generation is a pure in-process call with zero network I/O; the only coordination point is a one-time worker-id lease acquired at startup and renewed in the background, never on the generation path itself.

## Q zh
在一个 P99 延迟要求低于 1ms 的唯一 ID 生成器设计中，为什么把 ID 生成做成一个独立的网络服务（每次写入都发一次 RPC 调用）会违背设计本身的目标？这个设计用了什么样的放置方式来代替？

## A zh
独立的 ID 生成服务意味着每一次业务写入都要多一次网络往返，这一跳的延迟和可用性会直接叠加进写入的关键路径——这恰恰重新引入了这个设计最初就要避免的那种同步跨节点依赖。这个设计改为把生成逻辑作为一个库嵌入到每个部署单元自己的进程里（或者进一步下推，例如像 Instagram 那样做成和写入同处一地的数据库函数），让 ID 生成成为一次纯进程内调用、零网络 I/O；唯一的协调点是启动时申请一次的 worker id 租约，之后在后台续约，从不出现在生成路径本身上。
