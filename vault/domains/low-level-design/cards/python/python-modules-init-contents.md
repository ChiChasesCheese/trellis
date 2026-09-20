---
id: python-modules-init-contents
node: python.modules
type: qa
step: 4
tags: [grown]
---
## Q
`__init__.py` 应该放什么，不应该放什么？为什么把业务逻辑写进 `__init__.py` 是个坏主意？

## A
应该放这个包对外的**公共入口**：把内部子模块的关键名字重新导出（`from .order import Order`），可选地用 `__all__` 声明 `from pkg import *` 该导出什么。不应该放真正的业务逻辑——因为 `import pkg` 这一行会**立即、完整**执行 `__init__.py`：逻辑越多，import 的副作用越大、越慢，也越容易在这个包被别的模块 import 时触发循环导入（因为 `__init__.py` 几乎总是最早被执行的那份代码）。
