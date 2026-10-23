---
id: hl-sd03-fu-kill-switch-design
node: system-design.sd03-low-latency-trading
type: qa
step: 42
---
## Q
追问：熔断（kill switch）怎么设计？延迟多大？

## A
三层（进程内 `volatile` 标志 / 独立进程或设备 / 交易所 cancel-on-disconnect 与整体撤单）；自动触发条件：仓位 / 亏损超限、拒单率、下单速率异常、行情陈旧、日志落后、对账差异；每单检查一次标志（约 ns，单写者控制面写、热线程读）；触发后撤销全部未完成订单、禁新单、保持行情接收；恢复需要确认；定期演练。

可以说：「熔断的第一原则是它不能依赖被熔断的东西。」
