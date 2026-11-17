---
id: errors-bug-vs-failure-batch-scope
node: errors.bug-vs-failure
type: qa
step: 6
---
## Q
批量处理一千条记录，第 7 条格式有问题。是整批失败、跳过它不说，还是别的？哪些异常可以在批量里被收进结果，哪些不可以？

## A
**预期失败收进这一条的结果，缺陷不被批量吞掉**

- **一条一结果，保持输入顺序**：每条记录要么有结果，要么有 `error`，调用方能对号入座；
- **坏记录只影响自己**：后面的记录照常处理，不能因为一条格式错丢掉整批；
- **只接预期的那一类异常**：这里是 `ValueError`；`TypeError` 之类意味着我们的代码有 bug，批量不该替它遮掩；
- **缺陷被收进批量的代价**：一批全部变成“无效”，监控上只看到无效率飙高，没人知道是代码改坏了；
- **无效输入和策略拒绝分开计数**：前者上升说明上游在出问题，后者上升说明规则在起作用。

```python
def run_batch(rows, fn):
    out = []
    for row in rows:
        try:
            out.append((row, fn(row), None))
        except ValueError as e:                # 预期失败：这一条的结果是错误
            out.append((row, None, type(e).__name__))
    return out                                 # 其他异常（缺陷）不在这里接

print(run_batch(["1", "x", "3"], int))         # 中间一条是错误，两边照常
try: run_batch([None], int)
except TypeError: print("缺陷冒出来了")
```

**知识点：**缺陷与预期失败（Bugs vs Failures）
