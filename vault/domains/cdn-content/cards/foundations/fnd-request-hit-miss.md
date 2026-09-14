---
id: fnd-request-hit-miss
node: foundations.request-path
type: qa
---
## Q
Two requests have the same URL, but one is a 15 ms edge hit and the other a 600 ms miss. What evidence distinguishes the paths before you blame random network variance?

## A
Inspect a per-hop cache status (`HIT`, `MISS`, `STALE`, `BYPASS`), `Age`, selected cache key/variant, POP and shield identity, origin timing, and bytes transferred. The URL alone is not the execution path: cookies or `Vary`, expiry, purge propagation, or a cold POP can route otherwise identical URLs through different tiers.

## Q zh
两个请求 URL 相同，一个是 15 ms edge hit，另一个是 600 ms miss。在归因于随机网络波动前，应看什么证据来区分路径？

## A zh
检查每个 hop 的 cache status（`HIT`、`MISS`、`STALE`、`BYPASS`）、`Age`、实际 cache key/variant、POP 与 shield 身份、origin timing 和传输字节数。URL 本身不等于执行路径：cookie 或 `Vary`、expiry、purge propagation、cold POP 都可能让相同 URL 经过不同 cache tier。
