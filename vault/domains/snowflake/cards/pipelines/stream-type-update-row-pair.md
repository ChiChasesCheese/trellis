---
id: stream-type-update-row-pair
node: pipelines.stream-types
type: qa
source: snowflake-docs
---
## Q
标准流中，源表一行被 UPDATE 后呈现为什么形式？如果一行是在本次偏移量区间内先插入、后更新的，又会如何呈现？

## A
UPDATE 在标准流中表示为一对记录：一条 `METADATA$ACTION = DELETE`（旧值）和一条 `INSERT`（新值），两条的 `METADATA$ISUPDATE` 都为 TRUE。但流记录的是两个偏移量之间的差异：如果行在当前区间内先插入再更新，净变化只是一条新行，表现为一条 INSERT，且 `METADATA$ISUPDATE` 为 FALSE。
