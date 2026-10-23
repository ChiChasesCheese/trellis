---
id: hl-javaq-d-q17-main
node: java-questions.d-memory
type: qa
step: 24
---
## Q
CPU 缓存怎么影响 Java 性能？为什么 `long[]` 比 `List<Long>` 快？什么是伪共享（false sharing）？
How do CPU caches affect Java performance? Why is `long[]` faster than `List<Long>`? What is false sharing?

## A
一句话：CPU 以 **64 字节缓存行**为单位读内存。顺序访问连续数组命中缓存、预取器能提前加载；追指针（每个 `Long` 一个对象，位置随机）每次都可能 miss（约 100 ns）。**伪共享**：两个线程各写同一缓存行里的不同变量，缓存行在核间来回抢，写变慢。

- 量级：寄存器约 0.3 ns，L1 约 1 ns（32–64 KB），L2 约 4 ns，L3 约 15 ns，内存约 80–100 ns；因机器而异。
- `long[]`：一条 64B 缓存行装 8 个 long，顺序读几乎全命中。
- `Long[]`：ref 指向堆上随机位置的 `Long`（16B），打乱后每次访问约一次 miss。
