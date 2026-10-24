---
id: pl-types-gradual-typing-best-practice
node: types.gradual-typing
type: qa
step: 8
---
## Q
在一个已有的 Python 代码库里，资深工程师怎样逐步引入类型提示并让它真正有效？

## A
目标是让类型覆盖率只升不降，并把检查器放进流水线，使它成为强制的而不是建议。

1. 先标公共边界：模块的公开函数、类的公开方法、数据模型。内部细节可以后补，因为边界的类型信息传播得最远。
2. 参数和返回值都标。漏掉返回值，检查器把返回值当作 `Any`，之后的调用全部失去检查。
3. 在 CI 里运行检查器（`mypy` 或 `pyright`），对新文件和已标注的文件启用严格模式（`--strict`），旧文件用配置逐个豁免，豁免清单只减不增。
4. 限制 `Any` 和 `# type: ignore`：忽略时写错误代码和原因（`# type: ignore[arg-type]  # 库 X 缺少类型`），并定期清理。
5. 在系统边界做运行时校验：来自 JSON、HTTP、数据库、配置的数据，类型提示不会检查，用 `pydantic` 或手写校验转换成已知类型，再进入有类型的内部。
6. 泛型用新语法（Python 3.12 起），检查器能准确追踪类型变量：

```python
class Box[T]:
    def __init__(self, v: T) -> None: self.v = v
    def get(self) -> T: return self.v

b = Box(1)
s: str = b.get()   # mypy: expression has type "int", variable has type "str"
```

`b.get()` 被推导为 `int`，赋给 `str` 变量时报错。

何时可以破例：一次性脚本、笔记本里的探索代码、测试里的快速夹具，不必强求。其余场合，类型提示的维护成本远低于线上排查类型错误的成本。
