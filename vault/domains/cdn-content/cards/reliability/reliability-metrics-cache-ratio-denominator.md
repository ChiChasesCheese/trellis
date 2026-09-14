---
id: reliability-metrics-cache-ratio-denominator
node: reliability.metrics
type: qa
---
## Q
Cache hit ratio improved from 85% to 95%, but origin request volume did not fall. What metric design error might explain this?

## A
The numerator and denominator may include requests that could never reach the origin, such as immutable assets, bypasses, or internal probes. Track counters for eligible requests by outcome and compute both request hit ratio and byte hit ratio over an explicit eligibility set. Also inspect collapsed requests: one origin fetch may serve many misses, so request hit ratio alone does not predict origin load.

## Q zh
cache hit ratio 从 85% 提升到 95%，但 origin request volume 没有下降。什么 metric design error 可能解释这一点？

## A zh
numerator 和 denominator 可能包含永远不会访问 origin 的 request，例如 immutable asset、bypass 或 internal probe。应按 outcome 记录 eligible request counter，并在明确的 eligibility set 上计算 request hit ratio 和 byte hit ratio。还要检查 collapsed request：一次 origin fetch 可能服务多个 miss，因此 request hit ratio 本身不能预测 origin load。
