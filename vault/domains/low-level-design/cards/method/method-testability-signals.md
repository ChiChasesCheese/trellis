---
id: method-testability-signals
node: method.evaluation
type: qa
---
## Q
一个评分者用 30 秒的时间浏览你的代码"可测试"。他们实际上看的是什么?

## A
他们是否能**不构建世界**的情况下练习一个规则:

- 费用/分配逻辑是参数作为其输入，还是到达一个完全构建的 `ParkingLot`?
- 任何 `new Collaborator()`、`Singleton.getInstance()` 或 `LocalDateTime.now()` **内部**逻辑? 每一个是一个不可替代的依赖 — 一个注入的 `Clock` 是标准的迹象你已经遇见过这个。
- 是否有趣的规则是它们的参数的纯函数，I/O 和突变推到边缘?

"我写了测试"比让他们的构造函数弱。
