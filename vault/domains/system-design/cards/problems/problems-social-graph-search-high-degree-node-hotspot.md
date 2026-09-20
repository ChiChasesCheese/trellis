---
id: problems-social-graph-search-high-degree-node-hotspot
node: problems.social.social-graph-search
type: qa
step: 8
tags: [grown]
---
## Q
In a social graph where the average user has about 300 connections, why does a public figure or organization account with tens of thousands of connections create a hot spot different in kind from ordinary read/write load skew, and what does the design do about it?

## A
That single account's adjacency-list row set is disproportionately large compared to an ordinary user's, meaning reads that page through its connections and any 'mutual friends' query naming it as one of the two users cost far more per-request than the typical case, concentrated on whatever shard hosts that one account. The mitigation is the same class of fix used for celebrity accounts in a follow-based feed design: store and paginate that account's edges specially rather than assuming every user's adjacency list is cheap to read in full.

## Q zh
在一个人均约 300 个连接的社交图里，为什么一个有数万连接的公众人物/机构账号会造成一种和普通读写负载倾斜不同类型的热点？设计上怎么处理？

## A zh
这单个账号的邻接表记录集在物理上远大于普通用户，意味着分页读取它的连接、以及任何把它作为共同好友查询里一方的请求，单次请求的代价都远高于典型情况，而且集中在承载这一个账号的那个分片上。缓解方式和基于关注关系的信息流设计里处理名人账号是同一类思路：对这类账号的边单独存储和分页读取，而不是假设每个用户的邻接表都能廉价地整取。
