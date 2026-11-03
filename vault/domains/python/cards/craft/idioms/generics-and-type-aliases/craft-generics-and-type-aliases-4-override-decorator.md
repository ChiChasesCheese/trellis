---
id: craft-generics-and-type-aliases-4-override-decorator
node: craft.idioms.generics-and-type-aliases
type: qa
step: 4
---
## Q
**泛型与类型别名 · 模板方法的钩子为什么要标 @override**｜写法

日志处理器的基类定义了钩子 `emit`，子类覆盖它。有人把子类里的方法拼成了 `emitt`，程序没有报错，只是基类的 `emit` 悄悄被调用，日志没按预期写出。怎样让这类错误在检查时就暴露？

## A
**要点。** 在 Python 里，子类写一个新名字的方法不会和基类有任何联系，拼错就是定义了一个无用的新方法。`@override`（`typing.override`，Python 3.12 起）告诉检查器：这个方法应该覆盖基类的方法；如果基类里没有同名方法，检查器报错。同样地，基类改名时，所有标了 `@override` 的子类会立刻被指出。

```python
from typing import override

class Handler:
    def emit(self, record: str) -> None:
        print("base", record)

class FileHandler(Handler):
    @override
    def emit(self, record: str) -> None:        # 确实覆盖了基类的 emit
        print("file", record)

class TypoHandler(Handler):
    @override
    def emitt(self, record: str) -> None:       # 拼错了名字：本想覆盖 emit
        print("typo", record)

TypoHandler().emit("x")                         # 运行时：悄悄走了基类的实现
```

实际输出：

```
base x
```

把上面的代码存成 `g4.py`，mypy 的检查结果：

```
g4.py:14: error: Method "emitt" is marked as an override, but no base method was found with this name  [misc]
```

**为什么。** 运行时输出 `base x` 就是问题所在：钩子被拼错后，调用走了基类的默认实现，没有任何异常。`@override` 在运行时几乎不做事，价值全在检查器那一侧。

**版本。** Python 3.11 的 `typing` 里没有 `override`（导入会报 `ImportError`），要用 `typing_extensions.override`。只有会被子类覆盖的钩子才值得标；基类和子类各有独立方法时不需要。
