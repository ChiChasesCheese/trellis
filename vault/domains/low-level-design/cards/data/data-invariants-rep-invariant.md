---
id: data-invariants-rep-invariant
node: data.invariants
type: qa
step: 1
---
## Q
类的表示不变量（representation invariant）是什么？以购物车为例，它怎么写下来、在什么时候成立？

## A
**不变量：每个公共方法前后都成立的条件**

- **表示不变量**：对内部字段的约束，如“每行数量是大于 0 的 `int`”“同一商品只有一行”；
- **成立的时刻**：构造完成后、每个公共方法返回时；方法中途可以暂时破坏；
- **写下来**：docstring 一句话，再配一个 `_check_rep()`，开发和测试时调用；
- **价值**：每个方法只需证明“假设入口时成立，返回时仍成立”，不必推演整段历史；出了问题，范围缩到破坏它的那个方法。

```python
class Cart:
    """Rep invariant: every quantity in _lines is an int > 0."""
    def __init__(self):
        self._lines: dict[str, int] = {}
    def _check_rep(self):
        assert all(type(q) is int and q > 0 for q in self._lines.values())
    def set_qty(self, sku: str, qty: int):
        if type(qty) is not int or qty < 0:
            raise ValueError("qty")
        if qty == 0:
            self._lines.pop(sku, None)       # 0 不入库
        else:
            self._lines[sku] = qty
        self._check_rep()
```

**知识点：**不变量与封装（Invariants）
