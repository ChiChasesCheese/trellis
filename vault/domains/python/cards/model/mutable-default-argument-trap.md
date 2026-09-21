---
id: mutable-default-argument-trap
node: model.mutability
type: qa
source: python-docs
---
## Q
```python
def append_item(item, acc=[]):
    acc.append(item)
    return acc
```
依次调用 `append_item(1)`、`append_item(2)`，为什么结果是 `[1, 2]` 而不是各自独立的 `[1]`、`[2]`？应该怎么改？

## A
函数的默认参数值只在函数定义（def）被执行时求值一次，之后每次调用省略该参数都复用这同一个预先算好的对象；`[]` 是可变对象，`acc.append(item)` 就地修改的是被所有调用共享的同一个 list，所以修改会跨调用累积。正确写法是用 `acc=None` 占位，在函数体内 `if acc is None: acc = []`，让每次调用都拿到独立的新对象。
