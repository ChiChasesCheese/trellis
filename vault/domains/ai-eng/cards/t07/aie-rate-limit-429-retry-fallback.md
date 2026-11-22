---
id: aie-rate-limit-429-retry-fallback
node: t07.rate-limit-retry-fallback
type: qa
step: 1
tags: [实践]
---
## Q
**Rate limit · 429 怎么退避、何时 fallback**｜实践 · 必会

晚高峰你的服务大量收到 429。全部立刻重试可以吗？重试和备用供应商怎么搭？

## A
**不可以立刻全部重试：** 同时重试会形成请求风暴，让限流持续。

**429 的处理：**

| 情形 | 做法 |
|---|---|
| 响应带 `retry-after` | 至少等这么多秒再重试 |
| 没有该头 | **指数退避加随机抖动**（jitter）：等待时间成倍增长，并随机错开，避免所有客户端同时回来（通用做法） |
| 突然放量 | 有些供应商有 **ramp limit**（限制用量增长速度）：保持在能成功的水平，每分钟最多增加一小步；批量任务从低速开始、均匀发 |
| 月度花费上限触发 | Anthropic 的 429 里**没有** `retry-after`，重试也不会成功：不要重试，要报警 |

**限制的维度：** 请求数每分钟（RPM）、输入 token 每分钟（ITPM）、输出 token 每分钟（OTPM）；Anthropic 的 ITPM **不计缓存读取的 token**，所以 prompt caching 同时提升吞吐。限流用 token bucket：容量持续补充，而不是整点重置。

**fallback（gateway 层做）：** 主 API 不可用或被限流时，路由到备用模型、等一会重试，或体面地失败。要点：
1. 备用路径要**单独评测**，换了模型输出可能不同；
2. 同一个模型在不同供应商那里可能略有差异；
3. 重试要有次数上限和总超时，并配合 circuit breaker；
4. 流式输出中途断开：已发出的部分不能撤回，要么从头重试并告知用户，要么把已收到的内容作为前缀续写（实现复杂，先做前者）。

<details class="pt" markdown="1"><summary>出处</summary>

Anthropic 文档 Rate limits（platform.claude.com/docs/en/api/rate-limits，2026-11-21 读）；Huyen《AI Engineering》ch10 §Gateway（fallback policies）

</details>
