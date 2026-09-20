---
id: oop-default-methods
node: oop.interfaces
type: qa
step: 2
---
## Q
Java 接口的 default 方法解决了"接口发布之后还能不能安全加方法"的问题。Python 里最接近的等价物是什么，`Protocol` 能不能提供同样的东西？

## A
最接近的等价物是 `abc.ABC` 上的**非抽象方法**——除了 `@abstractmethod` 声明的方法，ABC 也可以直接给出具体实现，子类不覆盖就直接继承使用：

```python
class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...
    def describe(self) -> str:
        return f"area={self.area():.2f}"
```

但这要求走 `ABC` 这条名义子类型路线。`typing.Protocol` 完全没有这个概念——它只描述结构（有没有这个方法签名），本身不携带实现，也不参与继承链，所以"给一个默认实现"这件事在纯 `Protocol` 的世界里根本不存在。
