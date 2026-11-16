---
id: lcp-rate-limiter-fractional-tokens
node: lcproject.lcp-rate-limiter
type: qa
step: 7
tags: [作答]
---
## Q
在 LLM 网关限流器的令牌桶策略下（`capacity=3`、`refill_rate=0.5`），桶已被用空，1200 ms 后又来一个请求。它该返回什么？如果每次判定前把令牌数取整，会错在哪？`refill_rate=0` 时被拒该返回什么？

## A
**评分点**
- 说出此刻有 0.6 个令牌，不足 1，被拒且 remaining 为 0
- 说出 reset_after_ms 是 (1-0.6)/0.5 乘 1000 得 800，向 0 截断
- 说出不能取整：被拒时若把 0.6 清成 0，这位客户端永远攒不到 1；0.6 再过 800 ms 必须放行
- 说出放行时 remaining 是剩余令牌的整数部分、reset_after_ms 为 0
- 说出 refill_rate=0 永不恢复，可返回任意非负整数（用 0），并且不能除以 0
- 说出令牌数用 min(capacity, …) 夹住

<details class="pt"><summary>参考答案</summary>

返回 `(False, 0, 800)`：令牌数 0.6，还差 0.4，速率 0.5 个/秒，要 800 ms。令牌数始终保留小数，被拒也不写回，0.6 过 800 ms 补到 1.0 就放行，放行后 `remaining = int(1.0 - 1.0) = 0`。若判定前取整，0.6 变 0，永远攒不够。`refill_rate == 0` 时不做除法，返回 0。

</details>

**知识点：** 限流器（Rate Limiter）、边界校验（Validate at the Boundary）、内存持久化（In-Memory Persistence）
