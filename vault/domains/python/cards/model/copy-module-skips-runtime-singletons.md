---
id: copy-module-skips-runtime-singletons
node: model.copy
type: qa
source: python-docs
---
## Q
对 module（模块）、函数、类这类对象调用 `copy.copy()` 或 `copy.deepcopy()` 会发生什么？为什么这样处理是安全的？

## A
`copy` 模块不会真的复制 module、函数、方法、栈帧、文件、socket 这类对象，而是直接返回原对象本身，不新建副本（这与 `pickle` 模块处理它们的方式一致）。这些对象通常代表进程里唯一的运行时资源或命名空间，复制出第二份既不安全也没有意义，所以模块选择直接复用原对象。
