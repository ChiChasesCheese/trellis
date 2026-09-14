---
id: stream-shared-table-no-extension
node: pipelines.stream-staleness-and-retention-extension
type: qa
source: snowflake-docs
---
## Q
数据消费者在提供方共享（share）过来的表上建了流，指望 Snowflake 自动延长保留期以免流陈旧。这个预期成立吗？

## A
不成立。建在共享表或共享视图上的流不会延长提供方源表（或视图底层表）的数据保留期，因为保留期和相应的存储费用由提供方账户决定。消费者必须在源表原有保留期内按时消费流，否则流会陈旧。
