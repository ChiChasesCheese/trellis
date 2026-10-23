---
id: hl-j16-aba
node: java21.j16-concurrency-primitives
type: qa
step: 12
---
## Q
什么是 ABA 问题？用无锁栈举例，说出对策，以及 Java 里什么情况下仍会遇到。

## A
CAS 只比较「值是否还是我读到的」，不管中间变没变过。线程 1 读到 `top=A`、`next=B` 后被暂停；线程 2 弹出 A、弹出 B、再把 A 压回；线程 1 恢复做 `CAS(top, A, B)`，一比还是 A，**成功**，却把 `top` 设成了已被弹走的 B，B 又回到栈里（正确结果应是只剩 C）。

对策：
- 给值加**版本号**：`AtomicStampedReference`（引用 + `int` 戳，CAS 同时比较两者），`AtomicMarkableReference` 是布尔标记版；
- 不复用节点（靠 GC：旧对象还被引用就不会被回收再分配到同一地址）；
- 用锁。

有 GC 的 Java 里纯对象引用的 ABA 少得多，但**节点复用/对象池**、**计数器回绕**、**把值当状态机状态**时仍会遇到。
