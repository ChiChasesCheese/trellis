---
id: reliability-slo-dependency-ceiling
node: reliability.slo
type: cloze
---
A service's achievable SLO is capped by its **hard dependencies**: if you call a 99.9% service synchronously on every request, you cannot credibly promise more than {{c1::~99.9% (minus your own failures — hard dependencies multiply in)}}. To offer a *higher* SLO than a dependency you must {{c2::take it off the critical path — cache its data, degrade gracefully without it, or make the call async}}. Rule of thumb: your critical dependencies should each be about one nine *more* reliable than the SLO you sell.

## zh
一个服务的可实现 SLO 受其**硬依赖**限制：如果你每个请求同步调用一个 99.9% 服务，你无法可信地承诺超过 {{c1::~99.9%（减去你自己的故障——硬依赖乘以）}}。要提供*更高的* SLO 比依赖你必须 {{c2::将其从临界路径移除——缓存其数据，在没有它的情况下优雅降级，或使调用异步}}。经验法则：你的临界依赖每个应该比你出售的 SLO 大约多一个九的可靠性。
