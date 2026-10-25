%% trellis:begin %%
# 幂等与幂等键
*正确性工程*

客户端生成幂等键、服务端「同键同结果」的存储与过期、并发同键请求、跨服务传递；和数据库唯一约束的关系。

**Core** — part of the first pass through this subject.

**Unlocks:** [[domains/payments/map/correctness.state-machines|支付状态机]], [[domains/payments/map/correctness.webhooks-events|回调与事件：去重、乱序与重放]]

## Cards (9)
1. [[pay-correctness-idempotency-problem]]
2. [[pay-correctness-idempotency-key-contract]]
3. [[pay-correctness-idempotency-store-code]]
4. [[pay-correctness-idempotency-concurrent-same-key]]
5. [[pay-correctness-idempotency-cross-service]]
6. [[pay-correctness-idempotency-design-choices]]
7. [[pay-correctness-idempotency-best-practice]]
8. [[pay-correctness-idempotency-failure-new-key-on-retry]]
9. [[pay-correctness-idempotency-interview-angle]]
%% trellis:end %%

## Notes
