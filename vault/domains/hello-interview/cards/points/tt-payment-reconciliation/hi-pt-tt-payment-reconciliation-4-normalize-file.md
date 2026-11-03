---
id: hi-pt-tt-payment-reconciliation-4-normalize-file
node: tt.sd.tt-payment-reconciliation.points
type: qa
step: 7
---
## Q
**支付对账系统 · 规范化与文件幂等**｜必会 · 出自：支付对账系统 › 深入 3

对账系统导入 PSP 文件，怎么保证口径统一、文件幂等，以及截断或更正文件不出事？

## A
**规范化。** 金额用精确解析的整数最小单位，不用浮点；退款、拒付、手续费符号统一成对我们现金的影响；业务日以 PSP 处理时间为准。
**文件。** 按文件哈希去重，核对行数和控制总额，不符不进匹配，防止截断造成大批假的账本有 PSP 没有；更正文件用 supersedes_id 取代旧文件，旧匹配作废重算。
**预期到达日历。** 到点没来就告警。
