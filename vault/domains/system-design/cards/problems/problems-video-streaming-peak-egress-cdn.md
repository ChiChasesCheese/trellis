---
id: problems-video-streaming-peak-egress-cdn
node: problems.media.video-streaming
type: qa
step: 2
tags: [grown]
---
## Q
In a video streaming platform with 12.5 million peak concurrent viewers each streaming at an average blended bitrate of 3 Mbps, why does the resulting ~37.5 Tbps peak egress bandwidth rule out serving playback traffic directly from an origin data center?

## A
12.5 million concurrent viewers times 3 Mbps each is about 37.5 Tbps of simultaneous outbound traffic, a figure far larger than any single data center's practical network egress capacity, regardless of how much compute or storage it has. This forces the playback path to be served almost entirely from geographically distributed CDN edge caches, with the origin (object storage) only absorbing cache misses — origin capacity only needs to cover a fraction (e.g. the ~30% of requests not served from cached popular content) rather than the full peak.

## Q zh
在一个视频流媒体平台中，峰值有 1,250 万并发观众，每路平均混合码率约 3 Mbps，为什么由此得出的约 37.5 Tbps 峰值出口带宽会排除直接从源站数据中心提供播放流量这个选项？

## A zh
1,250 万并发观众乘以每路 3 Mbps，约为 37.5 Tbps 的同时出口流量，这个数字远超任何单一数据中心实际能承受的网络出口能力，无论它有多少计算或存储资源。这迫使播放路径几乎完全由地理上分布的 CDN 边缘缓存节点提供服务，源站（对象存储）只需要吸收缓存未命中的那部分——源站容量只需覆盖一小部分请求（例如热门内容缓存命中之外约 30% 的请求），而不是应对全部峰值。
