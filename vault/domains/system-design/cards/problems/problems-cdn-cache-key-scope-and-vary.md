---
id: problems-cdn-cache-key-scope-and-vary
node: problems.foundations.cdn
type: qa
step: 3
tags: [grown]
---
## Q
In a CDN's control-plane API, a `CacheRule` entity carries a `cache_key_vary` list alongside `ttl`. Why does putting the `Cookie` header in that list collapse a page's cache hit rate toward zero, even if the page's HTML body is identical for every visitor?

## A
The cache key is what the CDN uses to decide whether two requests are 'the same object' - by default the URL, plus anything named in `cache_key_vary`. Adding `Cookie` to that list means every distinct cookie value (which is different per visitor, since cookies typically carry a session or user id) produces a distinct cache key, even when the underlying response body would have been byte-identical. In effect the cache is fragmented into roughly one entry per visitor, so almost every request is a first-time miss for its unique key - hit rate collapses toward zero. The fix is to vary the key only on headers that actually change the response body, and serve identical-body content behind auth through a mechanism other than a cookie-keyed cache entry.

## Q zh
在 CDN 的控制面 API 中，`CacheRule` 实体除了 `ttl` 还带有一个 `cache_key_vary` 列表。为什么把 `Cookie` 头加进这个列表，会把一个页面的缓存命中率拉到接近零——即使这个页面的 HTML 内容对每个访客都一模一样？

## A zh
缓存键决定 CDN 如何判断两个请求是否算「同一个对象」——默认是 URL，加上 `cache_key_vary` 中列出的任何字段。把 `Cookie` 加进这个列表意味着每个不同的 cookie 值（通常每个访客都不同，因为 cookie 通常携带 session 或用户 id）都会产生一个不同的缓存键，即使底层响应体本来逐字节相同。实际效果是缓存被拆成大约每个访客一条条目，几乎每个请求都对其独一无二的键算首次未命中——命中率拉到接近零。修复方法是只对真正改变响应体的头做 vary，对需要鉴权但内容相同的请求，用除 cookie 键入缓存条目之外的机制处理。
