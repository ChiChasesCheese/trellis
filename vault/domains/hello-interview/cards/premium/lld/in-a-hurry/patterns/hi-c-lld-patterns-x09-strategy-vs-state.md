---
id: hi-c-lld-patterns-x09-strategy-vs-state
node: lld.in-a-hurry.patterns.exam
type: qa
step: 9
---
## Q
**设计模式 · 策略与状态的区别**｜考点 · 追问

Strategy 和 State 的类图几乎一样，区别在哪里？

## A
- **谁决定切换：** 策略由外部（调用方、配置）选择，状态由对象自己在转换时切换
- **行为数量：** 策略通常只有一个操作，状态覆盖一组动作
- **相互了解：** 状态之间知道彼此（指定下一个状态），策略之间互不相关
- **选择：** 同一件事的多种做法选 Strategy；行为随生命周期变化选 State
