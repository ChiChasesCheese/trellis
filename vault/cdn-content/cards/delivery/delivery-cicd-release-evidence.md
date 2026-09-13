---
id: delivery-cicd-release-evidence
node: delivery.cicd
type: qa
---
## Q
What evidence should a CDN cache-policy release attach before production approval?

## A
Attach the exact artifact/config digest; unit, protocol, integration, and production-shaped regression results; load and failure results for HIT, MISS, expiry, and purge; compatibility and rollback proof; expected SLI/cost effects; canary cohorts, guardrails, owner, and runbook. A green generic test job is not evidence that the risky state transitions were exercised.

## Q zh
CDN cache-policy release 在 production approval 前应附带什么 evidence？

## A zh
附上精确 artifact/config digest；unit、protocol、integration 与 production-shaped regression result；针对 HIT、MISS、expiry 和 purge 的 load/failure result；compatibility 与 rollback proof；预期 SLI/cost effect；canary cohort、guardrail、owner 和 runbook。一个绿色 generic test job 不能证明高风险 state transition 已被验证。
