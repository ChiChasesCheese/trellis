---
id: pandas-chunking-map-reduce
node: performance.pandas-at-scale
type: qa
tags: [grown]
---
## Q
处理一个几十 GB、装不进内存的 CSV 时，`pd.read_csv(chunksize=N)` 是怎么让你既能跑聚合又不用把整份数据读进内存的？

## A
`chunksize=N` 让 `read_csv` 返回一个分块读取器（chunk iterator），每次只把 N 行读进内存；典型用法是对每个 chunk 先做一次局部聚合（如按 key 分组求和），再把各 chunk 的局部聚合结果合并成最终结果——这是单机版的 map（每块算局部聚合）-reduce（合并局部结果）模式，内存占用只跟 chunksize 与聚合结果大小有关，与文件总行数无关。
