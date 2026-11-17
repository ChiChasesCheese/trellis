---
id: errors-bug-vs-failure-invariant-raise
node: errors.bug-vs-failure
type: qa
step: 4
---
## Q
按比例分摊一笔应收款，最后检查“各份之和等于总额”。这条检查失败了，应该返回错误码、用 `assert`，还是抛异常？

## A
**输入错是失败，守恒破坏是缺陷：显式 `raise` 具名异常**

- **入口先拦外部造成的错**：总额为负、权重为零或负，是调用方的错，抛 `ValueError`，合同里有；
- **守恒检查是缺陷检测**：入口都拦过了还对不上，就是我们的算法错了，不能带着错账继续；
- **涉及钱的不变量不用 `assert`**：`-O` 一开检查就没了，错账悄悄入库；用 `raise RuntimeError`；
- **缺陷不翻译成错误码返回**：返回一个“分摊失败”会被调用方当成预期情况处理，掩盖问题；让它崩，由顶层记录；
- **这条检查平时永远不触发**，它的价值是在算法被改坏的那一天立刻失败。

```python
def split(total: int, weights: list[int]) -> list[int]:
    if total < 0 or not weights or min(weights) <= 0:
        raise ValueError("invalid input")          # 预期失败：调用方的错
    parts = [total * w // sum(weights) for w in weights]
    parts[0] += total - sum(parts)                 # 整除剩下的零头给第一份
    if sum(parts) != total:
        raise RuntimeError("conservation broken")  # 缺陷：显式 raise，不用 assert
    return parts

print(split(100, [1, 1, 1]))                       # [34, 33, 33]
```

**知识点：**缺陷与预期失败（Bugs vs Failures）
