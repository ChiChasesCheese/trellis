---
id: hl-sd03-fu-exec-report-oms
node: system-design.sd03-low-latency-trading
type: qa
step: 48
---
## Q
追问：订单回报乱序、缺失、重复，OMS 怎么保持正确？

## A
`execId` 去重（重复）；会话序号检测缺失，请求补发；终态订单收到旧回报视为重复；非法转移（超量成交、成交价越限价、终态后再 Fill）不改状态并报警；PENDING 超时主动查询；仓位始终是成交事件的纯函数，所以修复 = 追加一条「对账修复」事件，而不是直接改数字。

可以说：「状态是事件的函数，修复也是事件。」
