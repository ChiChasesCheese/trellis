---
id: hft-machine-memory-ordering-x86-tso-vs-arm
node: machine.memory-ordering
type: qa
step: 2
---
## Q
x86 的内存模型 TSO 和 ARM 的内存模型相比有什么不同？为什么"在 x86 上跑得好好的"并发代码，换到 ARM 上可能出错？

## A
**x86 TSO**（Total Store Order，总存储序）很强：硬件只允许一种重排，就是"**写之后的读**可以先于这次写生效"（因为写先进了存储缓冲区）。其余三种（读读、读写、写写）都保持程序顺序。

经典例子：线程 1 做 `x = 1; r1 = y;`，线程 2 做 `y = 1; r2 = x;`，初始 x、y 都是 0。在 x86 上 `r1 == 0 && r2 == 0` 可能出现，因为两个读都先于对方的写生效。

**ARM** 更弱：读读、读写、写写也都可能被重排，需要程序明确插入屏障或使用 acquire/release。

后果：缺了屏障的代码，在 x86 上因为硬件替你保证了顺序，永远不出问题；换到 ARM 服务器或苹果芯片，才暴露出 bug。所以并发代码要按语言的内存模型（Java 的 happens-before、C++ 的 `memory_order`）写正确，而不是靠"在我的 x86 机器上测过"。
