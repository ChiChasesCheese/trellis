---
id: hi-pt-spreadsheet-engine-9-rewire
node: qb.lld.spreadsheet-engine.points
type: qa
step: 9
---
## Q
**电子表格引擎 · 改线要同步反向边**｜追问 · 出自：电子表格引擎 › 深入 2

已有 `C1==A1+B1`，现在把 `C1` 改成 `=D1`，或者清空成 `""`。引入反向边 `_users` 之后，`set` 里必须多做什么？

## A
**要点。** 先把 `C1` 从旧依赖（`A1`、`B1`）的 `_users` 里摘掉，再登记新依赖；清空时还要删值缓存，并重算 `C1` 的下游。

```python
for d in self._deps.pop(cell, set()):
    self._users[d].discard(cell)
```
**易错。** 忘了摘旧边：之后误报环，或白白多算。空格子也要允许有 `_users`，否则先写公式、后填引用就失效。
