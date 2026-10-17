---
id: amz-dns-resolver-what-and-three-questions
node: amazon.amz-dns-resolver
type: qa
step: 1
tags: [grown]
---
## Q
DNS 解析器（DNS Resolver）要你设计什么？开场先问哪三个澄清问题？

## A
解析器把域名翻译成 IP：先查本地缓存，没有再问上游，并缓存结果。三问：(1) 上游是真实 DNS 还是要自己递归查询——决定把上游抽象成接口；(2) 缓存多久——每条记录自带 TTL（生存时间，Time To Live），不能写死；(3) 上游挂了怎么办——决定要健康检查、切换备用上游，或返回已过期的旧数据。
