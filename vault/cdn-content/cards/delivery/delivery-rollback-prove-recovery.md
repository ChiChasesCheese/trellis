---
id: delivery-rollback-prove-recovery
node: delivery.rollback
type: qa
---
## Q
After rollback, error rate falls but remains above baseline. What proves recovery?

## A
Compare the rolled-back cohort with an unaffected control and the pre-change baseline across user SLI, cache state, origin load, and security probes. Confirm the bad version is absent, queues are draining, caches no longer serve its artifacts, and error-budget burn returns below the recovery threshold for a defined window. "Graph went down" is direction, not proof.

## Q zh
rollback 后 error rate 下降，但仍高于 baseline。什么能证明 recovery？

## A zh
把 rolled-back cohort 与 unaffected control 和 pre-change baseline 比较，覆盖 user SLI、cache state、origin load 和 security probe。确认 bad version 已消失、queue 正在 drain、cache 不再提供它的 artifact，并且 error-budget burn 在规定 window 内回到 recovery threshold 以下。“graph 下降了”只说明方向，不是证明。
