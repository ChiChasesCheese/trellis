---
id: hft-machine-memory-ordering-why-reorder
node: machine.memory-ordering
type: qa
step: 1
---
## Q
为什么编译器和 CPU 会改变内存读写的先后顺序？多线程程序因此会遇到什么问题？

## A
重排是为了更快，而且对**单个线程**看起来没有区别：
- 编译器可能把两条互不相关的读写换个顺序，或把值留在寄存器里。
- CPU 在写内存时，不是等数据真正写到缓存才继续，而是先把写入放进一个叫**存储缓冲区**（store buffer）的小队列里就接着执行后面的指令。后面的读取可能比前面的写入"先生效"。

问题出在多线程：线程 A 先写 `data = 42`，再写 `ready = true`；线程 B 看到 `ready == true` 后读 `data`。如果 A 的这两个写入被重排，或者 B 看到它们的顺序不同，B 可能读到旧的 `data`。

这类 bug 极难复现，通常几百万次才出一次。解决办法是**内存屏障**（memory barrier / fence，禁止某类重排的指令）或带同步语义的原子操作，如 Java 的 `volatile`、C++ 的 `std::atomic`。它们限制重排，但要付性能代价。
