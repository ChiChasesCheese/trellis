---
id: cache-freshness-no-cache
node: caching.freshness
type: qa
---
## Q
Why does `Cache-Control: no-cache` not mean "do not store," and when is it preferable to `no-store`?

## A
`no-cache` allows storage but requires successful validation before reuse; `no-store` forbids storage. Use `no-cache` when a representation may be retained and cheaply validated so `304` can save bytes. Use `no-store` for sensitive data that must not persist. Confusing them discards useful browser/CDN behavior or leaks data.

## Q zh
为什么 `Cache-Control: no-cache` 不等于“不要存储”？什么时候它比 `no-store` 更合适？

## A zh
`no-cache` 允许存储，但每次复用前必须成功 validation；`no-store` 禁止存储。当 representation 可以保留且能低成本 validation、用 `304` 节省 bytes 时使用 `no-cache`。敏感数据不能持久化时才用 `no-store`。混淆二者会丢掉有价值的 browser/CDN 行为，或造成数据泄露。
