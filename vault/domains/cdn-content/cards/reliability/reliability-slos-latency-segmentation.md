---
id: reliability-slos-latency-segmentation
node: reliability.slos
type: qa
---
## Q
Global p99 TTFB is inside target, yet cache misses regularly time out. How should the latency SLI be redesigned before declaring the service healthy?

## A
Define latency over successful eligible requests and segment at least by cache outcome and region: HIT, stale HIT, shield MISS, and origin MISS. Keep a global user-weighted SLO, but expose these diagnostic slices so dominant fast HITs cannot hide a broken miss path. Do not create a separate SLO for every label; that turns diagnosis into an unmanageable contract surface.

## Q zh
global p99 TTFB 达标，但 cache miss 经常 timeout。在宣布服务健康前，应该如何重构 latency SLI？

## A zh
在成功且符合条件的 request 上定义 latency，并至少按 cache outcome 和 region 切分：HIT、stale HIT、shield MISS、origin MISS。保留一个 user-weighted global SLO，同时暴露这些 diagnostic slice，防止大量快速 HIT 掩盖损坏的 miss path。不要为每个 label 单独建立 SLO，否则 diagnosis 会变成无法管理的 contract surface。
