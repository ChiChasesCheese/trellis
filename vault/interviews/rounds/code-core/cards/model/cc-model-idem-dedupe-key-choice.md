---
id: cc-model-idem-dedupe-key-choice
node: model.idempotency
type: qa
---
## Q
Chargeback records carry a `transaction_id` that is unique *per network*. What is the de-duplication key, and why does it matter?

## A
**`(network, transaction_id)` — the composite, not the id alone.**

With the id alone, a Visa dispute and a Mastercard dispute that happen to share an id become the same dispute: one withdrawal cancels both, one duplicate check suppresses a legitimate record.

The general move is to read the uniqueness sentence literally — "unique per network", "loan ids are unique per merchant", "the same customer at two merchants has two separate counters" — and make the key the full scope the sentence names. A key that is too narrow merges distinct entities, and the merge is invisible in the output.

## Q zh
退单记录带一个 `transaction_id`，它**在每个卡组织内**唯一。去重 key 是什么？为什么重要？

## A zh
**`(network, transaction_id)` —— 复合 key，而不是单独的 id。**

只用 id 的话，恰好共享同一 id 的 Visa 争议和 Mastercard 争议就成了同一笔争议：一次撤回同时取消两者，一次重复判定压掉一条合法记录。

通用做法是照字面读唯一性那句话 —— 「每个卡组织内唯一」「贷款 id 在每个商户内唯一」「同一顾客在两个商户有两个独立计数器」 —— 并让 key 覆盖该句点名的完整作用域。key 取窄了会把不同实体合并，而这种合并在输出里看不出来。
