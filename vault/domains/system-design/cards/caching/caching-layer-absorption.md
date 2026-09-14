---
id: caching-layer-absorption
node: caching.placement
type: qa
---
## Q
Traffic doubles on a page that is 90% identical for all users and 10% personalized. Which cache layers absorb which part, and why can't the CDN take it all?

## A
- **CDN/edge** absorbs the shared 90%: static assets and any response whose cache key is URL-derivable and user-independent.
- The personalized 10% must be served behind auth, so it lands on **application-level caches** (Redis keyed by user/segment) or client-side caching.

CDN caching keyed on `Cookie`/`Authorization` fragments the cache into per-user entries — hit rate collapses to ~0 and you risk serving one user's data to another if the key is wrong. Common pattern: cache the shell at the edge, fetch personalization via a small API call.

## Q zh
页面流量翻倍，90% 对所有用户相同，10% 个性化。哪些缓存层吸收哪部分，为什么 CDN 不能全部吸收？

## A zh
- **CDN/边缘** 吸收共享的 90%：静态资产和任何缓存键是 URL 可导出的且用户独立的响应。
- 个性化的 10% 必须在身份验证后面提供，所以它落在 **应用级缓存**（由用户/群体键入的 Redis）或客户端缓存上。

CDN 缓存由 `Cookie`/`Authorization` 键入会将缓存分割成每个用户的条目 — 命中率崩溃到 ~0，如果键错误，你冒着为一个用户提供另一个用户数据的风险。常见模式：在边缘缓存外壳，通过小型 API 调用获取个性化。
