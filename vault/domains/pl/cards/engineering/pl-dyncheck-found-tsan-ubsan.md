---
id: pl-dyncheck-found-tsan-ubsan
node: engineering.dynamic-checkers
type: qa
step: 3
---
## Q
ThreadSanitizer（TSan）怎样判断两次访问构成数据竞争？UndefinedBehaviorSanitizer（UBSan）检查什么？Go 的 `-race` 与它们是什么关系？

## A
**TSan** 的核心问题是：「这两次访问之间有没有 happens-before 关系」，即其中一次是否保证在另一次之前完成（由锁、原子操作、线程创建与等待这类同步建立）。做法：
1. 每个线程维护一个**向量时钟**（vector clock），同步操作（加锁、解锁、原子读写）按规则更新和合并时钟；
2. 每个内存位置的影子状态记录最近几次访问：哪个线程、什么时刻、读还是写；
3. 新的访问到来时，拿它的线程时钟和影子里的记录比较。如果发现一次写与另一次读写**之间没有 happens-before**，就报告数据竞争。

因此 TSan 不需要两个线程真的「同时」访问才发现，只要没有同步关系就能抓到。官方给出的开销量级：运行慢约 5 到 15 倍，内存多 5 到 10 倍。Go 的 `-race` 就是基于 TSan 运行时的实现，内存与时间代价同一量级。

**UBSan** 不是影子内存，而是在编译时把可能触发未定义行为的操作换成「带检查」的版本，开销很小：有符号整数溢出、移位越界、空指针解引用、类型不匹配的转换等。例（C）：

```c
int x = INT_MAX - 1 + argc;   /* argc == 1 -> INT_MAX */
int y = x + 1;                /* signed overflow: undefined behaviour */
```

无检查时程序打印 `-2147483648`，看起来「能跑」，编译器却有权假定它不发生并据此优化。用 `-fsanitize=undefined`：

```text
u.c:5:15: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
```

在 Rust 里，整数溢出在调试构建中会 panic，发布构建中回绕，是有明确定义的行为，所以 UBSan 的价值在 `unsafe` 和 C 依赖里。
