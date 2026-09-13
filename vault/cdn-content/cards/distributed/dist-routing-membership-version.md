---
id: dist-routing-membership-version
node: distributed.routing
type: qa
---
## Q
During a rolling membership update, clients use different hash rings and cache hit ratio collapses. What control-plane property is missing?

## A
Routing membership needs an explicit version and coordinated rollout. Publish an immutable member set, let clients load and acknowledge it, and support a bounded overlap where reads may try the prior owner while writes follow one policy. Measure version skew and key movement before promotion. An eventually updated node list without version semantics causes duplicate fills, inconsistent ownership, and hard-to-debug churn.

## Q zh
rolling membership update 期间，client 使用不同 hash ring，cache hit ratio 崩溃。control plane 缺少什么 property？

## A zh
routing membership 需要显式 version 和协调 rollout。发布 immutable member set，让 client load 并 acknowledge；在有界 overlap 期间，read 可尝试 prior owner，而 write 遵循单一 policy。promotion 前测量 version skew 与 key movement。没有 version semantics 的 eventually updated node list 会导致 duplicate fill、inconsistent ownership 与难调试的 churn。
