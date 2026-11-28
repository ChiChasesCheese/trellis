---
id: hi-c-sd-temporal-x06-bottleneck
node: sd.deep-dives.temporal.exam
type: qa
step: 6
---
## Q
**Temporal · 服务变慢，该加什么**｜考点 · 必会

大促期间 Workflow 的推进延迟升高。监控显示：worker 实例 CPU 只有 20%，Task Queue 里等待的任务很少，History 服务实例和它的数据库写入延迟很高。应该加什么？不该加什么？

## A
- **诊断：** worker 空闲、队列不积压，说明没有"待执行的工作等 worker"；延迟来自 History 服务和持久化层——每次状态变化（Activity 完成、Signal、计时器）都要写事件历史、可变状态和任务。
- **该加：** 增加 History 实例以分担 History 分片；扩大持久化数据库的写容量（更强的实例、更好的磁盘、或更多数据库节点）。History 分片数是创建集群时固定的，要在设计时预留足够分片。
- **不该加：** 增加应用 worker——没有积压的任务，加了没用，甚至可能因为更多轮询增加负载。
- **进一步：** 看能否减少事件数量：合并相邻的小 Activity、减少不必要的 Signal、对长流程用 continue-as-new 缩短历史。
- **原则：** 按瓶颈所在扩容，而不是随便加机器。
