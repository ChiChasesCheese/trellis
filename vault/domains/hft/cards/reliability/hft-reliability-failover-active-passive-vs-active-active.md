---
id: hft-reliability-failover-active-passive-vs-active-active
node: reliability.failover
type: qa
step: 4
---
## Q
为什么交易系统一般用 active/passive 主备，而不用两台都发单的 active-active？恢复时间为什么不追求毫秒级？

## A
两台实例对同一账户同时发单，会重复下单或自成交，持仓也对不上，所以通常是 active/passive：只有一台有发单权。只有严格按品种分区、互不重叠时，才可能做 active-active。

恢复时间为什么是秒级：切换要包含这些步骤——检测故障（心跳超时一般设为几百毫秒到数秒，设得太短会误判）、确认旧主机已停止、备机登录新会话、对账持仓、行情对齐。每一步都是为了不双发、不带错误持仓交易。

取舍：停摆几秒的代价（错过几秒行情、少量报价缺失）远小于重复下单或带错持仓交易。优先级是错单 ≫ 丢行情 ≫ 延迟变差 ≫ 停摆。
