---
id: hi-c-sd-caching-n15-read-through
node: sd.core-concepts.caching.notes
type: qa
step: 15
---
## Q
**缓存 · 缓存模式 · Read-Through**｜摘要 · 追问
Read-through 和 cache-aside 区别在哪？面试里什么时候才提它？

## A
- **做法：** 缓存充当智能代理，应用从不直接访问数据库。未命中时由缓存自己去数据库取、存下、返回。它是 write-through 在读上的对应，两者常合用。
- **优点：** 缓存逻辑集中；代价是复杂，通常要专门的缓存库或服务。
- **面试位置：** 应用层用 Redis 时 cache-aside 远比它常见。它的典型例子是 CDN：未命中就向源站取回并缓存。除非谈 CDN 之类基础设施，很少有理由主动提。
