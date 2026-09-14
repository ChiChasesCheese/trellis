---
id: networking-cdn-purge-vs-versioning
node: networking.cdn
type: qa
---
## Q
Shipping a new asset build behind a CDN: purge/invalidate vs versioned URLs — compare, and what's the standard practice?

## A
- **Purge**: propagates across PoPs in seconds–minutes (eventual), is a per-URL operational step, and does nothing for copies already in *browser* caches.
- **Versioned (fingerprinted) URLs**: content hash in the name (`app.3f2a1c.js`) makes each asset immutable → `max-age=1yr, immutable`; "invalidation" is just deploying HTML that references new names — instant and atomic.

Standard: fingerprint everything referenced; keep the HTML entry point short-TTL/no-store as the mutable pointer. Purge is for emergencies (leaked or wrong content), not deploys.

## Q zh
在 CDN 后部署新资源构建：清除/失效 vs 版本化 URL — 比较，标准做法是什么？

## A zh
- **清除**：在数秒到数分钟内跨 PoP 传播（最终一致），是每个 URL 的运维步骤，对已经在*浏览器*缓存中的副本无影响。
- **版本化（指纹生成）URL**：内容哈希在名称中（`app.3f2a1c.js`）使每个资源不可变 → `max-age=1yr, immutable`；"失效"就是部署引用新名称的 HTML — 即时且原子性。

标准做法：对所有引用的内容进行指纹生成；将 HTML 入口点保持为短 TTL/no-store 作为可变指针。清除仅用于紧急情况（泄露或错误的内容），而不是用于部署。
