---
id: quality-mutable-default-argument
node: quality.smells
type: qa
step: 4
---
## Q
```python
def add_item(item, cart=[]):
    cart.append(item)
    return cart
```
连续两次不传 `cart` 调用 `add_item`，第二次的结果里会包含第一次的 `item`。为什么，怎么修？

## A
函数的默认参数值在**定义函数的时候**只被求值一次，而不是每次调用都重新创建；`cart=[]` 创建的这个列表对象被绑定在函数对象上，之后每次省略 `cart` 的调用都复用同一个列表，于是上一次调用的修改会残留到下一次调用里——这是 Python 独有的坑，不是"忘了拷贝"的偶然失误，而是语言规则本身的必然结果。

```python
def add_item(item, cart=None):
    if cart is None:
        cart = []
    cart.append(item)
    return cart
```
规则：可变类型（`list`、`dict`、`set`，以及任何可变的自定义对象）永远不要直接作为默认参数值，用 `None` 作哨兵、在函数体内部创建新实例；不可变类型（`str`、`int`、元组）没有这个问题，因为它们不可能被"残留的修改"污染。
