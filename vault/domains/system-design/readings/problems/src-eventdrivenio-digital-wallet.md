---
nodes: [problems.commerce.digital-wallet]
url: https://event-driven.io/en/bank_account_event_sourcing/
tags: [no-archive]
---
# Why a bank account is not the best example of Event Sourcing?

值得读：事件溯源社区知名从业者 Oskar Dudycz 的博客，指出银行账户是教学事件溯源的一个
容易误导的例子，并给出具体计算——一个日均 3 笔交易的账户运行 17 年会累积约 18,600 个
事件，全量重放会让账户越老查询越慢。与本题解不同的地方在于：原文的结论是"换一个更
简单的教学例子"，本题解正面处理金融领域这个"困难例子"，把原文提醒的快照必要性落到
具体的快照频率设计上（见题解「深入探讨」第 4 节）。标记 `no-archive` 是因为这是一篇
个人技术博客而非公司工程博客，观点属于作者个人，不代表任何公司的生产实践披露。
