---
id: cc-model-state-two-counters-not-a-list
node: model.entity-state
type: qa
---
## Q
You need, per merchant, "how many charges" and "how many of them were fraudulent", over 10^5 events. Keep a list of that merchant's charges, or two integers?

## A
**Two integers — the counters are the state; the list is a re-derivation you would pay for on every event.**

Re-scanning a merchant's charges after each event is O(n) per event and quadratic overall; two counters make the same question O(1) and make the flag re-evaluation trivially cheap.

Keep a record of individual events **only** when something must later address one of them by id — a reversal needs `charge_id -> (merchant, was_fraud)`. That is a separate index with a separate purpose, not a substitute for the counters. See [[cc-model-rev-subtract-both-counters]].

## Q zh
在 10^5 个事件上，你需要按商户统计"共有多少笔扣款"和"其中多少笔是欺诈"。存该商户的扣款列表，还是两个整数？

## A zh
**两个整数 —— 计数器本身就是状态；列表是一种你要在每个事件上付费的重新推导。**

每来一个事件就重扫该商户的扣款，是每事件 O(n)、整体平方级；两个计数器让同一个问题变成 O(1)，也让重新判定标记变得极其便宜。

只有当后续必须按 id 定位到某个具体事件时，才保留逐条记录 —— 撤销需要 `charge_id -> (merchant, was_fraud)`。那是一个用途不同的独立索引，不是计数器的替代品。见 [[cc-model-rev-subtract-both-counters]]。
