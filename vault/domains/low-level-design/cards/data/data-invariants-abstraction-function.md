---
id: data-invariants-abstraction-function
node: data.invariants
type: qa
step: 2
---
## Q
同一个购物车，一种实现用 `dict[sku, qty]`，另一种用 `[(sku, qty), ...]` 列表。什么是抽象函数（abstraction function）？为什么换实现，调用方不受影响？

## A
**抽象函数把内部表示映射成调用方看到的值**

- **抽象值**：调用方眼里的购物车，是“SKU 到数量”的映射；
- **抽象函数 AF**：从内部表示到抽象值的映射；`dict` 版直接就是它，`list` 版把每一行放进映射，靠不变量“SKU 不重复”保证没有冲突；
- **换实现**：只要每个公共方法在抽象值上的效果不变（`set_qty` 之后 `qty` 返回新数量），换内部表示对外不可见；
- **会出事的情况**：调用方依赖了表示本身，比如遍历顺序、直接读 `_r`；
- **相等**：两个对象的 AF 相同就应当 `==`，行顺序不同的两个 `list` 表示是同一辆购物车。

```python
class DictCart:
    def __init__(self): self._r: dict[str, int] = {}
    def set_qty(self, sku, q): self._r[sku] = q
    def qty(self, sku): return self._r.get(sku, 0)

class ListCart:                              # 不变量：sku 不重复
    def __init__(self): self._r: list[tuple[str, int]] = []
    def set_qty(self, sku, q):
        self._r = [(s, n) for s, n in self._r if s != sku] + [(sku, q)]
    def qty(self, sku): return next((n for s, n in self._r if s == sku), 0)

for c in (DictCart(), ListCart()):
    c.set_qty("a", 2); c.set_qty("a", 3); print(c.qty("a"))     # 3 3
```

**知识点：**不变量与封装（Invariants）
