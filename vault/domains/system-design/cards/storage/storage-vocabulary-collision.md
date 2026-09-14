---
id: storage-vocabulary-collision
node: storage.record-modeling
type: qa
---
## Q
Two teams share a table with a `status` column. To billing, `active` means "currently paying"; to support, it means "account not banned". Name this schema hazard, describe how it corrupts data without any bug in either codebase, and give the fix that beats "agreeing on a definition."

## A
**Vocabulary collision**: one field name, two meanings — the schema silently encodes two different business concepts in the same column.

How it corrupts: each team reads and *writes* the column under its own semantics. Support "reactivates" an unbanned account → billing starts treating a non-payer as paying. No code is wrong in its own terms; the *data* is now unfalsifiably ambiguous, and every consumer downstream inherits the ambiguity.

Why "agree on one definition" fails: the two concepts genuinely differ, so one team ends up encoding its state *into* the other's vocabulary — the collision returns with the next edge case, and the agreement lives in tribal memory, not the schema.

The durable fix: **split the concepts and rename at the boundary** — separate columns/records (`billing_state`, `moderation_state`) owned by their respective teams, and when data crosses a team boundary, *translate* it into the consumer's vocabulary (an anti-corruption mapping) instead of sharing the raw column. Names in a schema are contracts; two meanings need two names.

## Q zh
两个团队共用一张表的 `status` 列。对计费团队，`active` 意为"正在付费"；对客服团队，它意为"账号未被封禁"。说出这个 schema 隐患的名字，描述它如何在双方代码都没有 bug 的情况下损坏数据，并给出比"统一定义"更好的修法。

## A zh
**词汇冲突（vocabulary collision）**：一个字段名，两种含义 — schema 悄悄把两个不同的业务概念编码进了同一列。

它如何损坏数据：每个团队都按自己的语义读并且*写*这一列。客服"重新激活"一个解封账号 → 计费开始把一个不付费的用户当作付费用户。没有任何代码在它自己的语义下是错的；但*数据*本身已经无法证伪地含糊了，而下游每个消费者都继承了这份含糊。

为什么"统一一个定义"行不通：两个概念确实不同，所以总有一个团队要把自己的状态*塞进*对方的词汇里 — 冲突在下一个边界情形卷土重来，而那份约定活在部落记忆里，不在 schema 里。

耐久的修法：**拆开概念、在边界处改名** — 拆成各自团队拥有的独立列/记录（`billing_state`、`moderation_state`）；当数据跨越团队边界时，把它*翻译*成消费方的词汇（一层 anti-corruption 映射），而不是共享原始列。schema 里的名字是契约；两种含义就需要两个名字。
