---
id: hl-c09-data-race
node: cpp-lessons.c09-ub-sanitizers
type: qa
step: 8
---
## Q
面试问：什么是数据竞争（data race）？和竞态条件（race condition）一样吗？两个线程各 `++counter` 十万次、结果「总是对的」说明没问题吗？
Interview question: What is a data race, and is it the same as a race condition?

## A
- **数据竞争**：两个线程无同步地访问同一内存，且至少一个是写。C++ 定义它为 **UB**。
- **竞态条件**是逻辑上的时序错误，用了原子/锁也可能有，两者不同。
- 打印结果恰好对**不说明没问题**：数据竞争本身就是 UB，只是当前编译器/CPU 碰巧表现正常；ThreadSanitizer 仍会报告 `WARNING: ThreadSanitizer: data race`。
- ASan/UBSan 抓不到它，要用 TSan。
- 修复：`std::atomic<int>`，或 `std::mutex` 保护；否则不共享。
