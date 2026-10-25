%% trellis:begin %%
# 跨服务一致性：outbox、SAGA 与 TCC
*正确性工程*

本地事务加 outbox 发事件、SAGA 的补偿、TCC 的预留与确认；支付场景里各自适用在哪里。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/payments/map/correctness.state-machines|支付状态机]]

## Cards (8)
1. [[pay-correctness-distributed-transactions-problem]]
2. [[pay-correctness-distributed-transactions-outbox]]
3. [[pay-correctness-distributed-transactions-saga]]
4. [[pay-correctness-distributed-transactions-tcc]]
5. [[pay-correctness-distributed-transactions-choices]]
6. [[pay-correctness-distributed-transactions-best-practice]]
7. [[pay-correctness-distributed-transactions-failure-no-outbox]]
8. [[pay-correctness-distributed-transactions-interview-angle]]
%% trellis:end %%

## Notes
