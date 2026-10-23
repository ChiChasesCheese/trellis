---
id: hl-sd03-fu-failover-no-dup
node: system-design.sd03-low-latency-trading
type: qa
step: 43
---
## Q
追问：主备怎么切换才不会双发？

## A
备机热备（收行情，经复制日志 / drop copy 得到回报，不发单）；发单权令牌带 epoch；切换：确认主机真停（STONITH）→ 交易所 cancel-on-disconnect 已撤单 → 备机获发单权 → 新会话登录 → mass cancel → 对账 → 恢复；不做 active-active 发单（除非按品种严格分区）；RTO 秒级，期间不报价是代价。

可以说：「宁可停几秒，也不让两个实例同时拥有同一个账户的发单权。」
