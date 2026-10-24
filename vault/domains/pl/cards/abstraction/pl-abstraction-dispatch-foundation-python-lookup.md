---
id: pl-abstraction-dispatch-foundation-python-lookup
node: abstraction.dispatch
type: qa
step: 4
---
## Q
CPython 里执行 `x.area()` 要做哪些查找？自适应特化解释器（3.11 起）怎样让它变快？

## A
Python 的对象和类都是可以在运行期被修改的：随时可以给类添加方法，甚至替换 `obj.__class__`。所以每次 `x.area()` 原则上要做：

1. 取 `type(x)`，沿它的方法解析顺序在各个类的字典里按名字 `area` 找（哈希查找）；
2. 同时还要检查实例自己的属性字典里有没有同名项（可能遮蔽方法）；
3. 找到后再做调用。

这比一次表下标慢得多。CPython 3.11 引入**自适应特化解释器**（specializing adaptive interpreter）：解释器发现某条字节码连续多次遇到同一类型，就把它原地改写成一条「假设类型不变」的专用指令，附带一个版本号检查；类被修改时版本号变化，专用指令失效并退回通用版本。

用 `dis.dis(f, adaptive=True)` 在多次调用后能看到：

```text
LOAD_ATTR_METHOD_WITH_VALUES  (area + NULL|self)
CALL_PY_EXACT_ARGS            0
```

通用的 `LOAD_ATTR` 已经变成了专用版本，跳过了字典查找。这与 HotSpot 的内联缓存思路一致：在运行期观察，对稳定的情形走快路径。区别是 Python 的快路径只能省查找，不能内联函数体，所以它的上限远低于 JIT 的内联。
