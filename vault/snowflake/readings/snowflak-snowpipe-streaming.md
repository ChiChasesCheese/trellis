---
nodes:
- ingestion.snowpipe-streaming-offset-tokens
title: Snowpipe Streaming:行级流式写入与精确一次投递
corpus: snowflake-docs
section: 20-data-load-snowpipe-streaming-overview
url: https://docs.snowflake.com/en/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview
tags:
- canonical
---

# Snowpipe Streaming:行级流式写入与精确一次投递

与依赖落地文件的 Snowpipe 不同,Snowpipe Streaming 直接把一行行数据写进表,不经过任何暂存文件,延迟可以低至 5 秒、单表吞吐最高 10GB/s。它靠客户端在每个通道(channel)内自行维护并提交偏移量令牌(offset token)来实现精确一次(exactly-once)语义:应用记录已提交的偏移量,故障恢复后从该位置重放即可,既不丢数据也不重复。同一通道内的行按顺序写入,通道天然对应上游分区(例如 Kafka 分区),因此可确定性地重放。读完应能判断:当数据源是持续产生的单行事件(而非成批文件)时,该考虑走这条路径而不是 Snowpipe。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.snowflake.com/en/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview)

## Archived copy
![[snowflak-snowpipe-streaming-clip]]
%% trellis:end %%
