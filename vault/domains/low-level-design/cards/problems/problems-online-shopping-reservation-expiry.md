---
id: problems-online-shopping-reservation-expiry
node: problems.marketplaces.online-shopping
type: qa
step: 2
tags: [grown]
---
## Q
电商库存的预留（reservation）带一个过期时间。要让这个过期时间不沦为装饰性字段，实现上必须做到哪几件事？

## A
三件。一、过期时间由**注入的时钟**算出，不是进程内的 `time.time()`，否则测试只能靠 `sleep` 验证过期。二、过期要被**执行**而不只是被记录：每次读写库存前扫一遍，把已过期的预留从字典里真正删掉，并把它占用的额度还回可用量；提交（commit）一笔已过期的预留必须直接失败，这才是“预留有时限”被强制的地方。三、预留表是这类设计里唯一会无限增长的容器，删除路径必须数得清——过期扫一次、放弃释放一次、提交删一次，缺一条就是内存泄漏；额度计数归零的行也要一起删掉。
