---
id: amz-closest-store-seam-only-where-two-implementations
node: amazon.amz-closest-store
type: qa
step: 5
tags: [grown]
---
## Q
在 Amazon 增删查最近值设计里，存储做成 `Protocol` 接缝（一处两种实现可互换、调用方不用改的位置），但「平局取较小还是较大」只做成一个 `Tie` 枚举，不做成策略类。为什么这样分？

## A
存储有两个真实现（有序列表、树状数组），门面不改就能互换，所以值得一条接缝。平局规则只有两个取值，差别只是 `_prefers_lower` 里的一行比较；做成 `TieBreaker` 抽象类加两个子类，就是三个类干一个布尔值的活。判据：同一职责真有两个以上实现再抽象，否则用枚举或参数。
