%% trellis:begin %%
# feed handler 的职责
*交易所协议：行情与下单*

收包、仲裁、检测缺口、解码、归一化（normalize）成内部格式、维护订单簿、发布给策略——每一步的延迟和正确性要求。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/protocols.gap-recovery|丢包恢复：A/B 线仲裁、重传与快照]], [[domains/hft/map/protocols.itch-messages|ITCH 5.0 关键消息与字段]]

**Unlocks:** [[domains/hft/map/architecture.pipeline|交易系统的组件流水线]], [[domains/hft/map/research-infra.tick-capture|行情抓取与存储规模]]

## Drills
- [[protocols-itch-gap-drift|练习：开盘后订单簿悄悄跑偏，找出原因]]

## Cards (4)
1. [[hft-feed-handler-pipeline]]
2. [[hft-feed-handler-normalization]]
3. [[hft-feed-handler-backlog]]
4. [[hft-feed-handler-correctness]]
%% trellis:end %%

## Notes
