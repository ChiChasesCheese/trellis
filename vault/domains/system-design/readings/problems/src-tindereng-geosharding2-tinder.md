---
nodes: [problems.social.tinder]
url: https://medium.com/tinder-engineering/geosharded-recommendations-part-2-architecture-3396a8a7efb
---
# Geosharded Recommendations Part 2: Architecture

值得读：系列第二篇讲清楚了地理分片索引的工程实现选择（multi-index 而不是
multi-cluster）和一个容易被忽略的负载不均来源——同一 geoshard 内的用户通常处在相邻
时区，不同 geoshard 在同一时刻的请求峰值可以相差 10 倍以上。比多数题解文章更具体的地方
是给出了他们放弃"手动把互补时区的分片配对到同一台物理机"（NP 难问题）、改用随机分布
副本这一反直觉但更简单有效的解法。
