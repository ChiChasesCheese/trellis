%% trellis:begin %%
# ITCH 行情模型：逐笔订单（order-by-order）
*交易所协议：行情与下单*

交易所把每一笔挂单、成交、撤单都作为一条消息发出，接收方自己重建订单簿；这和只发聚合档位的行情有什么不同。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/microstructure.lob|限价订单簿（limit order book）]]

**Unlocks:** [[domains/hft/map/protocols.itch-messages|ITCH 5.0 关键消息与字段]], [[domains/hft/map/protocols.moldudp64|MoldUDP64：给 UDP 行情加上序列号]], [[domains/hft/map/orderbook.requirements|订单簿要支持的操作与复杂度]]

## Readings
- [[nasdaq-itch-5|Nasdaq TotalView-ITCH 5.0 规范]]

## Drills
- [[protocols-itch-gap-drift|练习：开盘后订单簿悄悄跑偏，找出原因]]

## Cards (4)
1. [[hft-itch-model-order-by-order]]
2. [[hft-itch-model-vs-aggregated]]
3. [[hft-itch-model-volume]]
4. [[hft-itch-model-state-drift]]
%% trellis:end %%

## Notes
