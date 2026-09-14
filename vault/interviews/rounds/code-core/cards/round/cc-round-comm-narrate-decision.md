---
id: cc-round-comm-narrate-decision
node: round.communication
type: qa
---
## Q
You are implementing on a call and have been silent for two minutes. What do you say?

## A
**Narrate the decision, never the syntax.**

- Signal: "I'm keying charges by id so a dispute can find its merchant in O(1) — costs one extra dict, and it's the thing the reversal part will need."
- Noise: "now I write a for loop over the list."

The shape is: what I am choosing between, what I picked, why, what it costs. If you genuinely need quiet, buy it explicitly — "give me sixty seconds to write this loop and then I'll walk you through it" — which reads as control rather than as being lost.

## Q zh
你正在电话里写代码，已经沉默了两分钟。这时说什么？

## A zh
**讲决策，绝不讲语法。**

- 有信息量：「我用 id 给 charge 建索引，这样争议来的时候能 O(1) 找到商户 —— 代价是多一个 dict，而且撤销那一部分正需要它。」
- 噪音：「现在我写一个 for 循环遍历列表。」

句式是：我在哪两者之间选、选了什么、为什么、代价是什么。如果确实需要安静，就明确地把它买下来 —— 「给我六十秒写完这个循环，然后我走一遍」 —— 这听起来是掌控，而不是迷路。
