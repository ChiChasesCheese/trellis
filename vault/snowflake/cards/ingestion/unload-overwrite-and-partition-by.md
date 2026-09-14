---
id: unload-overwrite-and-partition-by
node: ingestion.unload-export
type: qa
tags: [grown]
---
## Q
每天定时把订单导出到同一个 S3 前缀，第二天的文件与前一天的文件混在一起，下游重复读取。有哪些选项可以解决？

## A
1) 用 `PARTITION BY` 表达式（例如按日期拼出路径 `'date=' || TO_VARCHAR(order_date)`）把输出写到按分区组织的子路径，下游按路径增量读取；2) 每次导出到带日期的新前缀；3) 如确实要替换同一路径下的旧结果，使用 `OVERWRITE = TRUE`。按日期分区的输出目录同时也便于外部表（external table）等湖上引擎做分区剪枝。
