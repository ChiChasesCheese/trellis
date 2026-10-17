---
id: amz-splitwise-concurrent-expenses
node: amazon.amz-splitwise
type: qa
step: 6
tags: [grown]
---
## Q
在分账设计里，两个人同时往同一个群里记账，会出什么错？怎么防？

## A
两条线程都「读 A–B 余额 → 加上自己的份额 → 写回」，后写的覆盖先写的，丢掉一笔（丢失更新，lost update）。做法：分摊的计算是纯函数，放在锁外；「更新这笔支出涉及的所有余额行」放在一把锁里，保证一笔支出要么全部生效要么都不生效，不会有人读到只更新了一半的账。`settle`（还款）用同一把锁。规模大了按群分锁，不同群互不阻塞。
