---
id: clone-billing-transient-clone-dev
node: continuity.clone-storage-billing
type: qa
tags: [grown]
---
## Q
团队每天从生产永久表（permanent table）克隆一份用于开发测试，并在克隆上频繁改写数据。有哪些降低克隆存储成本的做法？

## A
1) 用完及时 DROP 克隆，避免它长期占住源表已删除的分区；2) 在克隆上把 `DATA_RETENTION_TIME_IN_DAYS` 设为 0，频繁改写产生的历史版本就不会在时间旅行（Time Travel）中长期计费；3) 不需要灾难恢复的开发数据可以放在临时性（transient）数据库或模式中，临时性表没有故障保护（Fail-safe）期，被替换的数据不会再额外保留 7 天。
