---
id: hl-javaq-e-q24-log
node: java-questions.e-jit-gc
type: qa
step: 25
---
## Q
`-Xlog:safepoint` 的一行日志包含哪些时间段？一次 G1 young GC 的量级是多少？

## A
例：`Safepoint "G1CollectForAllocation", Time since last: 22903042 ns, Reaching safepoint: 97125 ns, Cleanup: 8166 ns, At safepoint: 1463917 ns, Leaving safepoint: 3875 ns, Total: 1573083 ns`。
- `Reaching safepoint`：到达时间，约 **0.1 ms**。
- `At safepoint`：真正做事，约 **1.5 ms**。
- 总暂停约 **1.6 ms**。
- 同一次运行的后续几行，`At safepoint` 涨到 2.9–3.1 ms，因为活跃数据在增长。
- ZGC 也有 safepoint，但极短，只做根扫描等小操作。
