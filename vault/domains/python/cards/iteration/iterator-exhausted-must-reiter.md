---
id: iterator-exhausted-must-reiter
node: iteration.iterator-protocol
type: qa
source: python-docs
---
## Q
一个迭代器被 `list()` 或某次 `for` 循环耗尽后，还能重新遍历同一批数据吗？

## A
不能。iterator 协议只规定了向前的 `__next__()`，没有 reset、回退或复制方法；耗尽后再调用 `__next__()` 只会不断抛出 `StopIteration`。要再遍历一遍，必须对原始的可迭代对象重新调用 `iter()` 产生一个新的迭代器；如果手上只有那个已耗尽的迭代器本身（它就是数据源），数据就已经丢失，无法恢复。
