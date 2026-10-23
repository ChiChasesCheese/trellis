---
id: hl-sd03-ha-failover
node: system-design.sd03-low-latency-trading
type: qa
step: 26
---
## Q
交易系统的主备高可用怎么做到「不双发」（I4）？切换流程是什么，为什么不做 active-active 发单？

## A
**active/passive 热备**：备机同样接收组播行情，并通过**复制的日志流**（或 drop copy）得到回报与命令，状态近乎实时一致，**但不向交易所发单**。

**谁有权发单**：用一个明确的「发单权」令牌（由外部协调服务 / 人 / 硬件开关授予，带 epoch fencing token）。持有者才能把意图交给网关；备机的网关线程没有会话 / 被禁止发送。

切换流程（秒级）：主机故障 → 交易所 cancel-on-disconnect 撤其订单 →（确认主机确实停止：断电 / 强制下线，**STONITH**）→ 备机获得发单权 → 备机登录新会话 → 发整体撤单（mass cancel）→ 与交易所对账仓位 → 行情已对齐 → 恢复。

不做 active-active 发单：两个实例对同一账户发单会重复下单 / 自成交，除非严格按品种分区且互不重叠。恢复期间不报价在 SLO 内（RTO 秒级），这是为 I3 / I4 付出的代价。
