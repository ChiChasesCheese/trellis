---
id: hi-pt-web-crawler-restricted-communication-9-termination
node: qb.sd.web-crawler-restricted-communication.points
type: qa
step: 9
---
## Q
**无中心网络爬虫 · 终止检测**｜追问 · 出自：无中心网络爬虫 › 深入 5

没有主控节点时，怎样判断整个爬取已经完成？只看"所有节点都空闲"为什么不行？

## A
**做法。** 每个节点记 Forward 消息的发送和接收计数及是否空闲，沿 gossip 求和；全体空闲且全局发送数等于接收数，连续两轮不变才判完成。

**为什么不能只看空闲。** 在途消息会让别人重新有活，空闲只是瞬时状态。
