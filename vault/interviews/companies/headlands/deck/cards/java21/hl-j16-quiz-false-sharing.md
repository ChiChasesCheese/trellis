---
id: hl-j16-quiz-false-sharing
node: java21.j16-concurrency-primitives
type: qa
step: 42
---
## Q
伪共享的原理是什么？怎么检测、怎么避免？

## A
两个互不相关的变量在**同一缓存行**，不同核写它们会不断使对方缓存行失效，导致性能下降。

- 检测：性能剖析看缓存未命中、`perf c2c`，或做对照实验（把变量隔开比较耗时）。
- 避免：填充或拆到不同缓存行（`@Contended`、手动 padding），或每线程用自己的状态再合并（`LongAdder` 思路）。
