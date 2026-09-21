---
id: string-interning-singleton-count
node: model.names-objects
type: qa
source: cpython-internals
---
## Q
CPython 会把哪些字符串在解释器初始化时就静态分配好并全局驻留（string interning），无需运行时判断？

## A
256 个单字符的 latin-1 字符串（每个字节值一个单例），以及编译器内部标记为 `_Py_ID`/`_Py_STR` 的标识符和常量字符串，都在初始化时存入静态数组并驻留；这些单例跨所有线程和子解释器（sub-interpreter）无锁共享，且一旦驻留就不可撤销，直到解释器关闭。
