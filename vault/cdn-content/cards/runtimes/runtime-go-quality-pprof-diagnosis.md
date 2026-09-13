---
id: runtime-go-quality-pprof-diagnosis
node: runtimes.go-quality
type: qa
---
## Q
p99 rises while CPU stays moderate and goroutine count climbs. Which Go profiles would you inspect, and what distinct question does each answer?

## A
Start with the goroutine profile to find leaked or blocked stacks, then block and mutex profiles to identify channel/lock waiting and contention. Use a CPU profile for where runnable time is spent and a heap profile for retained memory or allocation pressure. Capture a short, bounded sample from a representative instance and correlate it with request metrics; a profile is evidence about sampled runtime state, not proof of causality by itself.

## Q zh
p99 上升、CPU 仍中等，但 goroutine 数持续增长。应检查哪些 Go profile，各自回答什么不同问题？

## A zh
先看 goroutine profile，定位 leaked 或 blocked stack；再看 block 和 mutex profile，找 channel/lock waiting 与 contention。CPU profile 说明 runnable time 花在哪里，heap profile 说明 retained memory 或 allocation pressure。应从有代表性的实例采集短而有界的样本，并与 request metrics 关联；profile 只是 sampled runtime state 的证据，本身不是 causality 证明。
