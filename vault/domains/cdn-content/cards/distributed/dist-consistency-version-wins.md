---
id: dist-consistency-version-wins
node: distributed.consistency
type: qa
---
## Q
Why is wall-clock “last write wins” dangerous for global invalidation state?

## A
Clock skew can make an older update appear newer, and concurrent updates lose causal intent. Prefer a monotonic generation from an authoritative sequencer, or a logical/version-vector scheme when concurrent writers are required. Make updates idempotent and compare versions explicitly. Wall time is useful metadata for observability and expiry, but should not silently decide correctness across unsynchronized regions.

## Q zh
为什么用 wall-clock “last write wins” 处理 global invalidation state 很危险？

## A zh
clock skew 会让旧更新看似更新，concurrent update 也会丢失 causal intent。最好使用 authoritative sequencer 产生的 monotonic generation；若必须支持 concurrent writer，则用 logical/version-vector scheme。update 应 idempotent，并显式比较 version。wall time 可用于 observability 与 expiry，但不应在未同步 region 间静默决定正确性。
