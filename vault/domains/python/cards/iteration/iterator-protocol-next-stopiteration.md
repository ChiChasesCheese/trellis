---
id: iterator-protocol-next-stopiteration
node: iteration.iterator-protocol
type: qa
source: python-docs
---
## Q
一个对象要满足 iterator（迭代器）协议，必须实现什么方法？各自的职责是什么？

## A
必须实现无参的 `__next__()`：每次调用返回流中的下一个元素；元素耗尽时必须抛出 `StopIteration` 异常，不能返回 None 或其他哨兵值。惯例上迭代器还会实现返回自身的 `__iter__()`，这样迭代器自身也满足 iterable（可迭代对象）协议，可以直接放进 `for` 循环。
