---
id: hi-c-sd-gopuff-b02-ssi-and-claim
node: sd.problem-breakdowns.gopuff.beyond
type: qa
step: 2
---
## Q
**即时配送库存 · 拓展：Postgres 的 SERIALIZABLE 是怎么实现的**｜拓展 · 加分

SERIALIZABLE 在 Postgres 里不是靠锁住一切实现的，它到底做了什么？有什么代价？

## A
- **机制：** Postgres 的 SERIALIZABLE 是可串行化快照隔离（SSI）：事务在快照上运行，不阻塞读，同时记录读写之间的依赖关系（谓词锁），检测出可能导致不可串行化的环就中止其中一个事务。
- **代价：** 检测偏保守，会有误报（并没有真的冲突也被中止）；跟踪读写依赖需要内存，大范围扫描的事务代价更高。所以应用必须能重试。
- **和显式锁的区别：** 显式加 `SELECT ... FOR UPDATE` 是悲观锁，读的时候就阻塞别人；SSI 是乐观的，冲突在提交时才发现。
- **热点库存的另一种写法：** 热门商品的单行计数器（数量列）会成为热点，并发更新排队；若库存是一行一件实物，可以用 `FOR UPDATE SKIP LOCKED` 让每个事务直接领走一件还没被锁住的行，避免互相等待。
- **缩小事务：** 事务里不要做网络调用，查询行程时间等放在事务之前完成。
