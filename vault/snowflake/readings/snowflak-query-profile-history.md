---
nodes:
- query.reading-query-profile
- query.spilling-to-remote-disk
- pruning.partition-elimination
- cost.query-history-and-account-usage
title: 查询画像(Query Profile)与查询历史的定位方法
corpus: snowflake-docs
section: 09-ui-query-profile
url: https://docs.snowflake.com/en/user-guide/ui-query-profile
tags:
- canonical
---

# 查询画像(Query Profile)与查询历史的定位方法

查询画像把编译后的执行计划画成算子(operator)节点图,每个节点标注耗时、扫描字节数、裁剪掉的分区占比;“最耗时节点”面板按耗时降序列出所有算子,是定位性能瓶颈的第一站。中间结果放不下内存时会溢出(spill)到本地磁盘,本地磁盘也不够时进一步溢出到远程存储——后者的延迟代价远高于前者,是查询突然变慢的常见元凶。裁剪效率则通过对比“已扫描分区数”与“总分区数”判断,占比越低说明裁剪越有效。查询历史可以在 Snowsight、ACCOUNT_USAGE 视图或 INFORMATION_SCHEMA 三处查看,三者在保留时长和查询延迟上各有取舍。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.snowflake.com/en/user-guide/ui-query-profile)

## Archived copy
![[snowflak-query-profile-history-clip]]
%% trellis:end %%
