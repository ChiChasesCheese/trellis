---
id: python-modules-circular-import-cause
node: python.modules
type: qa
step: 2
tags: [grown]
---
## Q
`a.py` 顶部写 `import b`，`b.py` 顶部写 `import a`，运行会出什么问题？根因是什么？

## A
假设先 `import a`：Python 开始执行 `a.py`，执行到 `import b` 时去执行 `b.py`；`b.py` 执行到对应的 `import a` 时，发现 `a` 已经在 `sys.modules` 里（正在被加载，防止无限递归），于是直接拿回这个**尚未执行完**的 `a` 模块对象——如果 `b.py` 接着想用 `a` 模块里、还没执行到的那个名字（比如 `a.some_func`），就会得到 `AttributeError`。根因是**两个模块在各自顶层依赖对方还没执行完的内容**，不是“循环 import 本身违法”。
