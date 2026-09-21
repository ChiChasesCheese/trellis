---
id: yield-value-vs-return-value-extra-state
node: iteration.generators
type: cloze
source: cpython-internals
---
生成器每次执行到 `yield` 时，`YIELD_VALUE` 字节码和普通 `return` 用的 `RETURN_VALUE` 一样都会把值压栈、交还执行权给调用帧；但 `YIELD_VALUE` 还要多做两件事才能让生成器之后能被恢复：更新帧的{{c1::指令指针（instruction pointer）}}，以及把解释器当前的{{c2::异常状态（exception state）}}保存到生成器对象上（恢复执行时再拷贝回解释器状态）。
