%% trellis:begin %%
# 丢包恢复：A/B 线仲裁、重传与快照
*交易所协议：行情与下单*

同一行情在 A、B 两条组播线上各发一遍取先到者（arbitration），缺口（gap）向重传服务器请求，或用快照（snapshot）+ 增量追上。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/protocols.moldudp64|MoldUDP64：给 UDP 行情加上序列号]]

**Unlocks:** [[domains/hft/map/protocols.feed-handler|feed handler 的职责]]

## Readings
- [[nasdaq-moldudp64|MoldUDP64 规范]]

## Drills
- [[protocols-itch-gap-drift|练习：开盘后订单簿悄悄跑偏，找出原因]]

## Cards (4)
1. [[hft-gap-recovery-ab-arbitration]]
2. [[hft-gap-recovery-retransmit]]
3. [[hft-gap-recovery-snapshot]]
4. [[hft-gap-recovery-correlated-loss]]
%% trellis:end %%

## Notes
