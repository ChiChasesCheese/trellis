---
id: hi-ov-key-technologies-2-options
node: sd.in-a-hurry.key-technologies
type: qa
step: 2
tags: [通览]
---
## Q
**关键技术 · 要点一览**｜通览

关键技术这一章的要点有哪些？

## A
**11 项要点。**
- **关系型：** join、索引、事务；产品题默认，选 Postgres。
- **NoSQL：** 模型多变、横向扩展；四种数据模型，DynamoDB。
- **对象存储：** 大文件放这里，库里只存 URL；预签名 URL 直传，S3。
- **搜索型：** 倒排索引做全文搜索，不用 LIKE；Elasticsearch。
- **API 网关：** 路由、认证、限流；画在客户端第一站。
- **负载均衡器：** 当黑盒，只画一个；长连接用 L4，其余 L7。
- **队列：** 缓冲突发、解耦；同步低延迟路径不加，防反压。
- **流：** 数据保留可重放；实时处理、事件溯源，Kafka。
- **分布式锁：** 长时间占用，如占座；Redis 带过期，防死锁。
- **分布式缓存：** 说清淘汰、失效、写策略；Redis。
- **CDN：** 不只静态资源；Cloudflare、CloudFront。
