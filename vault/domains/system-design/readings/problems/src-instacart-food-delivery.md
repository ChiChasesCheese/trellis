---
nodes: [problems.geo.food-delivery]
url: https://tech.instacart.com/instacarts-item-availability-architecture-solving-for-scale-and-consistency-f5661acb20a6
---
# Instacart's Item Availability Architecture: Solving for Scale and Consistency

值得读：Instacart 官方工程博客，描述了他们如何用周期性全量同步（periodic full sync）
加按需懒刷新（on-demand lazy refresh）、辅以针对性的分数调整，维护跨多个客户端界面的
商品可用性一致性，而不是对每次展示都做强一致查询。本题解在「容量估算」和「深入探讨」
第 1 节用它印证"展示层可用性数据走缓存、容忍陈旧，只在真正扣减库存那一步做强一致"这个
决策——它是比 DoorDash/Uber Eats 更贴近 Gopuff 场景（平台自持库存）的一手参照。
