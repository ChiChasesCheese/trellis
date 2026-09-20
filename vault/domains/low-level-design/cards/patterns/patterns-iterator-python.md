---
id: patterns-iterator-python
node: patterns.behavioral
type: qa
step: 1
---
## Q
Python 里为什么很少需要手写一个带 `__iter__` / `__next__` 的 Iterator 类？

## A
生成器函数（用 `yield`）已经自动实现了迭代器协议——写一个普通函数、用 `yield` 逐个产出元素，Python 自动帮你管理"当前遍历到哪了"这份状态，不需要手动维护游标字段、手动抛 `StopIteration`。只有当遍历逻辑必须暴露成一个能被到处传递、能重复查询进度的对象（而不是一次性消耗的生成器）时，才值得手写类。

```python
def in_order(node):
    if node is None:
        return
    yield from in_order(node.left)
    yield node.value
    yield from in_order(node.right)
```
