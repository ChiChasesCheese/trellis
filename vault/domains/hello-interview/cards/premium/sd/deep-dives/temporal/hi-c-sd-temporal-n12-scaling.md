---
id: hi-c-sd-temporal-n12-scaling
node: sd.deep-dives.temporal.notes
type: qa
step: 8
---
## Q
**Temporal · 集群怎么扩展，瓶颈在哪里**｜摘要 · 必会

数百万个订单在等收货，需要数百万个 worker 吗？负载上升时应该加什么？

## A
- **不需要：** 在途进程数可以增长而不要求每个流程一个 worker。等待中的订单只占数据库空间，不占 worker。worker 算力取决于"此刻有多少工作可以做"，而不是还有多少订单没结束。突发的送达通知涌入，就加 worker 去处理评价邮件。
- **服务端单独扩展：** 更多 Frontend 实例处理 API 流量，更多 History 实例分担 History 分片，更多 Matching 实例处理 Task Queue 分区。
- **按瓶颈扩容：** 邮件积压 → 加邮件 worker；Workflow 状态更新速率上升 → 要扩大 Temporal 服务和持久化层。如果瓶颈是 Workflow 状态更新，增加应用 worker 没用，要加 History 或其数据库的容量。
