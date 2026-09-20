---
id: problems-food-delivery-saga-compensation-capture-timing
node: problems.geo.food-delivery
type: qa
step: 3
tags: [grown]
---
## Q
In a food delivery order saga, why does whether payment has already been captured (not just authorized) determine whether a failure's compensating action is a cheap authorization void or an actual refund?

## A
An authorization hold that has not yet been captured represents no real movement of funds, so voiding it is close to free and instantaneous — this is the right compensation for an early failure like the merchant rejecting the order before any real cost has been incurred. Once payment has been captured (typically because the merchant has already started preparing the order, representing a real, sunk cost), a later failure such as a dispatch timeout can't be treated as if nothing happened; the compensating action has to be an actual refund, and often only a partial one, because real cost was already incurred. This means the saga's compensation logic isn't uniform across all failure points — it depends on how much of the transaction's real-world effect is already irreversible at the point of failure.

## Q zh
在一个外卖订单的 saga（编排式工作流）里，为什么支付是否已经被扣款（capture，而不只是授权 authorize）会决定失败时的补偿动作是一次几乎零成本的授权撤销，还是一次真正的退款？

## A zh
一笔尚未 capture 的支付授权（authorization hold）没有产生真实的资金转移，所以撤销它几乎零成本、即时完成——这适合商户在产生任何真实成本之前就拒绝订单这类早期失败。一旦支付已经被 capture（通常是因为商户已经开始备餐，产生了真实的沉没成本），之后再发生的失败（比如调度超时找不到骑手）就不能当作什么都没发生过来处理；这时补偿动作必须是一次真正的退款，而且往往只能是部分退款，因为真实成本已经产生。这说明 saga 的补偿逻辑在各个失败点上并不是统一的——它取决于失败发生时，这笔交易对真实世界的影响已经有多少变得不可逆。
