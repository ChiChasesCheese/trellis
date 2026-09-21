---
id: code-object-composition
node: runtime.compile-bytecode
type: qa
source: cpython-internals
---
## Q
编译产出的 `PyCodeObject`（code 对象）里打包了什么？为什么说它「基本不可变」？

## A
除了字节码本身（3.11 起字段名是 `co_code_adaptive`，会被自适应解释器原地改写成特化指令），还打包了常量表（consts）、名字表（names）、变量名，以及记录每条指令对应源码行列号的定位表（用于生成回溯 traceback）。整体被视为不可变（可哈希、可比较），但字节码数组和少数运行时监控字段是例外——这些可变字段在哈希和比较时被直接忽略，不计入相等性判断。
