---
id: pl-abstraction-generics-foundation-python-generics
node: abstraction.generics
type: qa
step: 5
---
## Q
Python 的泛型是什么？为什么说它只存在于类型检查层，运行时根本不检查？

## A
Python 3.12（PEP 695）起可以用 `class Stack[T]` 声明泛型类，之前用 `TypeVar` 和 `Generic[T]`。语法的作用是**告诉静态检查器**（`mypy`、`pyright`）这个类里 `T` 是同一个类型。

```python
class Stack[T]:
    def __init__(self): self.items: list[T] = []
    def push(self, x: T): self.items.append(x)
s: Stack[int] = Stack()
s.push("not an int")        # 检查器报错，但运行时照常执行
print(s.items, Stack[int])  # ['not an int'] __main__.Stack[int]
```

运行时发生的事：`Stack[int]` 只是创建了一个记录类型参数的小对象（供反射和检查器使用），`Stack` 的实例并不知道自己是 `Stack[int]`，`push("not an int")` 照常成功。

原因是 Python 的类型注解被设计成**可选的、不影响执行**的元数据。这使得 Python 能渐进地加类型：旧代码不受影响，工具逐步增加检查。代价是类型错误如果没有人跑检查器，到运行期才会以别的形式暴露（比如后面某处对整数调用字符串方法）。因此 Python 项目里的泛型价值完全取决于 CI 里是否运行类型检查。
