---
id: pl-cpp-concurrency-best-practice
node: cpp.concurrency
type: qa
step: 10
---
## Q
资深 C++ 工程师写并发代码遵循哪些规则？什么时候用锁，什么时候用原子操作，什么时候用任务库？

## A
**规则（参照 Core Guidelines 的 CP 章）**：
1. **先减少共享**：优先传值、线程私有数据、不可变对象；共享可变数据是最后手段。
2. **线程用 `std::jthread`**，不要 `detach`；每个线程有明确的所有者和停止方式（`stop_token`）。
3. **锁用 RAII**：`std::scoped_lock`，一次锁多把用它的多参数形式；不手写 `lock()`/`unlock()`。
4. **锁和数据放在同一个类里**；持锁时间尽量短，**不在持锁时调用未知代码**（回调、虚函数、可能阻塞的 I/O）。
5. **条件变量的等待总要带谓词**：`cv.wait(lock, []{ return ready; })`，防虚假唤醒。
6. **原子操作用于简单的标志位和计数器**，默认 `seq_cst`；写 `acquire`/`release` 之前，先用 TSan 和基准测试证明有必要。
7. **不要自己造无锁数据结构**，用经过验证的库（folly、Boost.Lockfree、TBB、`moodycamel`）。
8. **用任务代替线程**：把工作分成任务交给线程池或库（TBB、`std::execution`、各框架），不要到处 `std::thread`。
9. **`std::async` 的返回值必须保存**；它的默认启动策略不保证异步，需要显式指定 `std::launch::async`。

**验证**：
- CI 里一轮 `-fsanitize=thread`，多线程测试要反复运行，因为竞争是概率事件；
- Clang 线程安全注解（`-Wthread-safety` + `GUARDED_BY`）让编译器检查"访问此变量必须持锁"；
- `volatile` 不是同步工具：它不保证原子性或顺序，只是告诉编译器不要优化掉访问，用于内存映射硬件寄存器，不用于线程。

**决策表**：

| 场景 | 选择 |
|---|---|
| 保护一组相关状态 | 互斥锁 |
| 单个计数器、标志位 | `std::atomic` |
| 生产者-消费者 | 队列 + 条件变量，或成熟的并发队列库 |
| 大量 I/O 并发 | 事件循环 + 协程（库） |
| CPU 并行（数据并行） | 并行算法 `std::execution::par` 或 TBB |

**为什么这样**：这些规则的共同点是把并发控制在**很小的、可审查的范围**；越少代码接触共享状态，TSan 能证明的越多。
