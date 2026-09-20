---
id: problems-instagram-origin-shield-request-coalescing
node: problems.social.instagram
type: qa
step: 5
tags: [grown]
---
## Q
In a photo-sharing system's CDN design, when a newly published photo from a high-follower account causes many geographically nearby edge nodes to receive their first request for that object at nearly the same time, why does a pure pull CDN (no extra layer) create a spike at the origin, and what does an origin shield fix?

## A
In a pure pull CDN, each edge node independently treats its first request for an object as a cache miss and fetches it from the origin, so if dozens of nearby edge nodes each get a near-simultaneous first request for the same freshly-published object, they each independently issue an origin fetch, multiplying origin load by the number of edges rather than serving them from one fetch. An origin shield is a regional layer between edge nodes and the true origin that coalesces concurrent requests for the same object into a single origin fetch, with the other requests waiting on and reusing that one result instead of each triggering their own origin round trip.

## Q zh
在一个图片分享系统的 CDN 设计中，当某个高粉丝账号新发布的照片导致多个地理相邻的边缘节点几乎同时收到对该对象的第一次请求时，为什么纯拉取型（pull）CDN（没有额外保护层）会在源站产生流量尖峰？源站保护层（origin shield）如何解决这个问题？

## A zh
在纯拉取型 CDN 中，每个边缘节点会独立把自己收到的第一次请求当作缓存未命中，各自去源站回源；如果几十个相邻的边缘节点几乎同时收到对同一个刚发布对象的第一次请求，它们就会各自独立发起一次回源，源站压力被放大到边缘节点数量的倍数，而不是只被服务一次。源站保护层是边缘节点和真正源站之间的一个区域性中间层，它把针对同一个对象的并发请求合并成一次真正的回源请求，其余请求等待并复用这一次结果，而不是各自触发自己的回源往返。
