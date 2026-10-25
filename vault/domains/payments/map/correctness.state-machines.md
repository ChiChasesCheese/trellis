%% trellis:begin %%
# 支付状态机
*正确性工程*

支付单、退款单、打款单的状态与合法转移；只能单调前进；终态；用条件更新防止并发乱序。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/payments/map/correctness.idempotency|幂等与幂等键]]

**Unlocks:** [[domains/payments/map/correctness.unknown-outcomes|超时与未知结果]], [[domains/payments/map/correctness.distributed-transactions|跨服务一致性：outbox、SAGA 与 TCC]], [[domains/payments/map/payouts.payout-flow|打款流程]], [[domains/payments/map/platform.gateway-orchestration|支付网关与编排]]

## Cards (8)
1. [[pay-correctness-state-machines-problem]]
2. [[pay-correctness-state-machines-states-transitions]]
3. [[pay-correctness-state-machines-conditional-update-code]]
4. [[pay-correctness-state-machines-out-of-order]]
5. [[pay-correctness-state-machines-design-choices]]
6. [[pay-correctness-state-machines-best-practice]]
7. [[pay-correctness-state-machines-failure-stale-event]]
8. [[pay-correctness-state-machines-interview-angle]]
%% trellis:end %%

## Notes
