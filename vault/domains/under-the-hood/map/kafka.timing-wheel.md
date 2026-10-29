%% trellis:begin %%
# 延迟操作：分层时间轮
*Kafka*

成千上万个超时请求放进环形的时间格，到点整格处理，插入删除 O(1)；时间范围不够就上一层更粗的轮；时钟不逐毫秒空转，而是靠非空格子的 DelayQueue 推进。

**Core** — part of the first pass through this subject.

## Cards (3)
1. [[uth-kafka-timing-wheel-1-hierarchical-wheel]]
2. [[uth-kafka-timing-wheel-2-no-tick]]
3. [[uth-kafka-timing-wheel-3-which-level]]
%% trellis:end %%

## Notes
