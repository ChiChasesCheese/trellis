---
id: hi-pt-spreadsheet-engine-5-inject-read
node: qb.lld.spreadsheet-engine.points
type: qa
step: 5
---
## Q
**电子表格引擎 · 求值函数注入 read**｜追问 · 出自：电子表格引擎 › 深入 4

惰性求值和缓存求值用同一个 `evaluate`，不改解析也不改求值函数。签名上做了什么设计？

## A
**要点。** `evaluate(node, read)` 把"怎么读格子"作为函数参数传入，求值函数不知道格子存在哪里（依赖注入，传函数）。

```python
def evaluate(node: Node, read: Callable[[str], float | None]) -> float:
    match node:
        case Ref(cell):
            v = read(cell)
            return 0.0 if v is None else v
```
**对比。** 求值里直接写 `self._val[cell]`，惰性与缓存就得各写一套，换策略要改求值函数。
