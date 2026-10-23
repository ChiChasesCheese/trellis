---
id: hl-sd03-problem
node: system-design.sd03-low-latency-trading
type: qa
step: 1
---
## Q
设计题：低延迟电子交易系统（Ingest market data, validate strategy order intents, route orders to exchanges, and reconcile executions）。四个动词各对应哪个子系统？Java 岗面试里它更可能被问成什么？

## A
题面：从一个或多个交易所接收实时行情；若干策略读取行情产生「订单意图」；系统对每个意图做风控校验，通过的订单路由到相应交易所；交易所的成交 / 拒绝 / 撤单回报要被处理，并与独立数据源对账。需说明延迟预算、线程与数据流模型、状态存放与崩溃恢复、故障与安全机制（熔断）、怎么测试与度量。可假设托管在交易所机房（co-location）。

四个动词 = 四个子系统：**ingest**（行情摄取）→ **validate**（订单意图校验，即交易前风控）→ **route**（路由到交易所）→ **reconcile**（对账成交）。

与岗位的关系：Java 岗偏研究平台 / 存储 / 计算集群 / 监控，毫秒以下热路径通常是 C++ 岗。所以更可能被问成「你理解整条链路，并能设计其中 Java 能做好的部分」（编排、风控监控、对账、研究回放）。**两头都要准备**：能讲热路径原理，也能说清 Java 适合放在哪。
