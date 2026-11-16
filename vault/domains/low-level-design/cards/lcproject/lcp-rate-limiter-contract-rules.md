---
id: lcp-rate-limiter-contract-rules
node: lcproject.lcp-rate-limiter
type: qa
step: 1
tags: [作答]
---
## Q
在 LLM 网关限流器里，网关每个请求前调用 `check(client_id, endpoint, limit, window_ms, capacity, refill_rate)`，得到 `(allowed, remaining, reset_after_ms)`。配置在滑动窗口和令牌桶两种策略里选一种，多个线程同时调用，另有一个 `stats()`。开工前你会先定下哪几条规则？

## A
**评分点**
- 说出 remaining 在本次判定之后算、被拒时恒为 0：响应头给客户端看的是此刻还能立刻发几次，不含以后才补回的额度
- 说出被拒的请求不扣额度、不进放行历史：否则客户端越勤重试，被锁得越久
- 说出毫秒数向 0 截断且是 int：四舍五入会差 1 ms，类型错了测试直接失败
- 说出状态按 (client_id, endpoint) 隔离：换接口或换客户端都是一份全新额度
- 说出令牌数保留小数、判定前不取整：0.6 个令牌攒到 1.0 时必须放行
- 说出时间由限流器自己读、check 没有时间参数：所以要注入时钟才能测边界

<details class="pt"><summary>参考答案</summary>

先把合同写成六条：返回 `(allowed, remaining, reset_after_ms)`，第三项是 `int`；`remaining` 在决策之后算，被拒为 0，只数此刻已有的额度；被拒的请求什么都不写；毫秒向 0 截断；按 (客户端, 接口) 隔离；令牌数是小数，不提前取整。再补两条：时间在 `check` 内部读，所以时钟要能注入；当前策略用不到的参数可以是任意值。每一条都配一个带数字的测试，再动手写。

</details>

**知识点：** 限流器（Rate Limiter）、边界校验（Validate at the Boundary）、接口的错误契约（Error Contract）
