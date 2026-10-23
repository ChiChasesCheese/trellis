---
id: hft-java-memory-model-happens-before
node: java.memory-model
type: qa
step: 1
---
## Q
Java 内存模型（JMM）里的 happens-before 是什么？为什么需要它？

## A
线程 A 写了一个变量，线程 B 不一定马上、甚至永远看不到，因为 CPU 有私有缓存和写缓冲（store buffer），JIT 也会重排指令、把变量缓存在寄存器里。

JMM 因此规定：若操作 X **happens-before** 操作 Y，则 X 的结果对 Y 可见，且 X 不会被重排到 Y 之后。主要规则：同一线程内按程序顺序；同一把锁的 `unlock` 先于之后的 `lock`；同一个 `volatile` 变量的写先于之后的读；`Thread.start()`、`join()`；以及传递性。没有这条先后链的“写—读”是**数据竞争**（data race），结果几乎没有保证。

例：普通 `boolean stop` 字段，读线程里的 `while (!stop)` 被 JIT 提到寄存器只读一次，永远停不下来；加 `-Xint` 又恢复正常，行为取决于 JIT 是否编译了这段代码。
