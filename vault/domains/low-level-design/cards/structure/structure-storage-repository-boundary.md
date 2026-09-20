---
id: structure-storage-repository-boundary
node: structure.storage
type: qa
step: 1
---
## Q
90 分钟的机考轮次里数据只存在内存 `dict` 中，为什么还要在 `dict` 外面包一层仓储（repository）接口（`save`、`find_by_id`、`find_by_x`），而不是让业务代码直接操作字典？

## A
三个理由：**经典的后续需求是"现在把它持久化"**——有 `class OrderRepository(Protocol)`，换成数据库实现是新写一个类；没有，业务代码里每处直接操作字典的地方都要改。

**测试**因此得到一个明显的接缝（seam）——注入一个内存实现的假仓储，不需要 mock 框架。

**存储相关的关注点集中在一处**——加锁、维护二级索引、防止返回内部可变引用，这些都待在仓储实现里，不泄漏进业务逻辑。

做起来很便宜：一个基于 `dict` 的实现大概十来行代码，而面试官恰恰是按"可扩展性"打分——这是每分钟投入回报最高的一个接缝。
