---
id: abstractmethod-blocks-instantiation
node: classes.abc-protocols
type: qa
source: python-docs
---
## Q
`@abstractmethod` 具体做了什么，光是在方法上加这个装饰器就够了吗？

## A
不够。`@abstractmethod` 要求这个类的元类（metaclass）是 `ABCMeta` 或其子类（继承 `abc.ABC` 就自动满足），否则装饰器不起作用。满足这个前提后，只要类里还有任何一个抽象方法/属性没被子类重写，这个类（及其未完全实现的子类）就无法被实例化，尝试 `SomeClass()` 会报 `TypeError`。抽象方法本身可以有函数体（不像 Java 的抽象方法必须为空），子类重写后仍可以通过 `super()` 调用父类里这份实现，只是不能跳过重写这一步。
