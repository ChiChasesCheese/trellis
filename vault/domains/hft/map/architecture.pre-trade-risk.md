%% trellis:begin %%
# 内联的下单前风控
*tick-to-trade 系统架构*

价格合理性（fat finger）、单笔数量、持仓上限、下单速率、自成交防范；这些检查必须在几十纳秒内完成。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/architecture.pipeline|交易系统的组件流水线]], [[domains/hft/map/market-structure.rules|约束 HFT 的监管规则]]

**Unlocks:** [[domains/hft/map/reliability.kill-switch|kill switch 与 drop copy]]

## Drills
- [[architecture-risk-inline-explain|练习：向新同事解释，为什么下单前风控放在热路径里]]

## Cards (5)
1. [[hft-architecture-pre-trade-risk-checks]]
2. [[hft-architecture-pre-trade-risk-fat-finger-example]]
3. [[hft-architecture-pre-trade-risk-o1-incremental]]
4. [[hft-architecture-pre-trade-risk-worst-case-position]]
5. [[hft-architecture-pre-trade-risk-three-layers]]
%% trellis:end %%

## Notes
