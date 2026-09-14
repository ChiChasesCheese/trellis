---
id: cc-round-comm-confirm-with-a-test-case
node: round.communication
type: qa
---
## Q
The rule "a payment may settle several invoices, oldest first" is clear enough to code, but you are not certain you read it the way the author meant. What is the cheapest way to check?

## A
**Propose a concrete micro-example with your expected output and ask for a yes/no.**

> "A payment of 250 against invoices of 100 (January) and 200 (February): I'd clear the 100, put 150 on the second, leave 50 owed and nothing unapplied — right?"

A worked example resolves an ambiguity faster than a prose question, it is checkable in one breath, and whichever way the answer goes you leave with a test case. Use the same move on yourself in a timed round: hand-compute the example before coding the rule.

## Q zh
规则「一笔付款可以清算多张发票，最早到期的优先」已经清楚到能写代码了，但你不确定自己的读法和出题人一致。最省事的核对办法是什么？

## A zh
**提出一个带你期望输出的具体小例子，请对方回答是或否。**

> 「一笔 250 的付款，对应 100（一月）和 200（二月）两张发票：我会付清 100，再把 150 记到第二张，剩 50 未付、没有未分配金额 —— 对吗？」

一个算好的例子比一句抽象提问更快解决歧义，一口气就能核对，而且无论答案是哪边，你都带走了一个测试用例。限时笔试里对自己用同一招：先手算例子，再写规则。
