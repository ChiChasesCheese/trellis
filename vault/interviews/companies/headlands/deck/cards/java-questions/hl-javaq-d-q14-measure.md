---
id: hl-javaq-d-q14-measure
node: java-questions.d-memory
type: qa
step: 15
---
## Q
2000 万次 `Long boxed += i` 和原始 `long` 求和相比，分配和耗时差多少？这个数字该怎么口述？

## A
- 实测第 1 轮：`long` 求和约 10 ms、分配 **0 字节**；`Long` 求和约 17 ms、分配约 **239,999,832 字节**（约 240 MB）。
- 平均每次约 12 字节而不是一个 `Long` 的 16 字节：JIT 展开循环后消除了一部分中间装箱，其余仍落在堆上。
- 面试时只说"JIT 可能消除一部分"，不要承诺具体消除量。
- 数字只看量级，不是严格基准。
