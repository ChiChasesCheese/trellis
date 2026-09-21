---
id: for-loop-iter-next-desugar
node: iteration.iterator-protocol
type: qa
source: python-docs
---
## Q
`for x in obj:` 在底层展开成什么调用序列，为什么同一个 list 能被多个 `for` 循环各自完整遍历一遍？

## A
等价于先 `it = iter(obj)` 得到一个迭代器，再反复调用 `it.__next__()`，遇到 `StopIteration` 就静默结束循环。list 本身只是 iterable（可迭代对象），不保存遍历位置；每次 `for` 循环都会重新对它调用 `iter()`，产出一个全新的、独立的迭代器实例，所以多个循环互不干扰。
