---
id: cc-round-hidden-second-occurrence
node: round.hidden-tests
type: qa
---
## Q
Which single input mutation catches the most hidden tests across payments, scheduling and ledger problems?

## A
**Repeat a line.** Duplicating one record probes de-duplication, idempotency, group counters and reversal at once, and it is trivial for a test author to write.

Ask, for each repeated record: does the second occurrence apply again, become a no-op, or get rejected? Statements say this in a half-sentence — "a repeated id is ignored", "a second reversal has no effect", "duplicate rows are separate transactions and count towards both group counters" — and the three answers are genuinely different. Never assume; find the sentence, and if there is none, decide and comment. See [[cc-model-idem-second-occurrence-noop]].

## Q zh
哪一种输入变形，在支付、调度和账本类题目中能抓到最多隐藏测试？

## A zh
**把一行重复一遍。** 复制一条记录能同时探测去重、幂等、分组计数和撤销，而且对出题人来说写起来毫不费力。

对每条重复记录都要问：第二次出现是再次生效、变成 no-op，还是被拒绝？题面往往只用半句话交代 —— 「重复的 id 被忽略」「第二次撤销无效」「重复行是各自独立的交易，两个分组计数器都要计」 —— 而这三种答案真的不同。绝不假设；去找那句话，找不到就自己决定并写注释。见 [[cc-model-idem-second-occurrence-noop]]。
