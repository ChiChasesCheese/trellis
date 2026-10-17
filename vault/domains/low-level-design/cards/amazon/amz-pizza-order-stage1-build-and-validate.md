---
id: amz-pizza-order-stage1-build-and-validate
node: amazon.amz-pizza-order
type: qa
step: 3
tags: [grown]
---
## Q
在披萨订单里，`PizzaBuilder.build()` 的校验和定价主流程怎么写？

## A
先逐项校验（尺寸 → 饼底及其适用尺寸 → 配料去重、数量、存在、互斥），任何一步失败就抛带原因的异常，全部通过才定价并返回不可变的 `Pizza`。

```python
def build(self) -> Pizza:
    m, size = self._menu, self._size
    if size not in m.base:
        raise InvalidChoiceError(f"未知尺寸: {size!r}")
    spec = m.crusts.get(self._crust)
    if spec is None or (spec.sizes and size not in spec.sizes):
        raise InvalidChoiceError(f"{size} 号做不了 {self._crust}")
    tops = tuple(sorted(self._toppings))
    if len(set(tops)) != len(tops) or len(tops) > m.max_toppings:
        raise InvalidChoiceError("配料重复或超限")
    for t in tops:
        if t not in m.toppings or m.toppings[t].excludes & set(tops):
            raise InvalidChoiceError(f"配料不合法: {t}")
    return Pizza(size, self._crust, tops, m.price(size, self._crust, tops))
```
