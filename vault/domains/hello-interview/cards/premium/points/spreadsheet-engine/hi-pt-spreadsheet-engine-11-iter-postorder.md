---
id: hi-pt-spreadsheet-engine-11-iter-postorder
node: qb.lld.spreadsheet-engine.points
type: qa
step: 11
---
## Q
**电子表格引擎 · 迭代后序遍历**｜加分 · 出自：电子表格引擎 › 逐步扩展 4

在一条 5,000 格的引用链上改源头，递归的后序遍历会怎样？怎么在不改其余逻辑的前提下改成迭代？

## A
**现象。** Python 默认递归深度约 1000，实测直接 `RecursionError`。

**做法。** 手写栈，栈里放 `(格子, 下游迭代器)`；迭代器耗尽（`for ... else`）才轮到自己入表，仍是后序。

```python
stack = [(changed, iter(self._users.get(changed, ())))]
while stack:
    c, users = stack[-1]
    for u in users:
        if u not in seen:
            seen.add(u)
            stack.append((u, iter(self._users.get(u, ()))))
            break
    else:
        order.append(c)
        stack.pop()
```
