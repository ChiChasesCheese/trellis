---
id: cache-invalidation-purge-scope
node: caching.invalidation
type: qa
---
## Q
Choose between purge-by-URL, prefix, tag, and purge-all for a product-page update. What is the decision rule?

## A
Use the narrowest key set that completely covers affected representations. URL is precise but must include every variant; prefix fits a route subtree; tags express logical dependencies such as product 42 across HTML/images; purge-all is an expensive emergency tool that creates a cold-cache surge. Record purge scope, propagation status, and origin protection.

## Q zh
product page 更新时，如何在 purge-by-URL、prefix、tag、purge-all 之间选择？

## A zh
选择能够完整覆盖受影响 representation 的最窄 key set。URL 最精确，但必须包含每个 variant；prefix 适合 route subtree；tag 可表达 product 42 跨 HTML/image 的逻辑依赖；purge-all 是昂贵的 emergency tool，会制造 cold-cache surge。应记录 purge scope、propagation status 与 origin protection。
