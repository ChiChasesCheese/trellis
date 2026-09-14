---
id: cc-model-sm-effect-on-edge
node: model.state-machine
type: qa
---
## Q
Money moves when a payment succeeds. Do you credit the merchant on entering `COMPLETED`, or on the `SUCCEED` transition?

## A
**On the transition — a side effect belongs to an edge, not to a state.**

Attaching it to the state invites double-crediting the moment any other edge can reach `COMPLETED`, or any command re-asserts the state. Attaching it to the edge means it fires exactly as often as the edge is taken, which the guard already limits to once.

The same rule explains the neighbouring rules: `SUCCEED` on an already-completed payment is ignored (no edge, no credit), and a refund is its own edge with its own inverse effect — never a re-entry into an earlier state.

## Q zh
付款成功时资金入账。你在**进入** `COMPLETED` 时给商户入账，还是在 `SUCCEED` 这条**转移**上入账？

## A zh
**在转移上 —— 副作用属于边，不属于状态。**

把它挂在状态上，一旦有别的边也能到达 `COMPLETED`，或者有命令重复断言该状态，就会重复入账。挂在边上则意味着它触发的次数恰好等于这条边被走的次数，而守卫已经把它限制为一次。

同一条规则也解释了相邻的规则：对已完成付款再执行 `SUCCEED` 会被忽略（没有走边，就不入账）；退款是它自己的一条边、带自己的逆向副作用 —— 绝不是回到更早状态的一次重入。
