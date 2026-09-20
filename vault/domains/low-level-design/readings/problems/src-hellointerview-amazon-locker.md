---
nodes: [problems.machines.amazon-locker]
url: https://www.hellointerview.com/learn/low-level-design/problem-breakdowns/amazon-locker
tags: [no-archive]
---
# Hello Interview — Low-Level Design: Amazon Locker

值得读：商业课程的题目拆解，Python 代码，强项是把面试官的追问顺序理得很清楚（先分配，
再取件码，再过期，再异常），可以拿来校准自己的分关节奏。它的核心对象是三个：`Locker`
（大管家，同时管柜格表和码表）、`Compartment`（带一个 `occupied` 标志的柜格）、`AccessToken`
（带 7 天有效期的持有即凭证）。本题解在三处不同意：尺寸它做成 `SMALL/MEDIUM/LARGE` 枚举并
严格匹配（"没有对应尺寸的柜格就拒绝投递"），我做成带三维的值对象加"最小可容纳"，好让第 4 关
新增尺寸时分配逻辑一行不改；有效期它写死在令牌里，我做成网点的构造参数；它没有讨论连续
输错码该按什么维度限流，而那恰恰是"一次性码不是密码"这条性质最锋利的推论。付费站点，
只链接不摘录。
