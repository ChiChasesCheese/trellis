---
id: hi-c-lld-intro-x06-gil-safe
node: lld.concurrency.intro.exam
type: qa
step: 6
---
## Q
**并发入门 · GIL 让我的类线程安全吗**｜考点 · 追问

面试官问："Python 有 GIL，我的 `Inventory` 类还需要锁吗？"怎么答？

## A
- **需要：** GIL 保证同一时刻只有一个线程执行字节码，不保证"检查库存再扣减"这类多步操作不被切开
- **字节码层面：** `x += 1` 是读取、相加、存储多条指令，线程可在中间切换
- **某些单个操作原子（如 `list.append`）：** 是 CPython 实现细节，不要依赖
- **答法：** 给复合操作加锁，并说明无 GIL 的 Python 构建和其他语言里这点更重要
