---
id: hl-cache-contended-sharding
node: foundations.cpu-cache-locality
type: qa
step: 26
---
## Q
除了手工填充，避免伪共享还有哪三种办法？`@Contended` 怎么用、有什么限制？

## A
- **`@jdk.internal.vm.annotation.Contended`**：JDK 内部注解，让 JVM 自动在字段前后加填充（默认 128 字节，同时覆盖 64 和 128）。`LongAdder` 的 `Striped64.Cell`、`ConcurrentHashMap` 的 `CounterCell` 就用它。用户代码要用需加 `--add-exports java.base/jdk.internal.vm.annotation=ALL-UNNAMED` 和 `-XX:-RestrictContended`。
- **按线程分片再合并**：用 `LongAdder` 代替 `AtomicLong` 做高并发计数。
- **设计上避免**：让每个线程写自己的数据结构，只在需要时读别人的，如 SPSC 环形缓冲把 head 和 tail 放在不同缓存行。
