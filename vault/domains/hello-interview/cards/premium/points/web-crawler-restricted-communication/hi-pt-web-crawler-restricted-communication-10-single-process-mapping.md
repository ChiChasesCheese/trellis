---
id: hi-pt-web-crawler-restricted-communication-10-single-process-mapping
node: qb.sd.web-crawler-restricted-communication.points
type: qa
step: 10
---
## Q
**无中心网络爬虫 · 单机爬虫的对应**｜追问 · 出自：无中心网络爬虫 › 取舍与追问

单机爬虫是"广度优先队列加访问集合"。变成无中心分布式后，访问集合的"检查并插入"、队列、布隆过滤器各自对应什么？

## A
**检查并插入。** 单进程靠一把锁或单线程；分布式变成单一写者，谁拥有这个键，谁串行处理。

**队列。** 变成每节点自己的待爬队列加批量转发。

**布隆过滤器。** 单机放不下内存才用；这里每节点只有 800 KB，精确集合更好，URL 多 1,000 倍时才值得换。
