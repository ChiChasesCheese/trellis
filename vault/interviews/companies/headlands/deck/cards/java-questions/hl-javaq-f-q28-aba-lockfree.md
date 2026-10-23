---
id: hl-javaq-f-q28-aba-lockfree
node: java-questions.f-concurrency
type: qa
step: 12
---
## Q
什么是 CAS 的 ABA 问题，怎么解决？什么情况下无锁值得用、什么情况下不值得？自己做无锁结构该怎么办？

## A
- **ABA**：线程 1 读到 A，线程 2 把 A→B→A，线程 1 的 CAS 成功，但中间状态已经变了。解决：带版本戳（`AtomicStampedReference`）或让数据不可变。
- **值得无锁**：竞争低、临界区极短、不能阻塞（实时 / 热路径）、要避免优先级反转 / 锁护航。
- **不值得**：竞争高、需要多变量一致性。
- 自己做无锁结构很难，用现成的：`ConcurrentLinkedQueue`、`ConcurrentSkipListMap`、`ArrayBlockingQueue` + 单线程所有者模式（mechanical sympathy：一个线程拥有数据，其他线程通过队列发消息）。
- 热路径偏好单写者设计加队列，而不是花哨的无锁结构。
