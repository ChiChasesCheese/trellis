---
id: lcp-rate-limiter-state-and-invariant
node: lcproject.lcp-rate-limiter
type: qa
step: 2
tags: [作答]
---
## Q
在 LLM 网关限流器里，每个 (client_id, endpoint) 在两种策略下各要存什么状态？哪条不变量最要紧，哪些写法会破坏它？

## A
**评分点**
- 说出滑动窗口存放行请求的时间戳，用升序 deque：队首清理是 O(1)
- 说出令牌桶存 (小数令牌数, 上次更新时刻)，用到时才按流逝时间补，不起后台线程
- 说出最要紧的不变量：状态只在放行时改变，被拒路径零写入
- 说出时间戳必须升序：读时钟要在锁内，否则先读后拿锁会乱序，队首清理被挡住
- 说出令牌数用 min 夹在 capacity 以内：容量调小时自动收敛，永远不超过容量
- 说出计数器和判定放在同一把锁里：total_allowed 与实际放行数才一致

<details class="pt"><summary>参考答案</summary>

滑动窗口：每个 key 一个升序的时间戳 `deque`，判定时先从队首清掉已满一个窗口的，再比较长度。令牌桶：`(tokens: float, stamp)`，用到时按 `min(capacity, tokens + 流逝秒数 × 速率)` 补。要紧的不变量是"只有放行才写状态"。读时钟必须在锁内，否则时间戳乱序，清理循环被队首挡住。

</details>

**知识点：** 限流器（Rate Limiter）、内存持久化（In-Memory Persistence）、复合操作（Compound Actions）
