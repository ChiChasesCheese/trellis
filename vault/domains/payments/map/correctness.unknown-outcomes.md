%% trellis:begin %%
# 超时与未知结果
*正确性工程*

调用 PSP 超时时钱到底扣了没有：查询补偿、对账兜底、绝不盲目重试扣款；「待处理一小时」怎么处理。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/payments/map/correctness.state-machines|支付状态机]]

**Unlocks:** [[domains/payments/map/reconciliation.why-reconcile|为什么必须对账]], [[domains/payments/map/payouts.failures-returns|打款失败、退票与重试]], [[domains/payments/map/platform.routing-failover|渠道路由与容灾]]

## Cards (7)
1. [[pay-correctness-unknown-outcomes-problem]]
2. [[pay-correctness-unknown-outcomes-resolution-flow]]
3. [[pay-correctness-unknown-outcomes-resolution-choices]]
4. [[pay-correctness-unknown-outcomes-pending-one-hour]]
5. [[pay-correctness-unknown-outcomes-best-practice]]
6. [[pay-correctness-unknown-outcomes-failure-failover-double-charge]]
7. [[pay-correctness-unknown-outcomes-interview-angle]]
%% trellis:end %%

## Notes
