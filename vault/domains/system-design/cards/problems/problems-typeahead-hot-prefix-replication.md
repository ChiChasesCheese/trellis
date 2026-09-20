---
id: problems-typeahead-hot-prefix-replication
node: problems.search.typeahead
type: qa
step: 7
tags: [grown]
---
## Q
In a typeahead system, what happens when a single short or viral prefix (e.g. a celebrity name suddenly trending) receives a disproportionate share of all suggestion requests, and how should the cache serving it be scaled to handle this?

## A
Because that one prefix's cache entry lives on a single logical location, simply adding more cache nodes doesn't help — every request for that prefix still targets the same entry, the same hot-key problem seen with a viral post's content cache. The fix is to replicate that specific hot prefix's cached entry across several independent read replicas and route requests to one of them by request identity (e.g. a random value) rather than always hitting the same instance, spreading the disproportionate load across replicas instead of concentrating it on one.

## Q zh
在一个 typeahead 系统中，当某一个很短或突然爆红的前缀（比如一个名人的名字突然开始流行）收到不成比例的大量联想请求时会发生什么？该如何扩容承载它的缓存来应对？

## A zh
因为这一个前缀的缓存条目只存在于一个逻辑位置，单纯增加更多缓存节点没有帮助——这个前缀的全部请求依然会打到同一个条目上，这和爆款帖子内容缓存的热 key 问题是同一个模式。修复方法是把这个特定热门前缀的缓存条目复制到几个互相独立的只读副本上，按请求本身的身份（例如一个随机值）而不是永远命中同一个实例来路由请求，把这份不成比例的负载分散到多个副本上，而不是集中在一处。
