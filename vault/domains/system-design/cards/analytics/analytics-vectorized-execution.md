---
id: analytics-vectorized-execution
node: analytics.olap
type: qa
---
## Q
What is vectorized execution, and what cost of the classic row-at-a-time (Volcano) model does it eliminate?

## A
Operators process **batches of a few thousand column values at a time** (a "vector") instead of pulling one row through the whole operator tree per `next()` call.

That kills the Volcano model's overhead: one virtual function call and branch per row per operator, terrible CPU cache behavior. Vectors sized to fit **L1/L2 cache** are processed in tight loops the compiler turns into **SIMD** instructions — one instruction operating on many values.

Result: analytical engines (DuckDB, ClickHouse, Snowflake) are CPU-efficient enough that scans are often bound by decompression bandwidth, not per-row bookkeeping.

## Q zh
什么是矢量化执行，经典行-at-a-time（Volcano）模型的什么代价它消除？

## A zh
operator 一次处理**几千列值的批次**（一个"矢量"）而不是每个`next()`调用通过整个 operator 树拉一行。

那会杀掉 Volcano 模型的开销：每行每个 operator 一个虚函数调用和分支，可怕 CPU 缓存行为。拟合**L1/L2 cache** 的矢量在紧循环中被处理，编译器变成**SIMD** 指令 — 一个指令操作很多值。

结果：分析引擎（DuckDB、ClickHouse、Snowflake）足够 CPU 高效，扫描通常由解压带宽限制，不是 per-row 簿记。
