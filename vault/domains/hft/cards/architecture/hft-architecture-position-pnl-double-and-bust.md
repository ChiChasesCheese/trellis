---
id: hft-architecture-position-pnl-double-and-bust
node: architecture.position-pnl
type: qa
step: 5
---
## Q
持仓与盈亏计算里常见的两类错误是什么？为什么金额要用整数而不是 double？

## A
**1. 浮点误差。** 在 double 里 `0.1 + 0.2` 的结果是 0.30000000000000004。亿万笔累加之后账对不上，重放时也可能和线上不一致。做法：价格用整数定点（比如 0.0001 元为单位的 `long`），金额用整数，乘法检查溢出（`Math.multiplyExact`）。

**2. 成交被更正或取消（trade bust）。** 交易所有时会事后撤销某笔成交。若持仓只是累计成一个数字，没保存成交序列，就无法冲销这笔成交。

所以要保存成交序列，持仓由它推出，并持续与 drop copy 和清算数据对账（drop copy 是交易所发来的独立副本）；出现差异就停止对相关品种发新单。
