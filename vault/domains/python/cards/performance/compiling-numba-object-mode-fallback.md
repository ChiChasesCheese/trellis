---
id: compiling-numba-object-mode-fallback
node: performance.compiling
type: qa
tags: [grown]
---
## Q
用 `@numba.njit` 编译一个操作字符串或自定义类实例的函数，为什么经常直接报错或者反而比纯 Python 还慢？

## A
Numba 的即时编译只对数值类型（整数、浮点数、NumPy 数组等）及其组合做了高效的机器码生成（nopython 模式）；一旦函数体涉及任意 Python 对象（字符串处理、自定义类、字典等），`@njit`（以及 0.59 起默认 nopython 的 `@jit`）会直接报 TypingError 编译失败；只有显式 `@jit(forceobj=True)` 才退回逐个操作 Python 对象的「object 模式」，这时拿不到 JIT 加速，还多一层调度开销，反而更慢。
