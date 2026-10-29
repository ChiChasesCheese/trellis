---
id: uth-compose-k8s-workqueue-4-real
node: compose.k8s-workqueue
type: qa
step: 4
---
## Q
**真实实现多做了什么**｜Kubernetes · client-go v0.37

真实的 workqueue 在这三个结构之外还加了什么？用户最容易踩什么坑？

## A
**细节。**

- 并发：一把互斥锁配一个条件变量（`sync.Cond`）；`Get` 遇到空队列就睡眠，`Add`、`Done` 有新活时唤醒一个 worker
- 关闭：`ShutDown` 之后新的 `Add` 被忽略；`ShutDownWithDrain` 还会等 `processing` 清空
- 延迟：`AddAfter` 外包一层，用按到期时间排序的最小堆加一张"key → 堆节点"的表；同一个 key 重复延迟，只保留更早的时间
- 限速：`AddRateLimited` 按失败次数指数退避（从 5 毫秒起翻倍，上限 1000 秒），并与每秒 10 个、桶容量 100 的令牌桶取较大者
- 底层队列是可替换的接口，重复 `Add` 会调用它的 `Touch`，可以换成带优先级的队列

**为什么。** 去重放在队列里，所有控制器都免费得到"同一个 key 不会并行处理"；业务代码只管"读最新状态、修正差异"。

**坑。** 取出后忘了 `Done`：key 永远留在 `processing`，之后的 `Add` 只记 `dirty`、不再入队，这个对象再也不会被处理。成功后还要 `Forget`，否则限速器一直记着失败次数。队列里放对象指针而不是 key，同一对象的两个副本互不相等，去重就失效。

**对应 LeetCode：** 无直接对应的题
