---
id: content-negotiation-server-choice
node: content.negotiation
type: qa
---
## Q
When should a CDN prefer explicit format URLs over server-driven `Accept` negotiation?

## A
Use explicit URLs when deterministic identity, simple cache keys, signed delivery, or pre-generation matters more than transparent client choice. Use `Accept` negotiation when one canonical URL and automatic capability selection improve ergonomics, but only with correct `Vary` and bounded normalization. Explicit identity simplifies debugging and purge; negotiation reduces application URL variants but moves correctness into cache policy.

## Q zh
CDN 什么时候应优先使用显式 format URL，而不是 server-driven `Accept` negotiation？

## A zh
当 deterministic identity、简单 cache key、signed delivery 或 pre-generation 更重要时，使用显式 URL。若希望一个 canonical URL 自动选择 client capability，可用 `Accept` negotiation，但必须正确设置 `Vary` 并做 bounded normalization。显式 identity 简化 debugging 与 purge；negotiation 减少应用 URL variant，却把正确性转移到 cache policy。
