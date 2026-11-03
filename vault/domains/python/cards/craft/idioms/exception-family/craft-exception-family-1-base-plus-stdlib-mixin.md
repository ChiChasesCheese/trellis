---
id: craft-exception-family-1-base-plus-stdlib-mixin
node: craft.idioms.exception-family
type: qa
step: 1
---
## Q
**异常家族 · 为什么每个模块一个基类，还要多继承 ValueError**｜写法

库里到处 `raise ValueError("数量不对")` 最省事。调用方想「只处理这个模块自己的失败」时会遇到什么问题？库存系统里的 `class InvalidQuantity(InventoryError, ValueError)` 是怎么解决的，多继承到底给调用方多了什么能力？

## A
**要点。** 异常（exception）的类型就是调用方的路由表：`except` 按类型匹配。裸 `ValueError` 无法区分「我的模块抛的」和「别处的 bug 抛的」，只好要么全吞（`except Exception`）、要么全不管。给每个模块定义一个基类（`InventoryError`），调用方只 catch 它，模块自己的 bug 仍会冒出来。再混入一个标准库异常，则让只认 `ValueError` / `LookupError` 的既有代码继续有效。

```python
class InventoryError(Exception):
    """模块的所有失败都继承它：调用方可以只 catch 这一个。"""

class InvalidQuantity(InventoryError, ValueError):
    """同时是 ValueError：只认标准库异常的旧代码继续工作。"""

class UnknownReservation(InventoryError, LookupError):
    """同时是 LookupError：和「找不到」这一类的 except 保持一致。"""

stock = {1: "a"}

def reserve(qty: int):
    if qty <= 0:
        raise InvalidQuantity(qty)
    return stock[qty]                # qty=5 时 KeyError：模块自己的 bug，不是业务错误

def call(qty, handler):
    try:
        reserve(qty)
    except handler as e:
        return f"{handler.__name__} 接住了 {type(e).__name__}"
    except Exception as e:
        return f"漏出去: {type(e).__name__}"

print(call(0, InventoryError))      # 只 catch 本模块的错误
print(call(0, ValueError))          # 旧代码按 ValueError 处理仍然有效
print(call(5, InventoryError))      # 模块自己的 bug 不会被误当成业务错误吞掉
print(call(5, Exception))           # 光秃秃的 ValueError 做不到这一点：要么全吞要么全不吞
```

实际输出：

```
InventoryError 接住了 InvalidQuantity
ValueError 接住了 InvalidQuantity
漏出去: KeyError
Exception 接住了 KeyError
```

**为什么。** 基类解决「谁抛的」，混入解决「属于哪一类」：两个维度各自独立，类型层次不用二选一。

**代价。** 多继承只混入语义确实对得上的一类：数量非法是 `ValueError`，找不到是 `LookupError`，业务规则（库存不足）不属于任何标准类，就只继承基类。混入 `KeyError` 有额外的坑，见第 4 张卡。
