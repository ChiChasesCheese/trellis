---
id: bagu-link-web-crawler-restricted-communication-1-map
node: links.web-crawler-restricted-communication
type: qa
step: 1
---
## Q
**无中心协调的分布式网络爬虫（节点间通信受限） · 会被追问哪些八股**｜必会

设计无中心协调的分布式网络爬虫（节点间通信受限）时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 用确定性的所有权代替中心：对 URL 哈希，每个 URL 有唯一主人节点。基础是：一致性哈希、布隆过滤器判重、受限并发、DNS 与连接复用、礼貌限速与重试、gossip。

**下钻路线。**
- 无中心怎么保证不重复 → URL 哈希到唯一主人，一致性哈希使节点增减只迁一小部分，[[b.distributed.consistent-hashing|一致性哈希与虚拟节点]]
- 数十亿 URL 怎么判断已爬 → 布隆过滤器放内存，宁可漏爬也不重爬，[[b.cache.bloom-filter|布隆过滤器原理与误判]]
- 并发下载几万页 → 虚拟线程或 goroutine 便宜，但仍要按域名限并发，[[b.runtime.java-virtual-threads|虚拟线程与现代 Java 特性]]
- 域名解析成瓶颈 → 解析缓存，按域名限速，[[b.net.dns|DNS 解析过程]]
- 每页新建连接的成本 → keep-alive 复用，避免 TIME_WAIT 堆积，[[a.net.time-wait-close-wait|TIME_WAIT 与 CLOSE_WAIT]]
- 失败 URL 重试与礼貌爬取共存 → 对同站点限速，退避后重试，[[a.protect.retry|重试的原则与为什么不能无限重试]]
- 总速率按节点均分 → 每节点令牌桶，节点数变化时重算，[[a.protect.rate-limit-algorithms|限流算法]]
- 节点宕机和成员变化 → gossip 传播成员，了解级，[[b.distributed.consensus|共识算法]]

**业务场景。** 对视频里的外链做批量安全巡检时，要下载大量外站页面，对同一站点必须限速，否则会被封。
**系统设计。** 网络爬虫（Web Crawler）：有中心的版本，URL 队列由中心调度，没有所有权哈希；[[links.global-ip-blocking|全球分布式封禁（黑名单）系统]]：同样靠哈希路由与 gossip 传播，名单是只读的。
