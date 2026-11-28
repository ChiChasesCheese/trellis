---
id: hi-pt-typeahead-search-system-5-cache-layers
node: qb.sd.typeahead-search-system.points
type: qa
step: 5
---
## Q
**搜索联想 · 四层缓存**｜必会 · 出自：搜索联想 › 深入 2

联想峰值约 8.7 万次/秒，延迟要求很严。缓存放哪几层，各自起什么作用？

## A
**客户端。** 防抖 100–150 ms、取消过期请求、本地缓存（回退删除时直接命中）。
**CDN/边缘。** 短前缀命中率 90% 以上，缓存约 1 分钟。
**进程内 LRU。** 最热的几十万个前缀。
**前缀快照。** 内存点查，1 ms 以内。

长尾前缀不值得放 CDN。
