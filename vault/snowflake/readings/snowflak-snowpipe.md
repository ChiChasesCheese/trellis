---
nodes:
- ingestion.snowpipe-auto-ingest
title: Snowpipe:事件驱动的自动微批加载
corpus: snowflake-docs
section: 19-data-load-snowpipe-intro
url: https://docs.snowflake.com/en/user-guide/data-load-snowpipe-intro
tags:
- canonical
---

# Snowpipe:事件驱动的自动微批加载

Snowpipe 让文件一到达 stage 就能被加载,不必手动排期跑 COPY:云存储的事件通知(event notification)触发 Snowpipe 轮询队列,按 pipe 对象里定义的 COPY 语句把新文件持续、以 serverless 方式加载进目标表,延迟通常在分钟级。它与批量加载的关键差异在于:使用 Snowflake 托管的计算资源而非用户仓库,按实际使用量计费;每个文件的加载元数据被记录以防止重复加载同一文件;多个内部处理进程并行拉取队列,因此文件到达顺序和加载顺序并不严格一致。读完应理解:Snowpipe 解决的是“文件持续到达、按小批量尽快可见”这一场景,而不是替代批量加载。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-intro)

## Archived copy
![[snowflak-snowpipe-clip]]
%% trellis:end %%
