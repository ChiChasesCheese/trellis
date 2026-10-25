%% trellis:begin %%
# 回调与事件：去重、乱序与重放
*正确性工程*

PSP webhook 的签名校验、至少一次送达下的去重、乱序到达的处理、事件溯源与重放。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/payments/map/correctness.idempotency|幂等与幂等键]]

## Cards (8)
1. [[pay-correctness-webhooks-events-problem]]
2. [[pay-correctness-webhooks-events-signature]]
3. [[pay-correctness-webhooks-events-dedup-inbox]]
4. [[pay-correctness-webhooks-events-ordering-replay]]
5. [[pay-correctness-webhooks-events-design-choices]]
6. [[pay-correctness-webhooks-events-best-practice]]
7. [[pay-correctness-webhooks-events-failure-lost-callback]]
8. [[pay-correctness-webhooks-events-interview-angle]]
%% trellis:end %%

## Notes
