---
id: hi-lld-oop-concepts-4-inheritance-vs-composition
node: lld.in-a-hurry.oop-concepts
type: qa
step: 4
---
## Q
**继承还是组合**｜低层设计 · 速览

继承（inheritance）什么时候合适，什么时候会出问题？为什么 LLD 默认用接口加组合（composition）？用汽车动力系统举例。

## A
**代价。** 继承让子类自动获得父类的数据和行为，是共享实现的工具，但代价是紧耦合：父类一改，所有子类都可能出问题，这就是脆弱基类问题（fragile base class）。

**适用。** 有稳定的、多个子类都需要的共享实现，而且关系稳定。例如 `SavingsAccount` 与 `CheckingAccount` 都是 `BankAccount`，存取款、余额、流水逻辑完全相同，子类不需要以破坏父类契约的方式覆盖行为。

**失效。** 用继承来表达行为差异是最典型的错误：`ElectricCar` 继承 `Car` 并重写 `start_engine`，但电动车根本没有发动机，没有可共享的逻辑；再加混合动力，是继承 `Car` 还是 `ElectricCar`？都不干净。

```python
class Drivetrain(ABC):
    @abstractmethod
    def start(self) -> None: ...         # 变化的行为抽成独立抽象

class Car:
    def __init__(self, drivetrain: Drivetrain) -> None:
        self.drivetrain = drivetrain     # 组合：新增氢能车只要新增一个 Drivetrain 实现

    def start(self) -> None:
        self.drivetrain.start()
```

**取舍。** 默认用接口加组合；只有需要共享稳定实现且关系稳定时才继承。多数 LLD 面试根本不需要继承。
