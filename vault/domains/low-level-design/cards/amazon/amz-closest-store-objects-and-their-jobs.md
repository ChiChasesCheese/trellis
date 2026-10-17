---
id: amz-closest-store-objects-and-their-jobs
node: amazon.amz-closest-store
type: qa
step: 2
tags: [grown]
---
## Q
在 Amazon 增删查最近值设计里，应该有哪几个对象？各自只负责一件什么事？

## A
三个核心对象：`NumberStore`（门面）——校验输入是整数、决定平局规则、持有锁；`OrderedIndex`（协议）——只回答 add、remove、count、floor（不大于 x 的最大值）、ceiling（不小于 x 的最小值）；`SortedListIndex` 与 `FenwickIndex` 是它的两个实现。切分依据：「怎么存」会变（值域一出现就换），「怎么比较最近」不变。
