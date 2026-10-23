---
id: hl-os-spsc-memory-order
node: foundations.os-processes-threads-ipc
type: qa
step: 26
---
## Q
SPSC 环形缓冲为什么需要内存序（memory ordering）？`setRelease` 和 `getAcquire` 怎么配对？只在 x86 上能跑的「碰巧正确」为什么不可靠？

## A
生产者先写数据 ①，再更新 `tail` ②。若消费者看到新 `tail` 却**看不到**数据 ①（硬件或编译器重排，或数据还在写缓冲里），就读到垃圾。

用 `VarHandle` 的有序访问：
- **`setRelease`**（释放写）：之前的所有写，在另一线程看到这次写之后都可见；
- **`getAcquire`**（获取读）：之后的所有读不会被重排到它之前。

配对：生产者 `setRelease(tail)` 与消费者 `getAcquire(tail)` 构成 *synchronizes-with*，消费者看到新 `tail` 时槽位的写一定可见；对称地，消费者 `setRelease(head)` 与生产者 `getAcquire(head)` 保证读完槽位后生产者才能覆盖。

x86 的内存模型（TSO）本就禁止写-写重排，所以不加屏障常「碰巧能跑」；但 ARM（Apple 芯片、AWS Graviton）模型很弱会出真 bug，即使在 x86 **JIT** 也可能重排普通读写或把读提到循环外。
