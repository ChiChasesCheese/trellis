---
id: module-executes-once-via-sys-modules-cache
node: runtime.import-system
type: qa
source: python-docs
---
## Q
一个模块被 `import` 两次，第二次会重新执行模块顶层代码吗？Python 怎么知道该不该重新执行？

## A
不会。每次 `import` 时 Python 先查 `sys.modules`——一个模块名到模块对象的缓存字典。如果模块名已经在里面（且值不是 `None`），就直接返回缓存的模块对象，不重新执行模块代码；只有缓存里没有这个名字，才会真正搜索、创建并执行模块。这也是模块顶层的初始化语句只在「第一次」被 import 时真正跑一遍的原因。
