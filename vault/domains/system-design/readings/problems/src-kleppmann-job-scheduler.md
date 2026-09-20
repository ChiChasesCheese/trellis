---
nodes: [problems.foundations.job-scheduler]
url: https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html
tags: []
---
# How to do distributed locking (Martin Kleppmann)

值得读：fencing token 机制的权威技术分析——为什么单靠租约/锁服务本身无法阻止一个
暂停后恢复的客户端带着过期的所有权认知继续写入，必须由被写入的资源本身校验单调
递增的 token。本题解「深入探讨」第 3 节的租约与 fencing 设计直接采用这篇文章的
论证；这不是关于某个具体调度器产品的披露，是本题解在通用分布式锁语境之外，把这个
机制具体应用到"任务执行互斥"这个场景的延伸。
