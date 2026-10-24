---
id: pl-eco-modules-intro-python
node: ecosystem.modules
type: qa
step: 5
---
## Q
Python 的模块、包和导入系统是什么？`import` 实际做了什么，`sys.path` 与 `sys.modules` 起什么作用？

## A
**模块**：一个 `.py` 文件就是一个模块，它的名字是文件名。**包**（package）是含有 `__init__.py` 的目录（也可以是没有该文件的命名空间包，PEP 420），可以嵌套。

**`import` 在运行时执行**，大致三步：
1. 查缓存：看 `sys.modules`（一个字典）里有没有这个名字，有就直接返回。
2. 查找：按顺序在 `sys.path`（目录列表）里找。第一个元素是运行脚本所在目录（或空串，表示当前目录），然后是标准库、第三方库目录。
3. 加载：**从头到尾执行**这个文件的全部顶层代码，把结果对象放进 `sys.modules` 和调用者的命名空间。

所以 `import` 是真执行，且每个模块在一个进程里只执行一次。导入一个模块可能触发副作用（打印、连接数据库、导入更多模块）。

**没有访问控制**：所有名字都可见；下划线开头的 `_name` 只是约定，`from m import *` 会尊重 `__all__`。

**两个经典后果**：
1. **循环导入**：`a` 导入 `b`，`b` 又导入 `a`。第二次导入 `a` 时它还在执行中（只加载了一半），`from a import fa` 取不到还没定义的名字，真实报错：`ImportError: cannot import name 'fa' from 'a'`。
2. **路径遮蔽**：脚本目录排在 `sys.path` 最前，你在旁边放一个叫 `random.py` 的文件，`import random` 就拿到你的，而不是标准库的。真实报错：`AttributeError: module 'random' has no attribute 'randint'`。

**要记住的一点**：Python 的模块系统是运行时的、执行式的、没有强边界；灵活，也容易被路径和顺序坑。
