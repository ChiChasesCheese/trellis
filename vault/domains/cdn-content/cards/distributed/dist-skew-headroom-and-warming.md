---
id: dist-skew-headroom-and-warming
node: distributed.skew
type: qa
---
## Q
Why is adding empty cache nodes during a traffic spike not immediate capacity relief?

## A
New nodes initially miss, so rebalancing shifts keys and increases origin load while the fleet is already stressed. Add headroom before peak, move only bounded key ranges, prewarm the hottest immutable objects, and ramp ownership using load-aware routing. Capacity planning must include warm-up bandwidth and miss amplification, not just steady-state memory and CPU.

## Q zh
为什么在 traffic spike 中加入 empty cache node 不能立即缓解 capacity？

## A zh
新 node 起初全是 miss，rebalancing 会移动 key，并在 fleet 已紧张时增加 origin load。应在 peak 前增加 headroom，只移动有界 key range，prewarm 最热 immutable object，并通过 load-aware routing 逐步 ramp ownership。capacity planning 必须包含 warm-up bandwidth 和 miss amplification，而不只是 steady-state memory 与 CPU。
