---
id: hl-bs-r1-followups-a
node: behavioral.stories
type: qa
step: 6
---
## Q
被追问个人研究平台 R1：为什么是四个接口？为什么点时？为什么账本只增不改？有策略被拦过吗？
Why four interfaces? Why point-in-time? Why an append-only ledger? Was a strategy ever blocked?

## A
- **Why four interfaces?** 新市场只是一个**薄适配器**，策略代码**不用改**。
- **Why point-in-time?** 否则回测会**用到当时拿不到的信息**。
- **Why an append-only ledger?** 防止**只记录赢家**。【待补：你的具体理由】
- **Was a strategy ever blocked?** 【待补：哪道门拦下的】
