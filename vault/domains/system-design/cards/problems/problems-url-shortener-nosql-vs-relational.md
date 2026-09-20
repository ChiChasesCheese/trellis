---
id: problems-url-shortener-nosql-vs-relational
node: problems.foundations.url-shortener
type: qa
step: 2
tags: [grown]
---
## Q
In a URL shortener design, why choose a NoSQL key-value / wide-column store for the short_code → long_url mapping instead of a relational database, given that the whole dataset is well under 1TB and would easily fit on a single Postgres instance?

## A
Because the deciding factor is access pattern, not data volume: every read and write is a pure primary-key lookup (short_code → long_url) with no joins and no multi-row transactions. NoSQL key-value/wide-column stores natively support horizontal partitioning and multi-region active-active writes without extra coordination middleware, which matters because the redirect path carries a 99.99%-availability target; a relational database could handle this data volume, but achieving the same multi-region write availability with it needs significantly more operational machinery.

## Q zh
在一个短链接（URL shortener）设计中，即便全部数据远小于 1TB、单台 Postgres 就能装下，为什么 short_code → long_url 映射还是选择 NoSQL 键值 / 宽列族（wide-column）存储而不是关系型数据库？

## A zh
因为决定性因素是访问模式而不是数据量：每次读写都是纯粹的主键查找（short_code → long_url），没有 join，也没有跨行事务。NoSQL 键值 / 宽列族存储原生支持水平分区和多区域主动写（active-active），不需要额外的协调中间件——这一点很重要，因为重定向路径承担着 99.99% 的可用性目标；关系型数据库能扛住这个数据量，但要达到同等的多区域写可用性需要多得多的运维机制。
