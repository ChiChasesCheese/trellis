---
nodes: [problems.social.stack-overflow]
url: https://algomaster.io/learn/lld/design-stack-overflow
tags: [no-archive]
---
# AlgoMaster — Design Stack Overflow

值得读：商业站点，只链接不摘录。Java 实现，与 ashishps1 仓库同一作者、同一套结构：
`Comment` 继承 `Content` 而不是 `Post`（评论天生不能被投票，靠类型系统而不是运行时判断
排除），声望是 `User` 上的 `AtomicInteger`、由 `ReputationManager` 在收到投票事件时直接
加减——用原子类型解决的是"并发写同一个整数"的问题，不解决"这个整数会不会因为一次改票
而算错"的问题，这正是本题解要害。

文章明确说关闭与删除问题超出了它设定的需求范围，没有实现——本题解第 3 关正是要把这两个
行为、以及它们对回答的影响说清楚。
