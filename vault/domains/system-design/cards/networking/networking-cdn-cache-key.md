---
id: networking-cdn-cache-key
node: networking.cdn
type: qa
---
## Q
Your CDN hit rate is mysteriously low for static assets. What cache-key mistakes cause this, and what's the fix?

## A
The cache key is (by default) the full URL plus any `Vary` headers — anything that varies fragments the cache:

- **Irrelevant query params** (tracking params, random ordering) → normalize: strip/sort params in the CDN config.
- **`Vary` on high-cardinality headers** (Cookie, full User-Agent) → drop cookies for static paths, vary only on what changes the response (e.g. `Accept-Encoding`).

Rule: put every byte that changes the response in the key, and **nothing else**.

## Q zh
CDN 的静态资源命中率神秘地很低。哪些缓存键错误导致这种情况，修复方法是什么？

## A zh
缓存键默认为完整 URL 加上任何 `Vary` 头 — 任何变化都会碎片化缓存：

- **无关的查询参数**（跟踪参数、随机排序）→ 规范化：在 CDN 配置中剥离/排序参数。
- **`Vary` 作用于高基数头**（Cookie、完整的 User-Agent）→ 删除静态路径的 cookies，只对改变响应的内容进行 vary（例如 `Accept-Encoding`）。

规则：将每个改变响应的字节放入键中，**除此之外别无其他**。
