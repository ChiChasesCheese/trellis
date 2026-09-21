---
id: compiling-three-paths-to-c
node: performance.compiling
type: cloze
tags: [grown]
---
把 Python 热点代码变成 C 速度，三条常见路径是：{{c1::Cython}}（给变量加类型标注后编译成 C 扩展，需要额外的构建步骤）、{{c2::Numba}}（用装饰器在运行时即时编译 JIT 数值函数，不需要单独构建但首次调用有预热开销）、{{c3::ctypes}}（直接调用已经编译好的外部 C/C++ 共享库，不编译你自己写的 Python 逻辑本身）。
