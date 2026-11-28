---
id: hi-pt-spreadsheet-engine-6-error-value
node: qb.lld.spreadsheet-engine.points
type: qa
step: 6
---
## Q
**电子表格引擎 · 出错状态是值**｜追问 · 出自：电子表格引擎 › 深入 5

重算时某个格子除以零。你让重算抛异常中断，还是另有做法？下游格子怎么办？

## A
**做法。** 把 `EvalError` 实例本身存进缓存，当作这格的值；下游读到就重新抛，下游自己也存成错误值。重算不中断。

**为什么。** 抛出去会让重算停在中途，其余下游留着旧值，表格不一致。上游改好后整条链自然恢复（错误即值）。

```python
try:
    self._val[c] = evaluate(node, self._read)
except EvalError as err:
    self._val[c] = err
```
