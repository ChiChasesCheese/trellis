---
id: cc-model-rev-zero-over-zero
node: model.reversal
type: cloze
---
When every one of a merchant's charges has been reversed, the ratio test becomes {{c1::0 / 0}} — a `ZeroDivisionError` in float form and a silently true comparison in the cross-multiplied form, since {{c2::`0 * den >= num * 0`}} holds for any threshold. The guard is to require {{c3::`total > 0` (and any stated minimum volume) before the threshold is even considered}}, which also covers an entity that was created but never charged.

## zh
当某商户的所有扣款都被撤销后，比率判断变成 {{c1::0 / 0}} —— 浮点写法会抛 `ZeroDivisionError`，交叉相乘写法则会静默地成立，因为 {{c2::`0 * den >= num * 0`}} 对任何阈值都为真。保护措施是在考虑阈值之前先要求 {{c3::`total > 0`（以及题面规定的最小交易量）}}，这同时也覆盖了"已创建但从未发生扣款"的实体。
