---
id: networking-push-vs-pull-cdn
node: networking.cdn
type: qa
---
## Q
Push CDN vs pull CDN — how does each get content to the edge, and which fits (a) a video release dropping globally at midnight, (b) a long-tail image catalog?

## A
- **Pull** (the default): edge fetches from origin on first miss, then caches. Zero upload workflow; cost is a slow first request per edge and origin load on misses.
- **Push**: you upload content to the CDN ahead of time.

(a) **Push/pre-warm** — a synchronized global spike would stampede the origin on cold caches.
(b) **Pull** — pre-pushing millions of rarely-viewed files wastes edge storage; let demand decide what's cached.

## Q zh
推送 CDN vs 拉取 CDN — 每种如何将内容获取到边缘，哪种适合 (a) 视频发布在午夜全球下降，(b) 长尾图像目录？

## A zh
- **拉取**（默认值）：边缘在第一次未命中时从源站获取，然后缓存。零上传工作流；成本是每个边缘的第一个缓慢请求和未命中时的源站负载。
- **推送**：你提前上传内容到 CDN。

(a) **推送/预热** — 同步全球峰值会在冷缓存上踩踏源站。
(b) **拉取** — 预推送数百万很少被查看的文件浪费边缘存储；让需求决定缓存什么。
