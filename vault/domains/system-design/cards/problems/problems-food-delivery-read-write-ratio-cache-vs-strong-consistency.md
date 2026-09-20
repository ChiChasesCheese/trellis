---
id: problems-food-delivery-read-write-ratio-cache-vs-strong-consistency
node: problems.geo.food-delivery
type: qa
step: 1
tags: [grown]
---
## Q
In a food/grocery delivery design, if browsing sessions that check menu or item availability outnumber the orders those sessions eventually produce by about 20 to 1, why should that ratio push the architecture toward two separate paths — a cache-heavy read path for availability display and a narrow, strongly-consistent write path only for the actual inventory decrement at checkout?

## A
A 20:1 read-to-write ratio means the availability-browsing traffic is by far the dominant load, so serving it from a cache with a short TTL (tolerating a few seconds to tens of seconds of staleness) keeps the read-heavy path cheap and fast. The correctness-critical operation — making sure two concurrent orders can't both claim the last unit of a specific item — only has to happen once, at the moment of checkout, on a single inventory row. Applying strong consistency to the whole browsing path as well would drag 20x more traffic through unnecessary coordination overhead, when only the narrow decrement operation actually needs it.

## Q zh
在一个外卖/生鲜配送设计中，如果浏览菜单或库存可用性的会话数量，比这些会话最终转化出的订单数量多出约 20 倍，为什么这个比例应该把架构推向两条分离的路径——一条给可用性展示用的、以缓存为主的读路径，一条只在结账时对真实库存做扣减、窄而强一致的写路径？

## A zh
20:1 的读写比意味着可用性浏览流量是绝对的主导负载，用短 TTL 的缓存来服务它（容忍几秒到几十秒的陈旧）能让这条读多的路径保持轻量和快速。真正关乎正确性的操作——确保两个并发订单不能同时抢到某个商品的最后一件——只需要在结账那一刻、针对单独一行库存发生一次。如果把强一致性也套用到整条浏览路径上，会让 20 倍于此的流量都承受不必要的协调开销，而实际上只有这个窄操作本身需要它。
