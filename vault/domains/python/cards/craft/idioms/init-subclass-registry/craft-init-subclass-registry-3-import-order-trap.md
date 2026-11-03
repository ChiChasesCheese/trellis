---
id: craft-init-subclass-registry-3-import-order-trap
node: craft.idioms.init-subclass-registry
type: qa
step: 3
---
## Q
**__init_subclass__ 注册表 · 为什么自动登记的类有时「不存在」**｜写法

用 `__init_subclass__` 自动登记之后，有人新增了插件文件 `fifo_plugin.py`，配置里写了 `fifo`，启动却报「未知策略」，而文件明明在磁盘上。哪里出了问题？

## A
**要点。** 自动登记发生在类定义被执行的时候，而类定义只有在模块被导入时才会执行。文件在磁盘上不等于模块被导入过。所以自动登记要求有人负责导入所有插件模块：应用启动时显式 `import` 它们，或者用包的入口点（entry point）机制按约定扫描并导入。漏掉导入，注册表里就缺了这个类，错误表现为「未知名字」，很难想到是导入的问题。

```python
import importlib, pathlib, sys, tempfile

tmp = pathlib.Path(tempfile.mkdtemp())
(tmp / "base.py").write_text('''
class Policy:
    registry: dict[str, type] = {}
    def __init_subclass__(cls, /, name: str | None = None, **kw) -> None:
        super().__init_subclass__(**kw)
        if name is not None:
            Policy.registry[name] = cls
''')
(tmp / "fifo_plugin.py").write_text('''
from base import Policy
class FifoPolicy(Policy, name="fifo"): ...
''')
sys.path.insert(0, str(tmp))

from base import Policy
print(sorted(Policy.registry))                 # 插件文件在磁盘上，但还没有被导入
importlib.import_module("fifo_plugin")         # 导入它，类定义执行，登记才发生
print(sorted(Policy.registry))
```

实际输出：

```
[]
['fifo']
```

**为什么。** 第一行显示插件文件在磁盘上，注册表仍然是空的；第二行导入之后才出现。手写字典没有这个问题，因为字典所在的模块导入时，所有名字已经静态可见。

**代价。** 自动登记把「有哪些实现」从一处可读的代码，变成「取决于运行时导入了什么」。排查问题时多一层：先问这个模块有没有被导入。所以用自动登记，就要有一个明确的地方集中导入所有实现，并有测试检查已知名字齐全。
