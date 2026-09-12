---
nodes:
- consumer.seek-and-replay
title: 从特定偏移量位置读取记录：seek 与按时间戳定位
corpus: kafka-2e
section: 047-4-8
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 从特定偏移量位置读取记录：seek 与按时间戳定位

消费者默认从上次提交的 offset（偏移量）继续读，但运维和修数据时经常要"回到过去"：重放昨天的事件、跳过一段有毒的积压、或从某个时间点开始重新处理。本节讲 seekToBeginning/seekToEnd、用 offsetsForTimes 把时间戳换成每个分区的 offset，再用 seek() 把读取位置跳过去；要注意 seek 只改变本地读取位置，不会提交，下一次 poll 才生效。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.ituring.com.cn/book/2937)
%% trellis:end %%
