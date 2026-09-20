---
id: problems-splitwise-canonical-key-and-shrink
node: problems.marketplaces.splitwise
type: qa
step: 2
tags: [grown]
---
## Q
分账（Splitwise）系统的余额账本用 `dict[(User, User), int]` 存每一对用户的净额。为什么键必须规范化（canonical，按用户 id 排序后再组成元组），以及为什么净额归零时必须把整行删掉而不是留一个 0？

## A
不规范化就会出现 (A,B) 和 (B,A) 两行各存一份方向相反的欠款：一次结算只改其中一行，两行迟早对不上，而且“A 欠 B 3 元、同时 B 欠 A 5 元”这种状态本身就不该存在。按 id 排序把一对人折成唯一一行，方向由值的正负号表达。归零就删行则是“容器必须会缩小”：账本是这个设计里唯一会无限增长的容器，结清过的人对如果各留一个 0，几年后遍历和查询都要为这些历史死条目买单。代码上就是 `if new == 0: self._net.pop(key)` 而不是 `self._net[key] = 0`。
