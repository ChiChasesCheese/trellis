%% trellis:begin %%
# ITCH 5.0 关键消息与字段
*交易所协议：行情与下单*

Add Order、Order Executed、Order Cancel、Order Delete、Order Replace、Trade、System Event；stock locate、纳秒时间戳、4 位小数价格。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/protocols.itch-model|ITCH 行情模型：逐笔订单（order-by-order）]], [[domains/hft/map/protocols.binary-encoding|二进制定长编码、字节序与定点价格]]

**Unlocks:** [[domains/hft/map/protocols.feed-handler|feed handler 的职责]], [[domains/hft/map/orderbook.building|从逐笔行情重建订单簿]]

## Readings
- [[nasdaq-itch-5|Nasdaq TotalView-ITCH 5.0 规范]]

## Cards (4)
1. [[hft-itch-messages-overview]]
2. [[hft-itch-messages-add-order]]
3. [[hft-itch-messages-lifecycle]]
4. [[hft-itch-messages-locate-timestamp]]
%% trellis:end %%

## Notes
