---
id: hi-pt-web-crawler-restricted-communication-8-failure
node: qb.sd.web-crawler-restricted-communication.points
type: qa
step: 8
---
## Q
**无中心网络爬虫 · 宕机与状态复制**｜追问 · 出自：无中心网络爬虫 › 深入 4

无中心爬虫里一个节点宕机了，它负责的 URL 和待爬队列怎么办？"不下载两次"还能保证吗？

## A
**检测与接管。** 节点间 gossip 互探；环上故障节点的槽位由后继接管，未确认的转发重发给新主人。

**状态。** 主人的已见集合和待爬日志异步复制给后继 2 个节点，否则队列里的 URL 永远没人爬。

**语义。** 只有崩溃时正在下载的约 20 个 URL 可能重做；页面按指纹命名覆盖写，结果上仍是每个 URL 一份。
