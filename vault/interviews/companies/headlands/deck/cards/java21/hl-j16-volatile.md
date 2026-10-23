---
id: hl-j16-volatile
node: java21.j16-concurrency-primitives
type: qa
step: 8
---
## Q
`volatile` 提供哪两个保证，不提供什么保证？`long`/`double` 呢？

## A
```java
static volatile boolean stop;
```
- 保证 1：**可见性**，写入对后续的读可见。
- 保证 2：**有序性**，volatile 写之前的操作不会被重排到它之后；volatile 读之后的操作不会被重排到它之前。
- **不保证原子性**：`volatile int count; count++;` 仍是读-加-写三步，会丢更新。`volatile` 只修饰单次读或单次写。
- `long`/`double`：JLS 保证 volatile 的 64 位读写原子（非 volatile 的 64 位在 32 位 JVM 上理论上可拆成两半）。
