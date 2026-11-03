---
id: hi-pt-payment-batch-processing-7-batch-scale
node: qb.sd.payment-batch-processing.points
type: qa
step: 7
---
## Q
**支付处理系统（授权冻结加每日批量结算） · 批处理规模与一致性**｜必会 · 出自：支付处理系统（授权冻结加每日批量结算） › 深入 3

支付处理器每晚要处理最多约 8 亿行扣款，怎么保证不漏不重、可恢复？

## A
**分区并行。** 按 (network, batchDate) 分区，每分区一个任务，多个文件并行，每个约 100 万行，附清单（行数、总额、校验和）。
**不可变。** 批次 CLOSED 后文件内容不可变，重提交永远发同一份；批次 id 和校验和作幂等键。
**单向状态机。** 按行回写，已 SETTLED 的不会再进下一批。
