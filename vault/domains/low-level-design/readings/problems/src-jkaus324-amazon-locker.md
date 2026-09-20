---
nodes: [problems.machines.amazon-locker]
url: https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier2-intermediate/016-amazon-locker
tags: [no-archive]
---
# machine-coding-interview-questions — 016 Amazon Locker System

值得读：这个仓库把每道题按"基础要求 / 扩展 1 / 扩展 2"分关列出，还附了各关的输入输出样例，
节奏和真实机器编码轮一致，适合用来对照自己的分关拆得全不全。两条关键规则和本题解一致：
小包裹在同尺寸柜格用完时可以占用更大的柜格（它给了一张 SMALL→MEDIUM→LARGE 的降级表），
以及过期**由显式的 `checkExpired(currentTime)` 调用触发**而不是后台定时器——后者正是把时间
注入而非内嵌的做法。分歧有两处：它的降级表把尺寸当成写死的三档全序，本题解用三维偏序加
体积排序，新增尺寸时无需改表；它把通知做成一组必须注册的 `NotificationChannel`，本题解只
发一条不带取件码的事件，短信推送只是众多订阅者之一。实现是五种语言的同一份 Java 风格设计。
（仓库无 LICENSE，只链接不复制。）
