---
id: hl-java-role-offline
node: company.java-role
type: qa
step: 3
---
## Q
交易系统里"离线"那一半包含哪些工作？它和实盘链路的特点有什么不同？

## A
离线部分**不要求极快，但数据极大**：
- 参数优化；
- production reconciliation（对账：实盘与模拟是否一致）；
- backtesting simulator（回测）；
- 画图。

其中 tick 数据"可达每天数百 GB"。

对比：实盘链路追求每一步微秒级；离线追求的是**吞吐和规模**——读海量数据、跑海量作业。Java 岗的研究平台、分布式存储、计算集群都服务于这一半。
