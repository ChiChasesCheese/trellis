---
id: hi-c-lld-oop-concepts-x06-hybrid-car
node: lld.in-a-hurry.oop-concepts.exam
type: qa
step: 6
---
## Q
**面向对象概念 · 混合动力怎么建模**｜考点 · 必会

已有 `Car` 与 `ElectricCar(Car)`，现在要加混合动力车。继承方案哪里卡住，组合方案怎么做？

## A
- **继承卡点：** 继承 `Car` 还是 `ElectricCar`？无论哪个都要重写启动逻辑；多重继承会引入菱形，并让两套逻辑纠缠
- **组合：** `Car` 持有一个 `Drivetrain`；混合动力是一个组合两个动力系统的 `HybridDrivetrain`，或者持有列表
- **效果：** `Car` 代码不变，新增的只是新类
- **补充问题：** 启动顺序和切换策略放在 `HybridDrivetrain` 里
