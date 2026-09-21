---
id: for-iter-gen-bypasses-dunder-next
node: iteration.generators
type: qa
source: cpython-internals
---
## Q
`for` 循环遍历一个生成器时，CPython 解释器是不是老老实实地每轮都调用一次生成器的 `__next__()` 方法？

## A
不一定。`FOR_ITER` 字节码本来的语义就是对栈顶迭代器调用 `__next__()`，但 CPython 针对常见迭代器类型做了特化（specialization）：遇到生成器时会切换成 `FOR_ITER_GEN` 变体，直接把生成器的帧压入解释器栈、从上次 `yield` 之后的指令继续执行，完全绕开 `__next__()` 这次方法调用的开销。这是 CPython 的内部优化，不是语言规范要求的行为。
