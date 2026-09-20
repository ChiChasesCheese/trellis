---
nodes: [problems.social.task-management]
url: https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier1-foundation/005-issue-resolver
---
# machine-coding-interview-questions — Customer Issue Resolution System

值得读：不是任务看板本身，而是相邻的一道题——客服工单按策略分派给客服、状态在
`OPEN → IN_PROGRESS → RESOLVED → CLOSED` 间转移、状态变化通知观察者。五种语言实现，
Python 版把转移规则写成一串 `(old == X and new == Y) or (old == Y and new == Z) or …`
的布尔表达式，状态和优先级用普通类属性（`class Priority: LOW = 0`）而不是 `Enum` 表达。
两处都是本文明确要避开的写法：转移规则本文用一张按看板声明的 `dict[str, set[str]]`
表达，加一条边不用碰判断表达式本身；有限状态集合本文用 `Enum`，能被类型检查器和
`match`/相等比较正确处理，不会有拼写错误的字符串常量悄悄通过。它的指派策略
（round-robin/least-loaded/specialist）三个类共享同一个只有一个方法的接口，是运行时确实
会被替换实现的正当策略模式用例——和本文"分账不用策略类"那条决策形成对照：判据是运行时
会不会真的换实现，这里会，所以类层级是合理的。
