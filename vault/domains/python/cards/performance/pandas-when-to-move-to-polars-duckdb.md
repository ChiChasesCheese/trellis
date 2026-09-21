---
id: pandas-when-to-move-to-polars-duckdb
node: performance.pandas-at-scale
type: qa
tags: [grown]
---
## Q
出现什么信号时，应该考虑把「用 pandas 聚合百万行以上数据」换成 DuckDB 或 Polars，而不是继续在 pandas 里调优？

## A
当数据本身放不进内存（DuckDB 能直接对磁盘上的 Parquet/CSV 做核外查询 out-of-core，不必先整体读进内存）、需要多核并行（Polars 底层是 Rust 实现的多线程执行引擎，而 pandas 单线程执行）、或工作负载主要是可被下推优化的过滤/分组聚合（Polars 支持惰性求值 lazy evaluation 与查询计划优化，DuckDB 本身就是列式 SQL 引擎）时，继续死磕 pandas 通常不如换引擎划算。
