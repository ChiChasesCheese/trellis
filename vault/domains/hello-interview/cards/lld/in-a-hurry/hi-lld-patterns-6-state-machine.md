---
id: hi-lld-patterns-6-state-machine
node: lld.in-a-hurry.patterns
type: qa
step: 6
---
## Q
**状态机：把每个状态的行为封装成类**｜低层设计 · 速览

自动售货机这类对象的行为取决于内部状态且转换规则复杂。状态机（State Machine）怎么设计？面试里怎样表达它？

## A
**结构。** 定义状态接口，每个动作（投币、选货、出货）都是方法；每个具体状态类实现这些方法，并决定下一个状态。机器类持有当前状态，把动作委托给它。

```python
class NoCoinState(VendingMachineState):
    def insert_coin(self, m: "VendingMachine") -> None:
        m.set_state(HasCoinState())    # 自己决定下一个状态
    def select_product(self, m: "VendingMachine") -> None:
        print("Insert coin first")     # 非法动作也有明确响应
```

**好处。** 不用在每个方法里写大段 switch 判断当前状态；每个状态能做什么一目了然。

**信号。** 需求里“状态”这个词多次出现，例如售货机、文档审批流程、游戏阶段。状态机出现时，通常是整场面试的核心。

**表达。** 先画状态图：圆圈是状态，箭头是带动作标签的转换，面试官很欣赏这种可视化。
