---
id: cleanroom-problem-it-solves
node: sharing.clean-rooms-privacy
type: qa
tags: [grown]
---
## Q
品牌方和媒体平台想知道“看过广告的用户里有多少人后来购买了商品”，但双方都不愿把各自的用户明细交给对方。普通安全数据共享（Secure Data Sharing）为什么解决不了？数据洁净室（Data Clean Room）怎么解决？

## A
普通共享一旦授予，对方就能对共享的表跑任意 SQL，等于把原始行交了出去。数据洁净室让双方在一个受治理的环境中协作：各自的数据仍留在自己账户里，只有事先由数据所有方批准的查询模板（如按哈希邮箱做交集后的计数聚合）才能在对方数据上运行，输出只是聚合结果，任何一方都看不到对方的原始行。
