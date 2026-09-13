---
id: cache-failure-stale
node: caching.failure
type: qa
---
## Q
During an origin outage, when is serving stale safer than returning an error, and when is it unsafe?

## A
Serve bounded stale for immutable assets, public pages, or data whose staleness risk is explicitly tolerated; it preserves availability and reduces recovery load. Do not do it for revoked authorization, security policy, rapidly changing prices/inventory, or legal takedowns without a product-approved contract. Expose stale age/reason so success metrics do not hide degraded correctness.

## Q zh
origin outage 时，什么时候 serve stale 比返回 error 更安全？什么时候不安全？

## A zh
immutable asset、public page，或业务明确容忍 staleness 的数据可 bounded serve stale；它能保 availability，并降低 recovery load。对已撤销 authorization、security policy、快速变化的 price/inventory、legal takedown，若没有产品批准的 contract，就不能这样做。必须暴露 stale age/reason，避免 success metric 掩盖 correctness degradation。
