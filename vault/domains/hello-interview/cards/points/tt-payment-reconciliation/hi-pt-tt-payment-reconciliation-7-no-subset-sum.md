---
id: hi-pt-tt-payment-reconciliation-7-no-subset-sum
node: tt.sd.tt-payment-reconciliation.points
type: qa
step: 7
---
## Q
**支付对账系统 · 不做子集和**｜必会 · 出自：支付对账系统 › 深入 1

对账系统里银行一条入账等于几万笔明细之和，没有批次号怎么找哪些交易加起来等于这个数？

## A
**要点。** 不要做子集和：NP 难问题且有多个解。
**正确做法。** 用 PSP 文件中的批次号，把 PSP 明细先按批汇总，再拿汇总额匹配银行入账。
**扩展性。** 两边按交易号哈希分片、每片排序，双指针流式比对，内存只放一个分片；重跑写新 run_id，完成后原子切换。
