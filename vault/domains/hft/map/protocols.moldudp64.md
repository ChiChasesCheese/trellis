%% trellis:begin %%
# MoldUDP64：给 UDP 行情加上序列号
*交易所协议：行情与下单*

会话（session）、序列号（sequence number）、消息计数、心跳包；接收方靠序列号发现丢包。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/protocols.itch-model|ITCH 行情模型：逐笔订单（order-by-order）]]

**Unlocks:** [[domains/hft/map/protocols.gap-recovery|丢包恢复：A/B 线仲裁、重传与快照]]

## Readings
- [[nasdaq-moldudp64|MoldUDP64 规范]]

## Drills
- [[protocols-itch-gap-drift|练习：开盘后订单簿悄悄跑偏，找出原因]]

## Cards (4)
1. [[hft-moldudp64-header]]
2. [[hft-moldudp64-gap-detection]]
3. [[hft-moldudp64-heartbeat]]
4. [[hft-moldudp64-packing]]
%% trellis:end %%

## Notes
