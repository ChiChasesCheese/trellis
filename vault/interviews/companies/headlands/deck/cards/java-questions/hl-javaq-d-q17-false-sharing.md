---
id: hl-javaq-d-q17-false-sharing
node: java-questions.d-memory
type: qa
step: 26
---
## Q
伪共享（false sharing）是怎么发生的？怎么修？用什么工具找？JDK 里谁用了这个技巧？

## A
- **发生**：一条 64B 缓存行里放着线程 1 写的 `counterA` 和线程 2 写的 `counterB`；线程 1 写 A，整行变"已修改"并使其他核的副本失效；线程 2 写 B 又要重新取整行，两个核互相抢。
- **修复**：在变量之间**填充**（padding）到 64 字节以上，或把计数拆成多个槽（striping）。
- **JDK 内部**：`@jdk.internal.vm.annotation.Contended`（应用代码默认不可用，需 `-XX:-RestrictContended`）；`LongAdder` 的 `Cell` 就用了它。
- **工具**：Linux 的 `perf c2c`。
