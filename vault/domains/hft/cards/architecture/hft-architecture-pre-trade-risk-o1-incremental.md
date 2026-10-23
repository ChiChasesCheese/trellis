---
id: hft-architecture-pre-trade-risk-o1-incremental
node: architecture.pre-trade-risk
type: qa
step: 3
---
## Q
下单前风控必须在几十纳秒内完成。它是怎么做到这么快的？为什么不能每次下单都遍历所有未完成订单来算总量？

## A
关键是 **O(1)**：检查要用到的汇总量，都在订单状态**每次变化时增量维护**。例如某品种的未完成买单总量 `openBuyQty[instrument]`：下单时加 qty，成交或撤单时减 qty。

检查时只是几次数组读取（品种用稠密的 int 编号当下标）和比较，数据全在 L1/L2 缓存里，约几十纳秒。风控状态本身很小：5000 个品种 × 20 个策略 × 64 字节 ≈ 6.4 MB，放得进 L2/L3 缓存。

如果每次检查都遍历 1 万张未完成订单，按每张几纳秒算就是几十微秒，已经超过整个 tick-to-trade 预算。
