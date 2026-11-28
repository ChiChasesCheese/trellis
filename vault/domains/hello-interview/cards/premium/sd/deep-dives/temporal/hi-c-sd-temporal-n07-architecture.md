---
id: hi-c-sd-temporal-n07-architecture
node: sd.deep-dives.temporal.notes
type: qa
step: 12
---
## Q
**Temporal · 服务端有哪四个角色**｜摘要 · 追问

Temporal 集群由哪几个部分组成？各自负责什么？Workflow 代码跑在哪里？

## A
- **Frontend Service：** 无状态的入口，客户端和 worker 连它，它把请求路由到内部相应服务。
- **History Service：** 持有 Workflow Execution 的持久状态，处理 Activity 完成、Signal、计时器、Workflow 代码做出的决定。
- **Matching Service：** 管理连接 Temporal 与 worker 的 Task Queue。
- **Worker：** 你的应用进程，Workflow 和 Activity 代码在这里执行，不在 Temporal 服务内部。worker 向 Temporal 拉取工作、执行代码、把结果送回。
- **各自独立扩展：** Frontend、History、Matching、Worker 是各自的实例群；History 拥有分片，Matching 管理 Task Queue 的分区。
- **面试提示：** 面试里几乎不需要知道 Temporal 的内部实现，有兴趣再深入。
