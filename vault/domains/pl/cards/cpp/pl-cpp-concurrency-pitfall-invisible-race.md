---
id: pl-cpp-concurrency-pitfall-invisible-race
node: cpp.concurrency
type: qa
step: 11
---
## Q
并发 bug 为什么难发现？一个"测试从不失败"的数据竞争是什么样的，怎样才能抓到？

## A
**事实**：数据竞争的后果依赖线程的交错、CPU 的内存模型、编译器的优化，**可能在测试里一次都不出现，上线后偶发**。

**本机实测**。把 release/acquire 配对故意改成 `relaxed`：

```cpp
// 生产者
data = 42; ready.store(true, std::memory_order_relaxed);
// 消费者
while (!ready.load(std::memory_order_relaxed)) {} if (data != 42) ++bad;
```

这在 C++ 标准里是数据竞争（消费者读 `data` 没有与生产者的写建立"先于"关系），是未定义行为。在 Apple Silicon 上跑 2 万轮，`bad` 一直是 0：**测试没有发现任何问题**。但用 `-fsanitize=thread` 编译同一份代码，立刻报告：

```
WARNING: ThreadSanitizer: data race
SUMMARY: ThreadSanitizer: data race i7.cpp:12 in main::$_1::operator()() const
```

**为什么测试看不出**：
1. 硬件不一定会重排（x86 的模型很强，ARM 在这类小例子上也很少重排）；
2. 编译器这次没有重排；
3. 换更新的编译器、更激进的优化，或换一台机器，才暴露。

**其他典型的"隐形"并发 bug**：
1. **检查后行动**（check-then-act）：`if (map.count(k) == 0) map[k] = v;`，两步之间被别的线程插入；
2. **伪共享**：不是 bug，但性能莫名下降；
3. **死锁**：多把锁的获取顺序不一致，只在特定负载下出现；
4. **`std::async` 的 future 被丢弃**：任务悄悄变成串行；
5. **悬垂引用**：线程 lambda 按引用捕获局部变量，线程比局部变量活得久。

**怎样抓到**：
- **TSan 是主力**：以"发生了同步缺失"而不是"出了错"为判据，所以即使这一轮没出错，也会报告潜在竞争；代价是慢 5 到 15 倍，用在测试构建；
- **压力测试**：多线程反复运行、降低优先级、加入随机延迟（`std::this_thread::yield()`）放大交错；
- **代码审查看"共享可变状态"**：每个被多线程访问的变量，问"谁保护它"；
- **形式化工具**：对无锁算法，用模型检查器（如 CDSChecker、Relacy）穷举交错。

**要记住的一点**：并发的正确性不能靠"测过没出事"证明；TSan 通过，才算有证据。
