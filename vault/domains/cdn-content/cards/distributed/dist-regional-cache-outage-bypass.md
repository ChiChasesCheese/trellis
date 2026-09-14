---
id: dist-regional-cache-outage-bypass
node: distributed.regional-cache
type: qa
---
## Q
A regional cache goes down and every miss immediately bypasses to origin. Why can this recovery policy take down the origin too?

## A
The cache was a capacity layer, so bypass multiplies origin traffic exactly when clients retry and connections churn. Bound origin concurrency, shed low-priority work, serve local stale content where safe, and ramp traffic gradually as the cache warms. Circuit breaking the cache alone is incomplete: the bypass path needs its own tested capacity and stop condition. Monitor origin amplification, not only cache availability.

## Q zh
regional cache 故障后，每个 miss 都立刻 bypass 到 origin。为什么该 recovery policy 也可能打垮 origin？

## A zh
cache 是 capacity layer，bypass 会在 client retry 和 connection churn 最严重时放大 origin traffic。应限制 origin concurrency、shed 低优先级工作、安全时服务 local stale content，并在 cache warm 时逐步 ramp traffic。只对 cache 做 circuit breaking 不完整：bypass path 必须有自己经过测试的 capacity 和 stop condition。监控 origin amplification，而不只是 cache availability。
