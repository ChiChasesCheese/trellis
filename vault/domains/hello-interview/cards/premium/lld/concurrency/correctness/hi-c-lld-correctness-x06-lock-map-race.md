---
id: hi-c-lld-correctness-x06-lock-map-race
node: lld.concurrency.correctness.exam
type: qa
step: 6
---
## Q
**并发正确性 · 细粒度锁映射的竞态**｜考点 · 必会

`_get_lock(seat)` 里写成 `if seat not in locks: locks[seat] = Lock()`，没有任何保护。有什么问题？

## A
- **问题：** 这本身是先检查后操作；两个线程同时为同一座位创建，各得一把不同的锁，以为互斥，其实没有
- **后果：** 双订回来，而且很难复现
- **修法：** 用一把管理锁保护锁映射的创建，或用 `setdefault`
- **更稳：** 预先创建全部座位的锁，或使用固定数量的锁条带（键哈希到固定个数的锁，内存不随座位增长）
