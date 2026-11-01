---
id: hi-lld-design-principles-1-how-to-use
node: qb.lld.kv-store-eviction.pre-lld-in-a-hurry-design-principles
type: qa
step: 1
---
## Q
**原则怎么用：KISS 与过度设计**｜低层设计 · 速览

低层设计面试里设计原则应当怎样使用？为什么说 KISS 是最常被违反的一条？

## A
**怎么用。** 原则是做决定时的思考工具，不是要背诵的口诀。面试官看你有没有应用它们，而不是能不能报出 SOLID 缩写。只想记三条通用原则，就记 KISS、DRY、YAGNI。

**KISS。** 能用的最简单方案通常最好：一个简单条件能解决，就别上策略模式；一个类够用，就别拆。

**易错。** 候选人常为展示知识，用不着也引入工厂、建造者、装饰器，面试官会注意到。复杂度要等简单方案失效再加：类膨胀到 500 行、十种职责，或者加一种支付方式要改五处，才重构。
