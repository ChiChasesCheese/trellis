---
id: amz-rate-limiter-per-key-isolation-and-memory
node: amazon.amz-rate-limiter
type: qa
step: 5
tags: [grown]
---
## Q
在限流器设计里，怎样让每个用户互不影响，又不让内存随用户数无限增长？并发时锁怎么放？

## A
用 `dict[key → Algorithm]`，key 第一次出现时才用工厂创建状态。内存：状态回到「和新建一样」（令牌满了、窗口里没有请求）就可以丢，定期扫描回收闲置 key；否则一百万个只来过一次的用户永远占内存。并发：「读状态、判定、写状态」必须在同一把锁里，否则两个线程都看到剩 1 个令牌，各放行一次。按 key 哈希分片加锁，不同用户不争同一把锁。
