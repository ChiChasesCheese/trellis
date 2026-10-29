---
id: uth-os-net-load-balancing-3-p2c
node: os-net.load-balancing
type: qa
step: 3
---
## Q
**随机挑两个，选闲的那个**｜Envoy · least request

有 1000 台后端时，“选当前请求数最少的”要扫 O(n)，有没有又便宜又接近的办法？

## A
**结构。** P2C（power of two choices）：随机挑 2 台，选活跃请求少的那台。Envoy 的 least request 在各主机权重相同时就是它，挑选个数默认 2，复杂度 O(1)。

**细节。**

- 文档引用 Mitzenmacher 等人的结论：几乎和 O(n) 的全扫一样好
- 全扫的毛病是羊群效应（herding）：所有负载均衡器同时涌向那台“最闲”的机器
- 权重不等时改用加权轮询，权重按 `weight / (active_requests + 1)^bias` 动态计算

**为什么。** 多看一个随机样本，就能避开最忙的机器，又不必掌握全局状态。

**对应 LeetCode：** LC 528 按权重随机选择 · LC 380 O(1) 时间插入、删除和获取随机元素
