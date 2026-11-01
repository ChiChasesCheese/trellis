---
id: hi-pt-tt-payment-reconciliation-2-three-way
node: tt.sd.tt-payment-reconciliation.points
type: qa
step: 2
---
## Q
**支付对账系统 · 为什么三方**｜出自：支付对账系统 › 取舍与追问

对账为什么要内部账本、PSP 报告、银行流水三方，而不是账本对银行或账本对 PSP 两方？

## A
**账本对 PSP。** 证明每笔交易两边都有且金额一致，但证明不了钱到了。
**PSP 批次对银行。** 证明 PSP 说要付的钱真的到了。
**不能只对银行。** 银行只有汇总，差异无从定位。
**桥。** PSP 结算批次是把明细和入账连起来的桥；两层叠加，账本上的应收 PSP 款才变成银行里的现金。
