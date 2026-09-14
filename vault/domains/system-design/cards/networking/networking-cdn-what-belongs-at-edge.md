---
id: networking-cdn-what-belongs-at-edge
node: networking.cdn
type: qa
---
## Q
Beyond static files, what can a modern CDN edge absorb — and what technique protects the origin even for cache misses?

## A
- **Cacheable dynamic responses**: API GETs with short TTLs (even 1–5 s absorbs a viral spike), personalized pages split so the shared shell caches.
- **Terminating work**: TLS, compression, WAF/bot filtering, edge functions for redirects/auth checks.

Miss protection: **origin shield / tiered caching** — all edge misses funnel through one mid-tier cache plus **request coalescing**, so a global miss becomes one origin fetch instead of hundreds.

## Q zh
超越静态文件，现代 CDN 边缘还能吸收什么 — 什么技术即使对于缓存未命中也能保护源站？

## A zh
- **可缓存的动态响应**：带短 TTL 的 API GET（甚至 1-5 s 可以吸收病毒式峰值），个性化页面分解使共享 shell 可以缓存。
- **工作终止**：TLS、压缩、WAF/bot 过滤、用于重定向/身份验证检查的边缘函数。

未命中保护：**源站屏蔽/分层缓存** — 所有边缘未命中通过一个中层缓存加**请求合并**，使全局未命中成为一个源站获取而不是数百个。
