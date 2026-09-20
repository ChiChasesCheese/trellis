---
id: problems-instagram-read-write-ratio-forces-cdn
node: problems.social.instagram
type: qa
step: 1
tags: [grown]
---
## Q
In a photo-sharing app design with 150M daily active users uploading media (about 87 QPS average) versus users viewing images while scrolling their feed (about 694,444 QPS average, an ~8,000:1 read-to-write ratio), why does this ratio specifically force nearly all read traffic onto a CDN rather than just onto an application-layer cache?

## A
At roughly 8,000 image views for every one upload, even a well-tuned application-layer cache sitting in front of application servers would still route every one of those ~694,444 QPS through the application tier's network and compute capacity before reaching a cache lookup. A CDN's edge nodes sit geographically and topologically outside the application tier entirely, so at this ratio the only way to keep read traffic from overwhelming application servers and the origin store is to have edge nodes answer the vast majority of requests without ever reaching the application tier.

## Q zh
在一个图片分享应用设计中，1.5 亿日活用户上传媒体（平均约 87 QPS）对比用户刷信息流浏览图片（平均约 694,444 QPS，读写比约 8,000:1），为什么这个比例specifically 会把几乎全部读流量推给 CDN，而不是仅仅推给应用层缓存就够了？

## A zh
在约 8,000 次图片浏览对应 1 次上传的比例下，即便应用服务器前面有调优良好的应用层缓存，约 694,444 QPS 的每一次请求也依然要先经过应用层的网络和计算能力才能走到缓存查找这一步。CDN 的边缘节点在地理和拓扑上完全在应用层之外，在这个比例下，唯一能防止读流量压垮应用服务器和存储源站的方法，就是让边缘节点直接回答绝大多数请求，根本不经过应用层。
