---
id: principles-ocp-trigger
node: principles.solid
type: qa
---
## Q
Every new discount type means editing the same growing `if/else` in `PriceCalculator` — and re-testing it. Which principle, what refactor, and when should you NOT apply it?

## A
**OCP**: extend behavior by adding code, not by modifying tested code. Refactor: extract a `DiscountRule` interface; each discount is a new class; the calculator folds over an injected list of rules.

Don't apply speculatively: a conditional with two stable cases doesn't earn the abstraction. OCP triggers on the *second or third* variant of the same axis — that's evidence the axis really varies.

## Q zh
什么时候你知道你的代码对修改不是开放的？

## A zh
触发器：
- 每次添加新的变化（新的支付方式、新的报告类型、新的日志级别），你都修改现有的类
- 一个 if-else 或 switch 在分派新类型，每种类型都需要修改
- 测试新功能需要修改现有代码，这意味着回归风险

解决方案通常涉及：
- 多态性：让子类实现扩展点
- 策略模式：注入新的行为对象
- 尽可能让变化通过参数或配置进行，而不是代码
