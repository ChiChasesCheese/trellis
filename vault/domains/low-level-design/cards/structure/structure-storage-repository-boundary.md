---
id: structure-storage-repository-boundary
node: structure.storage
type: qa
---
## Q
在 90 分钟的轮次中只有纯内存数据，为什么在 `HashMap` 周围包装一个存储库接口（`save`、`findById`、`findByX`）而不是让服务接触地图?

## A
- **经典的后续是"现在持久化它"** — 用 `interface OrderRepository`，那是一个新实现；不用，每个服务改变。
- **测试**得到一个明显的接缝: 注入一个内存假的，没有模拟框架。
- **存储关注的一个地方**: 锁定、索引维护和防御副本生活在接口后面而不是泄漏到商业逻辑。

便宜去做: 地图支持的实现是 ~10 行。面试官评分可扩展性，这是最高价值接缝每分钟花费。
