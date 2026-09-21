---
id: string-interning-two-mechanisms
node: memory.interning-immortal
type: qa
source: cpython-internals
---
## Q
CPython 用两种不同机制来驻留字符串，分别是什么？

## A
一种是「静态单例」（singletons）：256 个单字符的 latin-1 字符串、以及编译器源码里用 `_Py_ID`/`_Py_STR` 标记的固定字符串（含空字符串），在运行时初始化阶段就存进静态分配的数组里，运行期间不再变化。另一种是「动态驻留」（dynamic interning）：其余的字符串在运行过程中按需被加进一个按解释器（interpreter）维度维护的字典里完成驻留。
