---
id: amz-file-watcher-edge-callback-failure-isolation
node: amazon.amz-file-watcher
type: qa
step: 7
tags: [grown]
---
## Q
在 Amazon 文件监听器设计里，一个订阅者的回调抛异常、或在回调里订阅、取消订阅，会发生什么？怎么设计才不会出事？

## A
回调若在锁内调用，回调里再订阅就死锁（`Lock` 不可重入）。做法：锁内复制事件和订阅者列表，释放锁后再逐个调用；每个回调单独 `try/except`，异常记进有上限（如 100 条）的失败队列，其余订阅者和下一轮轮询照常。无上限的失败列表会随一个一直出错的订阅者无限增长。
