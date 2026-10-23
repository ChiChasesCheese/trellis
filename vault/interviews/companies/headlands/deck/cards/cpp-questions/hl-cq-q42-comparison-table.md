---
id: hl-cq-q42-comparison-table
node: cpp-questions.j-cross-language
type: qa
step: 16
---
## Q
Python 和 C++ 在类型检查、执行方式、整数、并发这四点上分别怎样？

## A
| 方面 | Python | C++ |
|---|---|---|
| 类型 | 动态，运行时才检查 | 静态，编译期检查 |
| 执行 | 解释（字节码 + 解释器） | 编译成机器码 |
| 整数 | 任意精度，不溢出 | 固定宽度：`int` 4 字节，溢出（有符号 UB，无符号回绕） |
| 并发 | GIL：线程不能并行跑 Python 代码（用多进程 / 原生扩展） | 真正的多线程 + 内存模型 |
