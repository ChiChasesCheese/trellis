---
id: compiling-cython-needs-type-annotations
node: performance.compiling
type: qa
tags: [grown]
---
## Q
直接把一段纯 Python 代码原封不动地丢给 Cython 编译，为什么速度提升往往很有限，甚至和解释执行差不多？

## A
Cython 真正的加速来自「给变量标注 C 语言的静态类型」（如 `cdef int i`），编译器据此把这些变量的运算直接翻译成 C 层面的操作，跳过 Python 对象的动态类型检查和装箱拆箱；如果代码里所有变量还是普通的 Python 对象（没有类型标注），编译出来的 C 代码本质上还是在反复调用 Python/C API 操作 Python 对象，速度提升非常有限。
