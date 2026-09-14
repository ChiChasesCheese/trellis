---
id: mvcc-high-churn-storage-cost
node: txn.mvcc-immutable-partitions
type: qa
source: snowflake-docs
---
## Q
一张每小时被大量 UPDATE 的企业版（Enterprise Edition）表把保留期设成了 90 天，存储账单明显上涨。机制上的原因是什么？

## A
每次修改都会让 Snowflake 保留修改前的数据版本，直到保留期结束才转入故障保护（Fail-safe）。频繁改写的表会不断产生历史版本，而 90 天保留期意味着这些版本要保存很久，扩展的数据保留需要额外存储，并计入月度存储费用。对高频改写的表，应按真实的恢复需求设置较短的保留期。
