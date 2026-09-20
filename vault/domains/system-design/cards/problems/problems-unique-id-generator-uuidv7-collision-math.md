---
id: problems-unique-id-generator-uuidv7-collision-math
node: problems.foundations.unique-id-generator
type: qa
step: 6
tags: [grown]
---
## Q
In a system generating unique IDs at a platform-wide peak of 200 IDs per millisecond, why does using UUIDv7 in pure-random mode (74 bits of combined rand_a and rand_b entropy per RFC 9562) still avoid collisions in practice, even without spending any bits on a monotonic counter?

## A
With 74 bits of random space (about 1.9x10^22 possible values) and 200 IDs generated within any single millisecond window at peak, the birthday-bound collision probability for that one window is on the order of 10^-18 — vanishingly small even before considering that a full day contains only about 86.4 million such millisecond windows. This shows that pure randomness in UUIDv7's rand_a/rand_b fields is sufficient to avoid collisions at realistic scale without needing the counter-based monotonicity method the RFC also allows; the counter method exists to guarantee strict same-millisecond ordering, not because pure randomness would otherwise collide.

## Q zh
在一个整个平台峰值每毫秒生成 200 个 ID 的系统中，为什么即使不把任何位数花在单调计数器上，使用纯随机模式的 UUIDv7（RFC 9562 里 rand_a 和 rand_b 合计 74 位随机熵）在实践中依然能避免碰撞？

## A zh
74 位随机空间（约 1.9×10^22 种可能取值），配合峰值下任意一个毫秒窗口内生成 200 个 ID，该窗口的生日悖论碰撞概率量级约为 10^-18——即使不考虑一整天只有约 8,640 万个这样的毫秒窗口，这个数字也已经微乎其微。这说明 UUIDv7 的 rand_a/rand_b 字段单纯依靠随机性，在现实规模下就足以避免碰撞，不需要动用规范同时允许的基于计数器的单调性方法；计数器方法存在的目的是保证严格的同毫秒排序，而不是因为纯随机性本身会撞车。
