---
id: hi-pt-credit-token-balance-5-accept-rule
node: qb.lld.credit-token-balance.points
type: qa
step: 5
---
## Q
**额度账本 · 接受迟到事件的条件**｜必会 · 出自：额度账本 › 深入 3

一笔迟到的扣费到达，什么条件下接受？为什么不一律拒绝，也不一律接受？

## A
**条件。** 重放之后每笔已接受的扣费仍能全额扣下，否则抛 `InsufficientCreditsError`，账本不变。

**为什么。** 一律拒绝会丢账（乱序是常态）；一律接受会让已告诉调用方成功的扣费事后失败。**代价。** 迟到的扣费有时被拒绝。

**现象。** 迟到事件会改变旧扣费用了哪些包（`c1` 迟到后，`c2` 从 `g1` 变成 `g2`），总额不变。
