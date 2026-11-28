---
id: mlp-traps-py-defaults
node: traps.python-output
type: qa
step: 1
---
## Q
**可变默认参数与循环里的闭包**｜语言陷阱与读代码

下面的 Python 代码输出什么？

```python
def add(x, bag=[]):
    bag.append(x)
    return bag
print(add(1), add(2))
fs = [lambda: i for i in range(3)]
print([f() for f in fs])
gs = [lambda i=i: i for i in range(3)]
print([g() for g in gs])
```

## A
**输出。**
```
[1, 2] [1, 2]
[2, 2, 2]
[0, 1, 2]
```

- **默认参数只在定义函数时求值一次：** `bag=[]` 创建的那个列表被所有调用共用，第二次调用往同一个列表里加，所以两次返回的是同一个列表，打印出来都是 `[1, 2]`（`print` 在两次调用都完成后才打印）。
- **闭包捕获的是变量，不是值：** 三个 lambda 都引用同一个变量 `i`；等到调用时循环早已结束，`i` 是 2，所以全是 2。这叫晚绑定（late binding）。
- **修法：** 用默认参数在定义时固定当前值（`lambda i=i: i`），或者用 `functools.partial`。
- **默认参数的修法：** 默认值写 `None`，函数里 `if bag is None: bag = []`。
- **记住：** 默认值不要用可变对象；闭包要的是定义时的值就绑定它。

**英文答法。**
- "The default is evaluated **once**, at definition time, so every call shares the same list."
- "The lambdas capture the **variable**, not its value; I'd bind it with a default argument."
