---
id: calling-generator-function-does-not-run-body
node: iteration.generators
type: qa
source: cpython-internals
---
## Q
调用一个生成器函数（如 `g = gen(3)`）时，函数体里的代码会立刻开始执行吗？CPython 字节码层面是怎么做到的？

## A
不会。生成器函数的字节码以 `RETURN_GENERATOR` 指令开头：它创建一个生成器对象，把该对象内嵌的帧初始化为「当前调用帧的拷贝」，随后立刻把这个生成器对象压栈并返回给调用者——此时函数体一行代码都还没执行。函数体真正开始运行，要等到第一次对这个生成器调用 `__next__()` 或 `send()`。
