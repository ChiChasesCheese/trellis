---
id: py-out-scope-nonlocal
node: output.scope
type: qa
step: 3
---
## Q
**内层赋值**｜读代码说输出

```python
def outer():
    n = 0
    def a():
        n = 1
    def b():
        nonlocal n
        n = 2
    a(); print(n)
    b(); print(n)
outer()
```

输出什么？

## A
**输出。**

```
0
2
```

**为什么。**

- `a` 里的 `n = 1` 创建了 `a` 自己的局部变量，外层的 `n` 没动，所以第一次打印 0。
- `b` 用 `nonlocal n` 声明：这个名字指向最近一层外围函数的 `n`，赋值改的就是外层那个变量，所以打印 2。
- 只读外层变量不需要任何声明，只有赋值才需要。

**语言为什么这样设计。**

- 赋值默认建局部，是为了让一个函数不会因为不小心写了同名变量而改掉外面的状态；`nonlocal` 由 PEP 3104 在 Python 3.0 加入，之前内层函数根本没法改外层的绑定。
- JavaScript 靠 `let` / `const` 显式声明，赋值沿作用域链找到已声明的那个；Python 把「声明」藏进赋值，所以才需要这两个关键字补出口。

**怎么写才对。**

```python
# 状态多时用对象，不用 nonlocal 堆变量
class Counter:
    def __init__(self): self.n = 0
    def inc(self): self.n += 1
```

**面试里一句话。**

Without nonlocal, an assignment in an inner function creates a new local; nonlocal rebinds the nearest enclosing function's variable.
