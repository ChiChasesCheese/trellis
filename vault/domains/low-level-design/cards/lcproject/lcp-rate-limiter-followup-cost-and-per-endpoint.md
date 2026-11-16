---
id: lcp-rate-limiter-followup-cost-and-per-endpoint
node: lcproject.lcp-rate-limiter
type: qa
step: 10
tags: [作答]
---
## Q
面试官在 LLM 网关限流器上追加：重接口一次请求要消耗 `cost` 个额度，而且不同接口要配不同的限额。它落在设计的哪里？哪些代码一行都不用改？

## A
**评分点**
- 说出 check 增加默认值为 1 的 cost：已有调用点不变
- 说出令牌桶把 tokens >= 1 改成 tokens >= cost，放行扣 cost；窗口里记 (时间, 数量)
- 说出被拒仍不留痕；cost 大于 capacity 或 limit 永远放不行，要在校验时说清
- 说出不同接口的限额由调用方按接口取出参数传入：判定代码已经只依赖参数
- 说出锁、统计、隔离、回收的代码不动

<details class="pt"><summary>参考答案</summary>

`check` 加 `cost: int = 1`；`TokenBucket.decide` 把门槛从 1 改成 `cost`，放行扣 `cost`；窗口队列元素改成 `(时间, 数量)`，计数是数量之和。被拒仍不写。`cost` 大于容量永远放不过，校验时抛 `ValueError`。接口各自的限额由调用方查表后传参。锁、统计、隔离和回收原样不变。

</details>

**知识点：** 限流器（Rate Limiter）、线程安全结构的写法（Thread-Safe Structures）、接口的错误契约（Error Contract）
