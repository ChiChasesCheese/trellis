---
id: foundations-load-parameters
node: foundations.method
type: qa
---
## Q
"Scalable" is meaningless until you describe load. What are load parameters, and how do you pick the right one — e.g. for Twitter's home timeline?

## A
Load parameters are the numbers that describe demand on *your* architecture: QPS per operation, read/write ratio, concurrent connections, cache hit rate, working-set size — and crucially their **distribution**, not just averages.

Pick the parameter the bottleneck actually depends on: Twitter's is not tweet-write QPS (a few k/s) but **followers per user**, because each tweet fans out into ~75 timeline writes and the distribution is extremely skewed (celebrities). Naming the wrong parameter means designing for the wrong problem. See [[foundations-fanout-estimation]].


## Q zh
"可扩展"这个词在你描述清楚负载之前毫无意义。什么是负载参数，你如何挑出正确的那个 — 以 Twitter 的主页推送流为例？

## A zh
负载参数是描述你架构上需求的那些数字：每个操作的 QPS、读写比、并发连接数、缓存命中率、工作集大小 — 关键是它们的**分布**，而不只是均值。

挑选瓶颈真正依赖的那个参数：Twitter 的瓶颈不是推文写入 QPS（每秒几千次而已），而是**每用户的关注者数**，因为每条推文会扇出成约 75 次推送流写入，且这个分布极度倾斜（名人账号）。选错参数就是在为错误的问题设计。参见 [[foundations-fanout-estimation]]。
