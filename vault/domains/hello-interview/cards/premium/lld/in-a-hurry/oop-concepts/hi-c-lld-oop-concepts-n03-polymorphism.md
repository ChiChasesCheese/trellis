---
id: hi-c-lld-oop-concepts-n03-polymorphism
node: lld.in-a-hurry.oop-concepts.notes
type: qa
step: 3
---
## Q
**面向对象概念 · 多态**｜摘要 · 必会

多态（polymorphism）替代了什么写法？它有什么代价，面试里怎么讲取舍？

## A
- **替代：** `if type == "credit"`、对车辆类型的 `switch`；改成调用同一个方法，让每个对象自己处理
- **前提：** 先有抽象（如 `Vehicle` 接口），各实现自带行为，新增类型只需新增一个类，调用方不变
- **何时用：** 行为随类型变化；看到类型判断或对枚举的 switch 就是信号
- **代价：** 实现越多越难追踪和调试，新人上手难；有的公司偏好显式分支，要能讲出两边取舍
