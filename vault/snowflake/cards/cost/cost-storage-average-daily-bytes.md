---
id: cost-storage-average-daily-bytes
node: cost.credit-model-per-second-billing
type: qa
source: snowflake-docs
---
## Q
某账户月初存了 10 TB，月中一次加载后变成 30 TB。Snowflake 的月存储费是按月末的 30 TB 算吗？存储量是按压缩前还是压缩后计？

## A
都不是按月末快照算。存储费按每天账户中平均落盘字节数计算出月平均值，再乘以每 TB 的月费率，所以这个月大约按两者的时间加权平均计费。计量的是落盘（on-disk）字节，即压缩后的大小，例如原始 325 TB 的数据压缩后约 65 TB，就按 65 TB 计费。费率因账户类型（Capacity 或 On Demand）和区域而不同。
