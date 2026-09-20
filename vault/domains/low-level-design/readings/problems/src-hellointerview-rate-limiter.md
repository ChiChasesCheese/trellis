---
nodes: [problems.components.rate-limiter]
url: https://www.hellointerview.com/learn/low-level-design/problem-breakdowns/rate-limiter
tags: [no-archive]
---
# Hello Interview — Rate Limiter（Low-Level Design Problem Breakdown）

值得读：商业站点，讲的是面试官视角的评分点与话术——哪一步该主动说出口、哪一步只会被追问，
对"这一关到底在考什么"有参考价值。它的落点偏向生产环境与分布式（Redis 计数器、原子读改写），
和本题"进程内库组件"的定位不同，读时要自行切换语境，否则很容易在机器编码轮里跑题。
它也没有展开本题解最看重的两件事：按 key 的状态如何回收（一百万个 IP 怎么办），
以及多条规则同时生效时"先全查、全过才全扣"的两阶段判定。
