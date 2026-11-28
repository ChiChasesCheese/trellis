---
id: hi-c-lld-oop-concepts-n06-inherit-breaks
node: lld.in-a-hurry.oop-concepts.notes
type: qa
step: 6
---
## Q
**面向对象概念 · 继承何时失效**｜摘要 · 必会

为什么用继承表达"行为差异"是常见错误？应该怎么建模？

## A
- **警示信号：** 子类要重写父类的方法来给出完全不同的实现，说明你在用继承表达"行为变化"，而继承适合"共享实现"。
- **例子：** `ElectricCar` 继承 `Car` 并重写 `start_engine`，但电动车没有发动机，也不共享燃油逻辑；以后加混合动力车，不知该继承 `Car` 还是 `ElectricCar`，哪个都不干净。
- **改法：** 把会变化的行为单独抽象出来再组合：定义 `Drivetrain` 接口，`GasEngine`、`ElectricMotor` 各自实现，`Car` 持有一个 `Drivetrain`。
- **效果：** 混合动力车就给两个动力系统，氢能源车新增一个实现；`Car` 本身不用改。
