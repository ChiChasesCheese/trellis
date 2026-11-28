---
id: hi-c-sd-networking-essentials-x09-retry-storm
node: sd.core-concepts.networking-essentials.exam
type: qa
step: 9
---
## Q
**网络基础 · 重试把下游打垮了**｜考点 · 必会

下游服务变慢，上游所有实例立刻重试三次，结果下游彻底挂掉。怎么修？

## A
- **原因：** 重试放大了负载（惊群），注定失败的请求被反复发送，下游无法恢复。
- **修复：** 指数退避加抖动，客户端不同步重试；限制重试次数；接口幂等才能安全重试。
- **熔断器：** 失败超阈值就打开，立即失败，不再调用；超时后半开放少量探测请求，成功则关闭。给下游喘息并避免级联。
- **面试加分：** 说出"retry with exponential backoff and jitter"，并补上熔断与降级（回退到缓存或默认值）。
