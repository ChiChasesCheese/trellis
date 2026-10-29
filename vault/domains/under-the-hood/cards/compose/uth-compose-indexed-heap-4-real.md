---
id: uth-compose-indexed-heap-4-real
node: compose.indexed-heap
type: qa
step: 4
---
## Q
**真实实现多做了什么：任务自带下标**｜Java ScheduledThreadPoolExecutor · JDK 21

JDK 的定时线程池怎样实现取消？和「懒删除」相比，取舍是什么？

## A
**结构。** `DelayedWorkQueue` 的堆数组里放 `ScheduledFutureTask`，任务对象自带 `heapIndex` 字段，记着自己在数组里的下标，起到「key → 下标」表的作用，却不用另建哈希表；每次上浮、下沉搬动元素都顺手写下标，移出堆后置为 -1。

**细节。**

- 整个队列一把 `ReentrantLock`；只有一个「领头」线程睡到堆顶到期，其余线程无限期等，减少无谓的定时唤醒。
- 到期时刻相同时靠递增的 `sequenceNumber` 保持先进先出；数组初始 16 格，满了扩 50%。
- Go 的 `container/heap` 同样要自己存下标（官方示例里的 `Item.index`），再调用 `Fix` 或 `Remove`；Kubernetes 的堆因对象不带下标，另存一张 key 到 {对象, 下标} 的表。

**为什么。** Python `heapq` 文档的做法是把旧条目标成已删除、另插一个新条目（懒删除）：取消 O(1)，代价是垃圾留在堆里。带下标则取消是 O(log n)，堆里没有垃圾。

**坑。** 定时线程池默认不会在取消时摘掉任务（`removeOnCancel` 默认 false），它们留在堆里直到原定时间：大量「长超时、成功后取消」的任务会把内存撑起来，要调用 `setRemoveOnCancelPolicy(true)`。

**对应 LeetCode：** 无直接对应的题
