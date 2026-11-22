---
id: tc-answer-first
node: t01.answer-first
type: qa
step: 1
tags: [原则]
---
## Q
**Answer first · 首句规则**｜原则 · 必会

面试官问："你们当时为什么选 Kafka 而不是 RabbitMQ？"你脑子里有六七条背景和理由。第一句话该说什么？

## A
**原则：** 第一句就给**结论**，再给理由。听的人一次只能接收一句话；你先说结论，他就知道后面每句话是在回答"为什么"，不用自己猜你要去哪。

**怎么做：**
1. 开口前先在心里写一句话：我的答案是什么。
2. 第一句只说这个答案，不铺垫背景。
3. 第二句起才讲理由，理由按重要程度排。
4. 对方追问再下潜到细节。

**常见错法：**
- **从背景讲起：** 讲了一分钟，听的人还在猜你的立场。
- **先讲过程再讲结论：** "我们先试了 A，后来发现…"，听的人要自己拼出结论。
- **结论藏在最后一句：** 一旦被打断，结论根本没说出口。

**改写示例：**
- Before: "So we had this order pipeline, and traffic was growing, and we looked at a few queues, and RabbitMQ had some limits on replay, so in the end we went with Kafka."
- After: "We chose Kafka because we needed to replay events. Two reasons: it keeps messages after they are consumed, and it scales by partition. RabbitMQ would have required extra tooling for both."

**出处：** Minto p. 25–32（Ch.1 Why a Pyramid Structure：Ordering from the Top Down）；p. 41–48（Ch.3 The Top-Down Approach）
