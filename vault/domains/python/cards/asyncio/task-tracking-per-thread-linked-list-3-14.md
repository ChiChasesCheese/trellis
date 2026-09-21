---
id: task-tracking-per-thread-linked-list-3-14
node: asyncio.coroutines-tasks
type: qa
source: cpython-internals
---
## Q
CPython 在 3.14 之前用全局 `WeakSet` 存放事件循环里所有存活的 Task，3.14 改成了什么结构，动机是什么？

## A
3.14 改为每个线程各自维护一条环形双向链表（doubly linked list，节点直接嵌在 Task 对象里，免去额外分配），当前任务也从「事件循环到当前任务」的全局字典改成存在每个线程的线程状态（`PyThreadState`）里。动机有三点：全局 `WeakSet`+字典查找性能差；旧实现在多线程下并发遍历 `WeakSet` 不安全；自由线程（free-threading）下多个事件循环并发添加/删除任务时，全局结构会造成严重锁竞争，按线程拆分后可以做到免锁（lock-free）增删。
