---
id: hl-cache-qa-false-sharing
node: foundations.cpu-cache-locality
type: qa
step: 36
---
## Q
追问：什么是伪共享？怎么发现和解决？

## A
推荐答法：「两个线程写的变量在同一缓存行，MESI 让这一行在两个核之间来回失效，性能骤降，但代码里看不出共享。」

- **发现**：`perf c2c` 或 VTune 的 false sharing 分析，或观察加线程反而变慢。
- **解决**：填充或 `@Contended` 隔开热变量，或按线程分片再合并（`LongAdder`）。
- **数字**：我测过，相邻 8 字节的两个原子计数器比相隔一行的慢 **3–13 倍**。
