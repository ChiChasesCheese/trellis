---
id: pl-abstraction-interfaces-traits-foundation-python-abc-protocol
node: abstraction.interfaces-traits
type: qa
step: 3
---
## Q
Python 的抽象基类（ABC）和 `Protocol` 分别是什么？它们对应「显式声明」和「按形状满足」的哪一种？

## A
**ABC**（abstract base class）是显式声明路线：你继承它，并实现标了 `@abstractmethod` 的方法；漏了就**在实例化时**报错，而不是在定义类时。

```python
class Repo(ABC):
    @abstractmethod
    def get(self, k): ...
class Mem(Repo): pass
Mem()   # TypeError: Can't instantiate abstract class Mem
        #   without an implementation for abstract method 'get'
```

**Protocol**（Python 3.8 起，PEP 544）是按形状满足路线：它只描述需要哪些方法，实现者不必继承它。

```python
class Closer(Protocol):
    def close(self) -> None: ...
class F:                       # F 从未提到 Closer
    def close(self) -> None: print("closed")
def done(c: Closer): c.close()
done(F())                      # 输出 closed
```

`Protocol` 只在静态类型检查器（`mypy`、`pyright`）里起作用：运行时 `done(1)` 依然是在调用时才抛 `AttributeError`。给它加 `@runtime_checkable` 后，`isinstance(F(), Closer)` 是 `True`、`isinstance(1, Closer)` 是 `False`，但这只检查方法名是否存在，不检查签名。简记：ABC 管运行期的「不许实例化」，Protocol 管静态期的「形状是否对得上」。
