---
id: reliability-incidents-postmortem-action
node: reliability.incidents
type: qa
---
## Q
A postmortem concludes "the reviewer missed an unsafe `Vary` change." What makes this conclusion weak, and what follow-ups are stronger?

## A
It stops at a person and does not explain why the system allowed an unsafe change to reach users. Trace contributing conditions such as absent cache-key invariants, weak production-shaped tests, missing canary isolation probes, and unclear rollback ownership. Create owned, prioritized actions with verifiable completion: a conformance test, rollout guardrail, dashboard, and practiced runbook—not "be more careful."

## Q zh
postmortem 的结论是“reviewer 漏掉了 unsafe `Vary` change”。为什么这个结论很弱，什么 follow-up 更强？

## A zh
它停留在个人层面，没有解释为什么 system 允许 unsafe change 到达用户。应追踪 contributing condition，例如缺少 cache-key invariant、production-shaped test 太弱、缺少 canary isolation probe，以及 rollback ownership 不清。创建有 owner、有 priority 且可验证完成的 action：conformance test、rollout guardrail、dashboard 和演练过的 runbook，而不是“以后更小心”。
