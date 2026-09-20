---
id: problems-bounded-blocking-queue-waiting-counts-for-tests
node: problems.components.bounded-blocking-queue
type: qa
step: 8
tags: [grown]
---
## Q
测试一个有界阻塞队列时，怎么确认一个线程真的因为队列满／空而阻塞住了，而不是靠猜一个 `sleep` 的时长？

## A
给队列暴露两个只读计数：`waiting_putters`／`waiting_takers`，分别是当前卡在『非满』／『非空』条件变量上的线程数（在进入 `cond.wait()` 前加一、返回后减一，读取时同样受锁保护）。测试里用一个有界轮询（反复检查计数是否达到期望值，超时只是防止真死锁把测试挂死）等到计数变化，就能确定性地知道『这个线程现在确实阻塞了』，而不必赌一个固定的 `sleep` 时长——`sleep` 太短可能线程还没来得及阻塞就去检查，太长又拖慢测试，而且在负载重的 CI 机器上依然可能不够。这两个计数在生产环境里同样有价值：它们是判断『要不要扩容处理能力』的直接信号。
