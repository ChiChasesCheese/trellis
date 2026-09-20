---
id: problems-pub-sub-cursor-owned-by-topic
node: problems.components.pub-sub
type: qa
step: 2
tags: [grown]
---
## Q
在进程内 Pub-Sub（发布订阅）的设计里，『某个订阅者读到哪了』这个位点（cursor）应该存在订阅对象里，还是存在主题对象里？理由是什么？

## A
存在**主题**里：主题同时拥有那条保留日志和一张 `dict[订阅id, 位点]`，两者由同一把锁保护。

直觉上『我读到哪了』是订阅者的私事，但只要溢出策略里有『阻塞发布者』（BLOCK），日志在淘汰队头之前就必须回答『最慢的那个位点在哪』。把位点散到各个订阅对象里，求最慢位点就得挨个去抢别人的锁，锁序（lock ordering）立刻变成一个需要证明的东西；放在日志旁边，这个问题在一次加锁里就答完了。

主题因此拥有两条不变量：`oldest_seq + size == next_seq`（日志是位点空间上一段连续区间）与 `size <= capacity`（内存有上限）。
