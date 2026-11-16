---
id: lcp-rate-limiter-boundary-and-truncation
node: lcproject.lcp-rate-limiter
type: qa
step: 6
tags: [作答]
---
## Q
在 LLM 网关限流器里，滑动窗口 `window_ms=10000`、`limit=2`，第一次请求在 t0，第三次在 t0+3500 ms 被拒，合同要求 `reset_after_ms` 向 0 截断，期望值是 6500。若用 `time.monotonic()` 的浮点秒来算，会得到什么？怎么处理？恰好满一个窗口的旧请求算不算数？

## A
**评分点**
- 说出浮点会出错：t0=0.7 s 时 (0.7+10.0)-(0.7+3.5) 乘 1000 得 6499.999999999999，截断成 6499
- 说出修法：内部用整数纳秒（monotonic_ns），最后一步整数除法得毫秒
- 说出向 0 截断就是非负整数的 //，不做四舍五入，结果类型是 int
- 说出恰好满 window_ms 的请求不再计数：清理条件是 now - ts >= window
- 说出用注入的假时钟精确断言 6500 和 int 类型
- 说出时钟倒退按没有流逝处理，令牌桶用 max(0, elapsed)

<details class="pt"><summary>参考答案</summary>

浮点秒相减会留下 `1e-12` 的尾巴，`int()` 截断把它放大成 1 ms：`(0.7+10.0)-(0.7+3.5)` 乘 1000 是 6499.999999999999。做法是内部全程整数纳秒，`reset = (stamps[0] + window - now) // 1_000_000`。窗口左闭右开：`now - ts >= window` 时旧请求已退出，所以第 100 ms 时恰好满 100 ms 的请求不再算数。

</details>

**知识点：** 限流器（Rate Limiter）、边界校验（Validate at the Boundary）、为测试而设计
