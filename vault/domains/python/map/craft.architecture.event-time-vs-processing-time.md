%% trellis:begin %%
# 事件时间 vs 处理时间：乱序、重复、迟到的事实
*编码功力（Coding Craft） / 架构理解（Architecture）*

用事件发生的时间做所有计算，处理时间永远不进业务逻辑；乱序和重复靠存事实 + 重放吸收。

**Requires:** [[domains/python/map/engineering.money-time|金额与时间：`Decimal` 舍入模式、整数分、时区感知 `datetime`]]

## Cards (5)
1. [[craft-event-time-vs-processing-time-1-replay-by-event-time]]
2. [[craft-event-time-vs-processing-time-2-as-of-pricing]]
3. [[craft-event-time-vs-processing-time-3-reject-or-accept]]
4. [[craft-event-time-vs-processing-time-4-duplicate-vs-conflict]]
5. [[craft-event-time-vs-processing-time-5-watermark]]
%% trellis:end %%

## Notes
