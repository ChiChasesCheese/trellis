---
id: hi-pt-flight-search-system-5-cache-ttl
node: qb.sd.flight-search-system.points
type: qa
step: 5
---
## Q
**机票搜索系统 · 缓存键与分层 TTL**｜必会 · 出自：机票搜索系统 › 深入 1

报价缓存的键和值怎么设计？TTL 取多久？怎么发现 TTL 偏长？

## A
**键值。** 键是规范化搜索键；值按供应商分开存，新增或下线供应商不让整条缓存失效。
**TTL。** 3 天内起飞约 5 分钟；一到四周约 30 分钟；更远 2～6 小时；更好是按航线实际价格变化率自适应。
**监控。** 点击确认时的价差率，价差太大说明 TTL 偏长。
