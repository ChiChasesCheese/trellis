---
id: traffic-rate-limiting-vs-load-shedding
node: traffic.rate-limiting
type: qa
---
## Q
Rate limiting vs load shedding — different triggers, different fairness. Draw the distinction and say why you need both.

## A
- **Rate limiting**: a *per-client contract* (quota), enforced even at 10% utilization — protects tenants from each other and makes cost predictable.
- **Load shedding**: *self-protection under actual overload*, triggered by health signals (queue depth, CPU, latency), dropping traffic regardless of anyone's quota — protects the service itself.

Shedding is priority-ordered: drop unauthenticated, background, and retry traffic before paid interactive requests; never shed health checks.

You need both because every client staying within quota can still sum to more than the system can serve.

## Q zh
速率限制 vs 负载丢弃 — 不同的触发器，不同的公平性。画出区别并说为什么你需要两个。

## A zh
- **速率限制**：一个*每客户端合约*（配额），即使在 10% 利用率时强制执行 — 保护租户彼此并使成本可预测。
- **负载丢弃**：*在实际过载下的自保护*，由健康信号触发（队列深度、CPU、延迟），删除流量不管谁的配额 — 保护服务本身。

丢弃是优先级排序的：在已付费交互请求之前删除未认证、后台和重试流量；永不丢弃健康检查。

你需要两者因为每个客户端停留在配额内仍然可以总和超过系统可以服务。
