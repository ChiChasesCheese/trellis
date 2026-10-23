---
id: hl-bs-r1-pit-purged
node: behavioral.stories
type: qa
step: 4
---
## Q
回测里的点时数据（point-in-time）和 purged 交叉验证（purged CV）各防什么问题？2 分钟版还加了什么？

## A
- **点时数据**：用了后来修订的数据或未来数据，会让结果**虚高**；点时平面保证回测**不使用当时还不知道的数据**。
- **Purged CV**：标签跨越一段时间，训练 / 测试边界附近的样本会**共享信息**；purging 把重叠的样本去掉。

2 分钟版在 60 秒版上加：**paper trading 闭环**——Alpaca / CCXT 路由、**下单前风控检查（pre-trade risk checks）**、一份 5 因子风险报告。
