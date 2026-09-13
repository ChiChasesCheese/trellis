---
id: content-isr-failure-policy
node: content.isr
type: qa
---
## Q
ISR regeneration returns a partial HTML file before the database times out. What prevents this corrupt result from replacing the good page?

## A
Generate into an isolated temporary object, validate completion and required metadata, then commit with an atomic rename or conditional pointer update. On failure, retain the last successful page, release the singleflight lock, and retry later with backoff. Never stream regeneration directly into the live cache key. Record consecutive failure count and stale age so stale serving remains an availability policy, not silent decay.

## Q zh
ISR regeneration 在 database timeout 前产生了部分 HTML。什么机制阻止这个 corrupt result 替换正常页面？

## A zh
先生成到 isolated temporary object，验证 completion 和必需 metadata，再通过 atomic rename 或 conditional pointer update 提交。失败时保留上一次成功页面，释放 singleflight lock，之后用 backoff retry。绝不能把 regeneration 直接 stream 到 live cache key。记录 consecutive failure count 和 stale age，使 serve stale 是可观察的 availability policy，而不是静默腐化。
