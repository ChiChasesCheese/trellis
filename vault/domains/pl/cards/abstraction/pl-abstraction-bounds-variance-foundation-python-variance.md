---
id: pl-abstraction-bounds-variance-foundation-python-variance
node: abstraction.bounds-variance
type: qa
step: 5
---
## Q
Python 的类型检查器怎样处理型变？`TypeVar` 的协变声明和 3.12 的自动推导是什么意思？

## A
Python 的类型检查在检查器里发生，所以型变也是检查器的规则。老写法是在 `TypeVar` 上显式声明：`T_co = TypeVar("T_co", covariant=True)`，声明的变体必须与类的使用方式一致，否则检查器报错。

PEP 695（Python 3.12）的新语法 `class Box[T]` 让检查器**自动推导变体**：看 `T` 在类里出现在什么位置。

```python
class Box[T]:                      # 只在返回值里用 T
    def get(self) -> T: ...
class MBox[T]:                     # 既读又写
    def get(self) -> T: ...
    def set(self, v: T) -> None: ...
def f(b: Box[object]): ...
def g(b: MBox[object]): ...
f(Box[int]())      # 通过：Box 被推导为协变
g(MBox[int]())     # mypy: expected "MBox[object]"，不通过
```

`Box` 只读，推导为协变，所以 `Box[int]` 可用于 `Box[object]`；`MBox` 可写，推导为不变，被拒绝。

可调用对象 `Callable` 的参数则是逆变的：能处理 `Animal` 的函数可以传给要求「处理 `Dog` 的函数」的参数，反之不行，检查器会报 `incompatible type "Callable[[Dog], None]"; expected "Callable[[Animal], None]"`。

这些规则全部只在静态检查时生效，运行期 `g(MBox[int]())` 照样执行。这与 Java 的运行期兜底（数组存储检查）完全不同。
