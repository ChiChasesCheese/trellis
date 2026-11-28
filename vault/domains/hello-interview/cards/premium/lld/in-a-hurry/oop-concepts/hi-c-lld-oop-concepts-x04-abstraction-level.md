---
id: hi-c-lld-oop-concepts-x04-abstraction-level
node: lld.in-a-hurry.oop-concepts.exam
type: qa
step: 4
---
## Q
**面向对象概念 · 抽象粒度判断**｜考点 · 必会

两个接口：`Handler.handle(request)` 和 `PaymentMethod.process(amount)`。哪个抽象得好？怎么判断一个抽象是否合适？

## A
- **操作名有含义才好：** `PaymentMethod.process(amount)` 好：操作名有明确含义，参数和结果清楚，调用方不需要知道实现
- **泛化的 handle 太空泛：** `Handler.handle(request)` 空泛：什么都能塞，实现者各行其是，调用方无从判断行为
- **检验：** 能否只看接口就写出调用方代码；能否用不同实现替换且调用方不变
- **反向检验：** 接口里是否泄露实现细节（如 `set_api_key`）
