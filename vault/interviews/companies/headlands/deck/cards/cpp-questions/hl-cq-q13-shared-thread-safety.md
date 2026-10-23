---
id: hl-cq-q13-shared-thread-safety
node: cpp-questions.c-memory-ownership
type: qa
step: 16
---
## Q
追问：`shared_ptr` 线程安全吗？
Is `shared_ptr` thread-safe?

## A
- **控制块是线程安全的**：不同线程拷贝和销毁指向同一对象的不同 `shared_ptr` 是安全的。
- 但**同一个 `shared_ptr` 对象**被两个线程修改，或者**被指对象本身**被多线程修改，都**不是**线程安全的，仍要加锁。
