---
id: hl-j16-synchronized
node: java21.j16-concurrency-primitives
type: qa
step: 10
---
## Q
`synchronized` 提供什么保证？HotSpot 怎么实现？JDK 21 虚拟线程下要注意什么？

## A
- **互斥**（同一时刻只有一个线程进入）+ **HB**（unlock HB 之后的 lock）。进入 = 获取 monitor，退出（含异常退出）= 释放。粗但安全。
- HotSpot 实现：先是**轻量级锁**（对象头上 CAS），竞争时**膨胀成重量级 monitor**（阻塞线程要走内核）。
- JDK 21：虚拟线程里**持锁阻塞会 pin** 载体（J10）；JDK 24 起不再 pin。
