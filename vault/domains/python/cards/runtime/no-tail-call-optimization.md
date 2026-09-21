---
id: no-tail-call-optimization
node: runtime.frames-eval
type: qa
source: cpython-internals
---
## Q
CPython 会对递归调用做尾调用优化（tail-call optimization）吗？这对写递归代码有什么后果？

## A
不会。CPython 的每次函数调用——包括处于尾位置、形式上等价于循环的递归调用——都会创建新的帧并压入调用栈，不会像支持 TCO 的语言那样把尾递归复用成常数栈空间的循环。用递归改写一个本可以用循环表达的算法，在 Python 里没有「变成循环」的栈空间收益，深递归反而更容易撞到递归深度限制，通常应该手动改写成循环或显式栈。
