---
nodes:
- continuity.zero-copy-clone
title: 克隆(CLONE)的元数据本质与常见陷阱
corpus: snowflake-docs
section: 15-object-clone
url: https://docs.snowflake.com/en/user-guide/object-clone
tags:
- canonical
---

# 克隆(CLONE)的元数据本质与常见陷阱

CREATE ... CLONE 只复制指向已有微分区的元数据指针,不搬动任何字节,因此对超大表也能瞬间完成——这就是零拷贝克隆(zero-copy clone)。但克隆并非事务性快照:若克隆过程中源对象上发生了改名、重建等 DDL,或数据保留期(retention)恰好为 0 导致所需历史版本已被清除,克隆会因命名冲突或数据不可用而失败。聚簇键、搜索优化访问路径等会被克隆但状态各异——聚簇键默认在克隆表上被挂起,需要手动恢复;外部表、内部临时 stage 等则完全不参与克隆。读完应记住:克隆快是因为不搬数据,但“不搬数据”本身也带来了一整套需要注意的边界情况。
