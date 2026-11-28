---
id: hi-c-lld-patterns-n08-strategy
node: lld.in-a-hurry.patterns.notes
type: qa
step: 8
---
## Q
**设计模式 · Strategy：用组合替代条件分支**｜摘要 · 必会

Strategy 解决什么？它和 Factory 的分工是什么？为什么是最常被问的模式？

## A
- **作用：** 同一件事有多种做法，运行时可切换，用多态取代 if/else 或 switch
- **做法：** `ShoppingCart` 持有 `PaymentStrategy`，结账时委托；换策略就是换对象
- **分工：** Factory 决定创建哪个类，Strategy 决定创建之后用哪种行为
- **为什么常考：** 直接检验多态和"组合优于继承"；看到一堆按类型分支的代码，就是策略在等你
- "运行时"指程序执行中；"编译期"是类定义里写死的
