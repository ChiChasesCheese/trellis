---
id: problems-rate-limiter-three-layer-quota-model
node: problems.foundations.rate-limiter
type: qa
step: 2
tags: [grown]
---
## Q
In a rate limiter design, why does enforcing only a per-API-key limit fail to protect the backend even when every single key stays within its own quota, and what three layers does the design use instead?

## A
Every key individually staying under its own limit says nothing about the sum of all keys' traffic — thousands of keys each safely under quota can still add up to far more load than the backend can serve, an 'individually compliant, collectively overloaded' failure. The design stacks three layers that a request must pass simultaneously: (1) per-key sustained and burst limits for fairness between callers, (2) per-endpoint limits weighted by cost (e.g. a bulk export consumes 50 quota units versus 1 for a simple GET) so cheap and expensive operations aren't counted the same, and (3) a global fleet limit that caps total admitted traffic regardless of which keys it comes from, protecting the backend even when every individual key is compliant.

## Q zh
在一个速率限制器设计中，为什么即使每一个 API key 都没有超过自己的配额，只做 per-key 限制仍然保护不了后端？这个设计用了哪三层来代替它？

## A zh
每个 key 各自没超额，并不能说明所有 key 加总的流量有多大——成千上万个各自安全达标的 key，加总流量仍可能远超后端承载能力，这是一种'个体合规、整体过载'的故障模式。这个设计让请求必须同时通过三层：①per-key 的 sustained 和 burst 限制，保证调用方之间的公平性；②按成本加权的 per-endpoint 限制（例如一次批量导出消耗 50 个配额单位，一次简单 GET 消耗 1 个），让昂贵操作和廉价操作不被同等计数；③不挂在任何单一 key 上的全局 fleet 限制，无论流量来自哪些 key，都对总放行量设上限，即使每个 key 都合规也能保护后端。
