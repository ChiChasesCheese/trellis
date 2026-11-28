---
id: hi-pt-web-crawler-restricted-communication-4-comm-volume
node: qb.sd.web-crawler-restricted-communication.points
type: qa
step: 4
---
## Q
**无中心网络爬虫 · 通信量**｜必会 · 出自：无中心网络爬虫 › 深入 2

无中心爬虫里，每节点要处理 10 万个页面、每页 50 个链接，其中几乎都指向别的节点。通信量有多大，靠什么压下来？

## A
**数字。** 每节点 100,000 × 50 = 500 万次链接出现 × 80 B = 400 MB。(10,000 − 1) ÷ 10,000 = 99.99% 指向别的节点，没有局部性可挖。

**压缩。** 发送端去重（假设重复 5 倍，约 100 万个不同 URL）后只发 80 MB；每批 1,000 条约 80 KB，整个爬取每节点只发约 1,000 个包。只传 URL，页面留在本机。
