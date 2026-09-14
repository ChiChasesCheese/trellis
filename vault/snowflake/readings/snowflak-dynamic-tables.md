---
nodes:
- pipelines.dynamictable-target-lag
- pipelines.dynamictable-incremental-vs-full-refresh
- pipelines.dynamictable-adaptive-refresh
title: 动态表(Dynamic Table):用目标延迟声明代替手写 Stream+Task
corpus: snowflake-docs
section: 23-dynamic-tables-about
url: https://docs.snowflake.com/en/user-guide/dynamic-tables-about
tags:
- canonical
---

# 动态表(Dynamic Table):用目标延迟声明代替手写 Stream+Task

动态表只需声明一条 SELECT 查询和一个目标延迟(target lag,例如 10 分钟),Snowflake 自动追踪依赖的基表、推导刷新节奏,并按依赖图顺序刷新一整条动态表流水线——不必再手写 Stream 捕获变更、Task 调度、MERGE 合并这一整套逻辑。刷新模式上,INCREMENTAL 只重算发生变化的那部分行,FULL 则整体重算,AUTO 让 Snowflake 在创建时自行判断;ADAPTIVE 默认走增量刷新,但一旦检测到上游变更量大到增量反而比全量重算更慢,会自动切换成全量重新初始化。每次刷新都是原子生效,读者永远看不到刷新过程中的中间状态。读完应能判断什么场景该用动态表替代手写的 Stream+Task 组合。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.snowflake.com/en/user-guide/dynamic-tables-about)

## Archived copy
![[snowflak-dynamic-tables-clip]]
%% trellis:end %%
