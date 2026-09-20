---
id: problems-live-comments-single-video-hotspot
node: problems.social.live-comments
type: qa
step: 7
tags: [grown]
---
## Q
Why is a viral live video's hot spot in a live-comments system harder to mitigate than a typical hot-key problem elsewhere (like a viral post in a news feed), where spreading load across more shard keys is usually part of the fix?

## A
A live video's comment stream is inherently a single partition keyed by `video_id` — there's no set of alternative keys to spread the load across, because the whole point is that all viewers of that one video need the same broadcast stream. Unlike a viral post's read traffic (which can be replicated across independent cache instances and routed by request), a live video's fan-out cost is concentrated on one logical stream by definition. The mitigations available are instead: capping the absolute load per gateway via sampling/rate-limiting the broadcast (reducing how much gets sent), and co-locating that video's viewers onto a smaller set of gateways to shrink how many gateways the dispatcher must forward to — both reduce the impact of the hot spot rather than spreading it across more keys.

## Q zh
为什么直播评论系统里爆款直播的热点，比其他场景的典型热 key 问题（比如信息流里的爆款帖子，通常可以靠把负载分散到更多分片 key 上来缓解）更难缓解？

## A zh
一场直播的评论流天然就是一个按 `video_id` 分区的单一分区——没有一组可以把负载分散过去的备选 key，因为整个需求的核心就是这场直播的所有观众都要共享同一份广播流。和爆款帖子的读流量（可以复制到多个独立缓存实例、按请求路由）不同，一场直播的扇出成本按定义就集中在一条逻辑流上。可用的缓解手段只能是：通过对广播本身采样/限速来限制每台网关的绝对负载（减少发送量），以及把这场直播的观众协同定位（co-locate）到较少的网关上，缩小 dispatcher 需要转发到的网关数量——两者都是降低热点的影响，而不是把它分散到更多 key 上。
