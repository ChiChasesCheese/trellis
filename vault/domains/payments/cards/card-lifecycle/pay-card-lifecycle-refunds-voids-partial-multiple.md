---
id: pay-card-lifecycle-refunds-voids-partial-multiple
node: card-lifecycle.refunds-voids
type: qa
step: 3
---
## Q
一笔 100 美元已请款订单要分多次部分退款，系统怎么保证总退款额不超过原金额？账本怎么记？

## A
**场景**：用户买了三件商品，共 100 美元，已请款。
- 第一次退 30 美元（一件商品退货）。
- 第二次退 50 美元（另一件，含运费补偿）。
- 剩余可退 20 美元。

**约束**：累计退款 ≤ 已请款金额。重复提交、并发提交和客服误操作都可能突破它。

**实现**
1. 支付单上维护 `refunded_amount`。创建退款时用条件更新：`UPDATE payment SET refunded_amount = refunded_amount + 50 WHERE id = ? AND refunded_amount + 50 <= captured_amount`，影响行数为 0 就拒绝。
2. 每次退款是独立的退款单，有自己的 id 和幂等键（业务退款单号）。
3. 退款单与支付单关联，状态独立：pending、succeeded、failed。只有 succeeded 才算入"已退款"，失败要把额度还回去。

**账本**（第一次 30 美元，商户待结算已含该笔）
- 借：商户待结算 30（或若已打款则借商户应付，形成负余额）
- 贷：渠道应收 30（等渠道退款清算后，改为银行存款减少）
手续费怎么处理由政策决定：比例退还手续费收入，或不退。

**要点**：部分退款让"一单一状态"不够用，支付单要同时有已请款、已退款、可退三个数。
