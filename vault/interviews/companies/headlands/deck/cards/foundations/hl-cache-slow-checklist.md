---
id: hl-cache-slow-checklist
node: foundations.cpu-cache-locality
type: qa
step: 31
---
## Q
「这段 Java 代码为什么慢」按什么顺序排查？有哪些工具？

## A
按顺序问七件事：
1. **复杂度对吗？** n 是多少？有没有隐藏的 O(n)（`list.contains`、字符串拼接）？
2. **在分配吗？** 热路径里有没有 `new`、装箱、`stream` / lambda 捕获、`String.format`？（`-Xlog:gc`、JFR 分配剖析、`async-profiler -e alloc`）
3. **数据怎么摆的？** 指针追逐多吗？能换成原始类型数组 / SoA 吗？
4. **访问模式？** 顺序、固定步长还是随机？嵌套循环下标顺序对吗？
5. **分支可预测吗？**
6. **多线程共享吗？** 伪共享？锁争用？
7. **测对了吗？** JIT 预热了吗？有没有被死代码消除？

工具：`perf stat`（cache-misses、branch-misses、IPC）、`perf c2c`（专找伪共享）、JFR、async-profiler；macOS 用 Instruments。
