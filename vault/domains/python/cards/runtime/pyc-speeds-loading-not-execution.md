---
id: pyc-speeds-loading-not-execution
node: runtime.compile-bytecode
type: qa
source: cpython-internals
---
## Q
把模块编译缓存成 `.pyc` 会让程序运行得更快吗？

## A
不会。`.pyc` 缓存只省去下次导入时重复做词法分析和语法分析的时间，加快的是「加载」（loading）这一步；一旦进入求值循环，从 `.pyc` 读出的字节码和现场编译出的字节码执行速度完全一样。真正决定运行速度的是解释器本身（如自适应特化），不是有没有编译缓存。
