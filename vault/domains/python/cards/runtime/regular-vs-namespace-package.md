---
id: regular-vs-namespace-package
node: runtime.import-system
type: qa
source: python-docs
---
## Q
「常规包」（regular package）和「命名空间包」（namespace package，PEP 420）在文件结构和导入表现上有什么区别？

## A
常规包必须有 `__init__.py`，导入时该文件会被隐式执行，其定义的内容绑定进包的命名空间。命名空间包没有 `__init__.py`，是由多个「部分」（portion，可能分布在文件系统不同位置甚至压缩包里）拼成的复合体，导入时不执行任何初始化代码；它的 `__path__` 也不是普通列表，而是一个会在 `sys.path` 变化后自动重新搜索的可迭代对象。
