---
id: problems-e-commerce-order-saga-pivot-ordering
node: problems.commerce.e-commerce
type: qa
step: 6
tags: [grown]
---
## Q
In an e-commerce order saga spanning inventory, payment, fulfillment, and notification, why should inventory reservation happen before payment, and payment happen before fulfillment, rather than some other order?

## A
Saga steps should be ordered so the hardest-to-compensate action comes last (the 'pivot' comes after everything cheaply reversible). Releasing an inventory reservation is nearly free (it's just letting a TTL expire or clearing a row), so it goes first. Payment involves real money movement and its compensation is a refund — more costly than releasing a reservation, so it comes after inventory is locked. Fulfillment (shipping) is nearly irreversible once triggered, so it must wait until payment is confirmed successful. This ordering minimizes the cost of the compensations that actually run when a later step fails.

## Q zh
在跨库存-支付-履约-通知的电商订单 saga 中，为什么库存预留要在支付之前、支付要在履约之前，而不是其他顺序？

## A zh
saga 步骤应该让最难补偿的动作排在最后（转折点/pivot 放在所有廉价可逆的步骤之后）。释放库存预留几乎零成本（只是让 TTL 过期或清掉一行），所以排最前。支付涉及真实资金移动，其补偿是退款——比释放预留代价更高，所以在库存锁定之后进行。履约（发货）一旦触发几乎不可逆，所以必须等支付确认成功后才能进行。这个顺序把后续步骤失败时真正要执行的补偿代价降到最低。
