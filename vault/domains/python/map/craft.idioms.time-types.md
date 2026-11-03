%% trellis:begin %%
# 时间类型选型：monotonic / aware datetime / 整数时间戳
*编码功力（Coding Craft） / 高级写法（Idioms）*

持续时间与租约用 monotonic；日历、账单、静默时段用带时区的 datetime；纯逻辑用调用方给的整数时间戳。

**Requires:** [[domains/python/map/engineering.money-time|金额与时间：`Decimal` 舍入模式、整数分、时区感知 `datetime`]], [[domains/python/map/runtime.stdlib-map|标准库地图：`collections`、`heapq`、`bisect`、`datetime`、`pickle`、`logging`]]

## Cards (6)
1. [[craft-time-types-1-monotonic-for-durations]]
2. [[craft-time-types-2-aware-datetime]]
3. [[craft-time-types-3-calendar-vs-duration]]
4. [[craft-time-types-4-timestamp-as-data]]
5. [[craft-time-types-5-across-problems]]
6. [[craft-time-types-6-scales-logical-clock]]
%% trellis:end %%

## Notes
