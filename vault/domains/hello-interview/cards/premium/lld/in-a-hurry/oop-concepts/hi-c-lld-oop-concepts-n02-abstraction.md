---
id: hi-c-lld-oop-concepts-n02-abstraction
node: lld.in-a-hurry.oop-concepts.notes
type: qa
step: 2
---
## Q
**面向对象概念 · 抽象**｜摘要 · 必会

抽象（abstraction）解决什么问题？应该在系统的什么位置引入？抽象层次怎么把握？

## A
- **含义：** 只暴露本质，用清晰的接口隐藏实现；接口说明"能做什么"，不说明"怎么做"。
- **收益是简化：** `OrderService` 依赖 `PaymentMethod` 接口，而不是具体的 Stripe 类，就能随时换实现，调用方只管调用 `process()` 拿结果。
- **在哪里引入：** 在逻辑缠绕的地方——变体多、规则杂、细节乱的区域，或需求暗示有多种做法时；这些信号表示引入抽象会让其余代码更容易理解。
- **层次的把握：** 太抽象（`doWork()`、`handleRequest()`）等于什么都没说；太具体又等于没抽象。从调用方需要执行的操作出发，而不是从实现细节出发。
