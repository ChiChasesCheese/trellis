---
id: hi-x-caching-invalidation-3-choose
node: sd.cross.caching-invalidation
type: qa
step: 3
---
## Q
**缓存、失效与一致性窗口**｜跨题模式 · 怎么选

面对一个新的「读多写少」设计题，怎样决定缓存放什么、失效靠什么、一致性放在哪里？列出信号，每个分支给一个例子。

## A
| 信号 | 选择 | 例子 |
|---|---|---|
| 值几乎不变，读写比极端悬殊 | 长 TTL 加多层缓存，问题只剩命中率与容量 | [[url-shortener-design\|短链接服务（URL Shortener / TinyURL）]] |
| 值会改，要把不一致控制在可说明的范围 | 先更库再删缓存，CDC 兜底，TTL 加抖动，热点用本地缓存 | [[tt-cache-consistency-hot-keys\|缓存一致性与热点 Key]] |
| 缓存值来自按次计费的外部调用 | TTL 按价格变化速度分档，合并并发请求，高成本的确认推迟到用户真正选中时 | [[flight-search-system\|设计机票搜索系统（多供应商聚合，按调用计费）]] |
| 读侧是搜索索引、缓存这类派生视图 | 事件驱动更新，带版本条件写入，保底 TTL | [[merchant-product-listings\|商家商品上架与更新系统]] |
| 读几乎都能旧，但下单不能错 | 搜索用预聚合摘要，一致性只放在写路径和下单时的核验 | [[hotel-booking-system\|酒店预订系统（Expedia 型聚合与自营）]] |
| 所有读者共享同一份内容 | 共享的页面缓存加 CDN，不做每用户一份 | [[news-aggregator-feed\|设计新闻聚合系统（Google News）]] |
| 价格、库存、权限必须准 | 关键路径绕过缓存读主库，缓存只用于展示 | [[tt-cache-consistency-hot-keys\|缓存一致性与热点 Key]] |

缓存内容的粒度也要选：只存 ID，内容另取，换来删除和编辑只改一处（[[twitter-clone-feed\|微博客与个性化信息流（Twitter）]]）。
