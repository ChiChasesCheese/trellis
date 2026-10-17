---
id: amz-closest-store-concurrency-one-lock-two-reads
node: amazon.amz-closest-store
type: qa
step: 8
tags: [grown]
---
## Q
在 Amazon 增删查最近值设计里，多个线程同时 add、remove、closest，为什么即使有 GIL 也要加锁？锁放在哪一层、锁多大？

## A
`closest` 要读 `floor(target)` 与 `ceiling(target)` 两次，GIL 只保证单条字节码原子，两次读之间另一个线程可能删掉其中一个，得到「从未同时存在过」的答案；树状数组一次写更新 O(log R) 个节点，读到一半会看到半成品。做法：门面 `NumberStore` 的每个公开方法持有同一把 `threading.Lock`，临界区只含索引调用（微秒级）。读写锁、写时复制在这个体量下得不偿失。
