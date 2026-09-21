---
id: generator-is-one-shot-cannot-restart
node: iteration.generators
type: qa
source: cpython-internals
---
## Q
一个生成器对象被完整遍历一次（耗尽）之后，能不能重新 `for` 一遍拿到同样的序列？

## A
不能。生成器耗尽意味着它内嵌的帧已经执行到函数体末尾并抛出 `StopIteration`，之后每次 `__next__()` 都会立刻再次抛出 `StopIteration`，帧本身也可能已被清理，没有「倒带」的机制。要再拿一遍同样的序列，必须重新调用生成器函数（如再次执行 `gen(3)`）创建一个全新的生成器对象。
