---
nodes: [problems.social.instagram]
url: https://algomaster.io/learn/system-design-interviews/design-instagram
tags: [no-archive]
---
# Design Instagram

值得读：给出了另一组容量估算假设（5 亿日活、每天 1 亿次上传、每天 280TB 存储、50 亿次
每日信息流读取）以及推/拉混合 fan-out 的处理框架，是网上免费可读、覆盖面较完整的
Instagram 系统设计走查之一。与本题解不同的地方在于：它把关注关系 fan-out 和媒体处理
平铺在同一篇里各自浅讲，本题解把 fan-out 完全交给 [[solution-news-feed]] 去深挖，自己
把容量估算和「深入探讨」的篇幅都投入到媒体上传、转码、存储和 CDN 这几个 Instagram 真正
独有的环节，覆盖得更深；两篇文章的容量估算数字也不同，因为各自假设的日活规模不同，不
构成对同一事实的分歧。
