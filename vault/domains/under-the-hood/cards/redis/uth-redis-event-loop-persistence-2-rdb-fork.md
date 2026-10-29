---
id: uth-redis-event-loop-persistence-2-rdb-fork
node: redis.event-loop-persistence
type: qa
step: 2
---
## Q
**RDB 快照时为什么不停服**｜Redis · 8.10

`BGSAVE` 要把几十 GB 内存写盘，主线程怎么还能处理写命令？

## A
**结构。** `fork()` 出子进程：子进程看到 fork 那一刻的内存，慢慢写盘；父进程照常服务。

**细节。**

- 靠写时复制（copy-on-write）：父子共享内存页，谁改某一页才复制那一页
- 快照期间写得越多，复制的页越多，额外内存越多
- 默认触发：1 小时 1 次修改、5 分钟 100 次、1 分钟 10000 次，满足任一条

**为什么。** 不在主线程里遍历写盘，也不加锁就拿到一致快照。

**坑。** 数据集很大时，`fork()` 本身可能停服几毫秒到一秒。

**对应 LeetCode：** LC 1146 快照数组 · LC 981 基于时间的键值存储
