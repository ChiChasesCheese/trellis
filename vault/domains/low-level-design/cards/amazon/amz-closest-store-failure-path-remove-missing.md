---
id: amz-closest-store-failure-path-remove-missing
node: amazon.amz-closest-store
type: qa
step: 7
tags: [grown]
---
## Q
在 Amazon 增删查最近值设计里，对不存在的值 `remove(31)` 应该怎么处理？树状数组实现里最容易埋下什么 bug？

## A
门面抛 `ValueNotFoundError`（继承 `LookupError`），并保证集合不变；索引层的 `remove` 返回 `bool` 只报告「删没删成」。bug：树状数组不先检查个数就直接减 1，该值的个数变成 −1，此后 `floor` 会返回一个根本不存在的值。修法：先看计数数组 `cnt[v]` 是否为 0，为 0 直接返回 False；测试断言失败后 `values()` 与之前相同。
