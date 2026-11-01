---
id: hi-sd-caching-3-patterns
node: qb.sd.news-aggregator-feed.pre-sd-core-concepts-caching
type: qa
step: 3
---
## Q
**四种缓存读写模式**｜系统设计 · 核心概念

缓存的四种读写模式（cache-aside、write-through、write-behind、read-through）分别怎么工作，各有什么代价，为什么面试里默认 cache-aside？

## A
**Cache-aside（旁路缓存，延迟加载）。** 应用先查缓存；命中就返回；未命中则查数据库、写入缓存再返回。只缓存被用到的数据，缓存保持精简，代价是未命中时多一次延迟。面试里只记一个模式，就记它。

**Write-through（写穿）。** 应用只写缓存，缓存同步写数据库后才返回。读到的总是新数据，但写变慢，缓存可能被以后不会读的数据污染；仍有双写问题（缓存成功、库失败会不一致），需要重试或接受不完美。Redis 本身不原生支持，要靠库或框架。

**Write-behind（写回）。** 应用只写缓存，缓存批量异步落库。写入极快，但缓存在刷盘前崩溃就丢数据，适合分析和指标这类容忍少量丢失的场景。

**Read-through（读穿）。** 缓存是智能代理，应用不直接碰数据库，未命中时由缓存自己去取。逻辑集中，但需要专门的库或服务。CDN 就是读穿缓存；应用层面 Redis 用 cache-aside 远比它常见。

**取舍。** 读必须新鲜且能容忍写慢，用 write-through；写吞吐高且接受最终一致，用 write-behind。
