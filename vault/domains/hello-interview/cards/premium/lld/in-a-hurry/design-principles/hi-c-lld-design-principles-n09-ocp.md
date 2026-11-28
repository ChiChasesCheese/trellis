---
id: hi-c-lld-design-principles-n09-ocp
node: lld.in-a-hurry.design-principles.notes
type: qa
step: 9
---
## Q
**设计原则 · OCP：对扩展开放，对修改封闭**｜摘要 · 必会

开闭原则（OCP）怎么做到？一个靠 `if payment_type == ...` 分支的支付处理器该怎么改？

## A
- **含义：** 类应该对扩展开放、对修改封闭——加新行为时，不需要改动已有代码，通常靠接口或抽象类实现。
- **为什么：** 每次改动旧代码都可能弄坏已经好用的功能；新增类则不会影响旧类，因为旧代码根本没动。
- **反例：** 处理器里按支付类型写 `if/elif`，每加一种方式（比如加密货币）就要改这个方法。
- **改法：** 定义 `PaymentMethod` 抽象，信用卡、PayPal、加密货币各自实现；`PaymentProcessor` 只调用 `method.process(amount)`。
- **效果：** 新增支付方式只是新增一个类，处理器一行不改。
