---
id: hi-pt-web-crawler-restricted-communication-6-ramp-up
node: qb.sd.web-crawler-restricted-communication.points
type: qa
step: 6
---
## Q
**无中心网络爬虫 · 启动扩散**｜必会 · 出自：无中心网络爬虫 › 深入 3

无中心爬虫启动时只有种子 URL 的主人有活可干，其余 9,999 台机器闲着。多久能让所有机器都有活？

## A
**数字。** 每页 50 个链接：第 1 层最多 50 个节点有活，第 2 层 50² = 2,500，第 3 层 50³ = 125,000 > 10,000。

**结论。** 约三层（几秒）全员有活，因为链接按哈希分散到不同主人，启动扩散很快。
