%% trellis:begin %%
# 生效时间版本表：按事件发生时刻取规则（effective-dated lookup）
*编码功力（Coding Craft） / 跨题模式（Patterns）*

规则/价格/政策按生效时间排成升序版本；用事件时间二分取版本，而不是当前配置，历史交易可精确重算。

**Requires:** [[domains/python/map/runtime.stdlib-map|标准库地图：`collections`、`heapq`、`bisect`、`datetime`、`pickle`、`logging`]], [[domains/python/map/engineering.money-time|金额与时间：`Decimal` 舍入模式、整数分、时区感知 `datetime`]]

## Cards (5)
1. [[craft-effective-dated-versions-1-price-by-event-time]]
2. [[craft-effective-dated-versions-2-bisect-right-edge]]
3. [[craft-effective-dated-versions-3-append-only-or-backfill]]
4. [[craft-effective-dated-versions-4-snapshot-of-parallel-lists]]
5. [[craft-effective-dated-versions-5-across-problems-and-scales]]
%% trellis:end %%

## Notes
