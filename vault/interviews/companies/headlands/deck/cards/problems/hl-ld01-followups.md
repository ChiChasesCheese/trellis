---
id: hl-ld01-followups
node: problems.ld01-spsc-channel
type: qa
step: 15
---
## Q
SPSC 通道的追问：多生产者怎么办？跨进程内存序成立吗？消费者崩溃重启怎么办？伪共享怎么证明？

## A
- **为什么 head/tail 自由增长**：下标存取模值时 `head==tail` 空 / 满不可分，补救（空一格 / 另存 size）各有代价；自由增长的计数让空和满是两个不同的差值，不浪费槽位，`long` 溢出要几十万年；
- **为什么容量 2 的幂**：取模变按位与，除法（几十周期）变一周期；代价是容量只能取 2 的幂，空间最多浪费一半；
- **多生产者**：`tail` 要 CAS 竞争（先 CAS 预留，再写，再按序提交——Disruptor `next()/publish()`、Aeron `tryClaim/commit`）；或每个生产者一个 SPSC 环，消费者轮询多个环（无争用但无全局顺序）；
- **跨进程内存序还成立吗**：成立的是硬件缓存一致性 + VarHandle 发出的屏障，不是 JMM 的形式化保证，说法要谨慎；
- **消费者崩溃重启**：head/tail 在文件里，重启 `attach` 接着读；读完才发布 head，处理中崩溃会重读那条——至少一次语义，处理需幂等；要恰好一次需消息带序号并持久化处理进度；
- **伪共享怎么证明**：单变量实验，只改变两个计数器是否在同一缓存行；相邻约慢 2 倍且呈双峰；同时诚实说 SPSC 整体吞吐差异常被噪声淹没；
- **cached index 为什么安全**：head/tail 只增不减，旧快照只低估对方进度，旧值说有空位 / 有数据必然为真，说满 / 空才刷新；
- **null / false 与 drained 怎么区分**：closed 标志，`isDrained = closed && head==tail`，先读 closed 再读 tail；
- **怎么测试跨进程且不挂死**：子进程 + 确定性消息 + 自旋带截止时间 + `waitFor` 超时后 `destroyForcibly`；类路径含被测类实际位置；不靠 sleep。
- 为什么不用 `ArrayBlockingQueue`：锁 + 条件变量，竞争时睡眠 / 唤醒要系统调用、延迟抖动，且跨不了进程。
