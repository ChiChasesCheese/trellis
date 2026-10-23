---
id: hl-cq-q34-pitfall-sync
node: cpp-questions.h-os
type: qa
step: 14
---
## Q
跨进程共享内存里怎么做同步？普通变量能当标志吗？进程间互斥有哪些选择？跨平台要注意什么？

## A
- 普通变量**不能**当标志；用 `std::atomic`，而且必须无锁（用 `is_always_lock_free` 检查）。
- 进程间互斥：`pthread_mutex`（设 `PTHREAD_PROCESS_SHARED`，Linux 上还有 robust 属性处理持有者崩溃），或信号量。
- 平台差异：macOS 不支持未命名的 POSIX 信号量（`sem_init`），Linux 支持。
