---
id: amz-locker-onsite-dry-run-trace-one-package
node: amazon.amz-locker-onsite
type: qa
step: 4
tags: [grown]
---
## Q
在 Amazon 现场版快递柜里，代码不会被运行时，怎样用手工推演证明它是对的？给一个具体的推演。

## A
写完后选一个包裹逐行走一遍，每步写出空闲集合和码表。三个柜格 S、M、L 全空，投一个小包裹：三个柜格都装得下，取体积最小的 S，空闲变 {M, L}，码表 {AB12: S}。取件 AB12：码表变 {}，S 回到空闲 {S, M, L}。再取 AB12：码表里没有，抛 `UnknownCode`。再补一条过期路径：时钟越过期限后取件，抛 `ExpiredCode`。四个状态表写在记事本边上，就是证据。
