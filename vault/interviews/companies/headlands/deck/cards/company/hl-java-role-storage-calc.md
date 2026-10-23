---
id: hl-java-role-storage-calc
node: company.java-role
type: qa
step: 5
---
## Q
为什么 tick 数据必须放进分布式存储（distributed storage）？假设每天 200 GB，一年多大？用一块单盘（顺序读约 500 MB/s）读完要多久？

## A
- 每天 200 GB（示例值）× 250 个交易日 = **50 TB / 年**，历史越长越大。
- 单盘顺序读约 500 MB/s：50 TB = 50,000,000 MB，除以 500 MB/s = 100,000 s ≈ **28 小时**。

一块盘装不下，也读不快。所以数据要**切开放在很多台机器上并行读**。岗位要求"with various performance and reliability requirements"：有的数据要快（最近的 tick），有的要稳（不能丢的审计数据），取舍不同，设计也不同。
