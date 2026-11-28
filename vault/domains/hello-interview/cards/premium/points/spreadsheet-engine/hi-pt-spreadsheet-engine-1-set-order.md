---
id: hi-pt-spreadsheet-engine-1-set-order
node: qb.lld.spreadsheet-engine.points
type: qa
step: 1
---
## Q
**电子表格引擎 · set 的执行顺序**｜必会 · 出自：电子表格引擎 › 整体设计

`set(cell, raw)` 里有四件事：校验格子名、解析公式、检查是否成环、写入表格。顺序怎么排，为什么？

## A
**要点。** 校验格子名 → `parse_raw` 解析 → `_reaches` 查环 → 最后才写 `_node`（格子到语法树）和 `_deps`（格子读了谁）。

**为什么。** 所有可能失败的步骤都排在任何写入之前，失败时表格原样；边写边检查的版本要手工回滚边表和缓存，漏一处就留下脏状态（校验在先、提交在后）。

```python
node = parse_raw(raw)                         # 1. 先解析：写错了表格没动过
deps = refs_of(node) if node else set()
if self._reaches(deps, cell):                 # 2. 再查环：仍然没动过
    raise CycleError(f"{cell} would depend on itself")
```
