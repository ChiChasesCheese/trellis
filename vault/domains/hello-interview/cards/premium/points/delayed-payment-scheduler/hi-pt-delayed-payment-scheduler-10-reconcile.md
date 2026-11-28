---
id: hi-pt-delayed-payment-scheduler-10-reconcile
node: qb.sd.delayed-payment-scheduler.points
type: qa
step: 10
---
## Q
**延迟支付调度服务 · 对账不变量**｜追问 · 出自：延迟支付调度服务 › 深入 6

延迟转账服务每天要核对账务是否正确。哪些不变量可以自动检查？

## A
**不变量一。** 所有钱包余额加上所有未完成预约的金额，等于总发行量。
**不变量二。** 每条 COMPLETED 的预约恰有一条 CREDIT 分录，反之亦然。

差异报警。这两条能抓出重复入账、漏入账和状态卡死。
