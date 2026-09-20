---
id: problems-video-streaming-cdn-build-vs-buy
node: problems.media.video-streaming
type: qa
step: 6
tags: [grown]
---
## Q
In a video streaming platform, why would a design use a self-operated edge appliance network (Netflix-Open-Connect style, deployed inside ISP facilities) for the head of the content catalog while still relying on a third-party commercial CDN for long-tail content, instead of picking one strategy for all traffic?

## A
A self-operated edge network trades a fixed hardware and power cost for near-zero marginal bandwidth cost, which only pays off when traffic is large and predictable enough to justify the investment — this fits the head of the catalog (e.g. the top 1% of videos that account for the majority of views), which is stable and forecastable. Long-tail content is unpredictable, low-volume per title, and constantly changing as new content is uploaded, so it is cheaper to serve through a pay-per-gigabyte third-party CDN that offers elastic reach without fixed infrastructure commitment. Picking only one strategy either overpays for elastic capacity on predictable head traffic, or overpays fixed hardware costs to cover unpredictable long-tail demand.

## Q zh
在一个视频流媒体平台中，为什么设计会对内容库头部（类 Netflix Open Connect，部署在 ISP 机房内的自建边缘设备网络）用自建边缘网络，而对长尾内容仍然依赖第三方商业 CDN，而不是对所有流量统一选一种策略？

## A zh
自建边缘网络用固定的硬件和电力成本换取接近零的边际带宽成本，只有当流量足够大且足够可预测、值得为它投入这笔固定成本时才划算——这正好匹配内容库头部（例如贡献大部分播放量的头部 1% 视频），这部分流量稳定且可预测。长尾内容不可预测、单个标题播放量低、且随新内容上传不断变化，用按流量计费的第三方 CDN 提供弹性覆盖，比为它承诺固定基础设施更便宜。只选一种策略要么在可预测的头部流量上为弹性能力多付钱，要么为覆盖不可预测的长尾需求多背固定硬件成本。
