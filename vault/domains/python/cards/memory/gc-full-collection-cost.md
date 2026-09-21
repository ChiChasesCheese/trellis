---
id: gc-full-collection-cost
node: memory.cyclic-gc
type: qa
source: cpython-internals
---
## Q
为什么 CPython 的循环 GC 不是「第 2 代（最老一代）回收次数够多就触发」，而是用 `long_lived_pending / long_lived_total`（待考察的长寿对象数 / 长寿对象总数）超过 25% 这个比例来决定要不要做一次完整（full）回收？

## A
完整回收的开销和长寿对象总数成正比，而长寿对象总数可以无限增长；如果按固定的对象创建次数触发完整回收，创建并长期持有大量对象的程序会退化成二次方（quadratic）级别的开销（例如构建一个很大的、元素都被 GC 追踪的 list）。改用「待考察比例超过 25%」触发，使得摊还（amortized）到每个对象上的 GC 开销是线性的：对象越多，单次完整回收越贵，但做完整回收的频率也越低。
