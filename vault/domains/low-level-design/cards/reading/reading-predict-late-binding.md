---
id: reading-predict-late-binding
node: reading.predict-behaviour
type: qa
step: 4
---
## Q
`funcs = [lambda: i for i in range(3)]`，然后依次调用每个函数，打印什么？为什么？怎么让它们各自记住自己的 `i`？

## A
**闭包捕获的是变量，不是当时的值：调用时才读，那时循环已经结束**

- **三个 lambda 共用同一个变量 `i`**：推导式里每轮只是给同一个名字重新赋值；
- **调用发生在循环之后**：`i` 停在最后的值 2，三个函数都返回 2；
- **用默认参数固定当前值**：`lambda i=i: i`，默认值在 lambda 创建的那一刻求值（上一张卡的机制反过来用）；
- **或用 `functools.partial`**：把参数绑进去，也不依赖外层变量；
- **推演提示**：看到闭包，就问“它引用的变量在被调用时是什么值”；延迟执行（回调、线程、生成器）里最容易踩。

```python
from functools import partial

bad = [lambda: i for i in range(3)]
print([f() for f in bad])          # [2, 2, 2]

good = [lambda i=i: i for i in range(3)]
print([f() for f in good])         # [0, 1, 2]

show = lambda i: i
print([partial(show, i)() for i in range(3)])   # [0, 1, 2]
```

**知识点：**预测输出与副作用（Predicting Behaviour）
