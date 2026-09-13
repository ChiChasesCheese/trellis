---
id: content-static-generation-immutable-assets
node: content.static-generation
type: qa
---
## Q
Why should JavaScript and CSS build outputs use content-hashed filenames instead of purging `/app.js` on every release?

## A
Content-addressed names make identity equal bytes: unchanged assets reuse cache across releases, changed bytes get a new URL, and old HTML can still reference its matching old assets. They can safely receive a year-long immutable TTL. Reusing `/app.js` requires globally coordinated invalidation and risks mixed versions while purges propagate. Keep mutable route metadata short-lived; keep artifact URLs immutable.

## Q zh
为什么 JavaScript/CSS build output 应使用 content-hashed filename，而不是每次发布都 purge `/app.js`？

## A zh
content-addressed name 让 identity 等于 bytes：未变化 asset 跨版本复用 cache，变化的 bytes 获得新 URL，旧 HTML 仍能引用匹配的旧 asset。它们可安全设置一年 immutable TTL。复用 `/app.js` 需要全球协调 invalidation，purge 传播期间还会产生 mixed version。mutable route metadata 应短 TTL；artifact URL 应 immutable。
