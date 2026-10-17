---
id: amz-dns-resolver-objects-and-jobs
node: amazon.amz-dns-resolver
type: qa
step: 2
tags: [grown]
---
## Q
在 DNS 解析器设计里应该有哪几个对象？各自只负责一件什么事？

## A
`Record`：域名、IP 列表、TTL。`TTLCache`：存记录并判断过期。`Upstream` 接口：`resolve(name)`，每个上游自带健康状态。`Resolver`：门面，缓存没有就按顺序问健康的上游，成功后写缓存。切分依据：「存多久」「问谁」「怎么串起来」各自变化，测试时上游可以换成假的。
