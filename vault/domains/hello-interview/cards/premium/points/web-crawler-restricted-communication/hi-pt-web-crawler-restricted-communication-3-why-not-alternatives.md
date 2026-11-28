---
id: hi-pt-web-crawler-restricted-communication-3-why-not-alternatives
node: qb.sd.web-crawler-restricted-communication.points
type: qa
step: 3
---
## Q
**无中心网络爬虫 · 为何不用广播与布隆过滤器**｜必会 · 出自：无中心网络爬虫 › 深入 1

无中心爬虫去重时，有三个直觉方案：广播已爬 URL、共享布隆过滤器、按主机名哈希分配。各自为什么不行？

## A
**广播。** 每个节点都要收全部 URL，通信放大 10,000 倍。

**共享布隆过滤器。** 误判会漏爬，而"下载全部"是硬要求，同步量也大。

**按主机名哈希。** 目标站点只有一个主机，所有工作会压到一个节点。

**所以。** 按完整 URL 哈希。
