---
id: hl-cq-q28-deadlock-scoped-lock
node: cpp-questions.g-concurrency
type: qa
step: 4
---
## Q
两个线程在两个账户之间反向转账，为什么会死锁？用 `std::scoped_lock` 怎么写才不死锁？

## A
- 死锁：线程 1 先锁 A 再锁 B，线程 2 先锁 B 再锁 A，互相等待。
- 修法：`std::scoped_lock lk(from.m, to.m);` 同时锁两个互斥量，无论参数顺序都不会死锁。
- 实测：双方各转 10 万次后余额仍是 1000 + 1000。
- 另一个办法是约定**统一的加锁顺序**。
