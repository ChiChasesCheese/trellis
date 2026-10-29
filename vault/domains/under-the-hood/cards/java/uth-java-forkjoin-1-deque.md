---
id: uth-java-forkjoin-1-deque
node: java.forkjoin
type: qa
step: 1
---
## Q
**工作窃取是怎么偷的**｜Java · OpenJDK 25

`ForkJoinPool` 的每个线程有自己的任务队列，空闲的线程怎么从别人那里「偷」任务？

## A
**结构。** 每个工作线程一个双端队列（deque）：环形数组，初始 64 个槽，数组长度是 2 的幂。

**细节。**

- 自己：`fork` 把子任务压到栈顶（`top`），取任务也从栈顶弹出，后进先出（LIFO）。
- 窃取者：从另一端 `base` 用 CAS 取走最老的任务，先进先出（FIFO），且随机扫描挑受害者。
- 异步模式（`asyncMode`）下，自己也改为 FIFO。

**为什么。** 主人和小偷分在两端，平时不抢同一端，几乎无锁；比起生产者给空闲线程派活，小偷自己去找更快。

**对应 LeetCode：** LC 912 排序数组 · LC 23 合并 K 个升序链表
