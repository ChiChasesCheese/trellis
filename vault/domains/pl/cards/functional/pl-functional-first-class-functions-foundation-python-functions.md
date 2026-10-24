---
id: pl-functional-first-class-functions-foundation-python-functions
node: functional.first-class-functions
type: qa
step: 5
---
## Q
Python 里的函数是什么样的对象？`lambda` 为什么被限制成一个表达式？

## A
Python 里 `def` 和 `lambda` 都创建**函数对象**：它有 `__code__`（字节码）、`__closure__`（捕获的变量）、`__name__`、`__defaults__` 等属性，可以像其他对象一样被赋值、传递、放进字典。任何实现了 `__call__` 的对象都是可调用的（`callable(x)` 为真）。

```python
def mk(k):
    def f(x): return x + k
    return f
f = mk(7)
f.__code__.co_freevars        # ('k',)
f.__closure__[0].cell_contents  # 7
(lambda: 1).__name__          # '<lambda>'
```

`lambda` 只能写**一个表达式**，不能包含语句（赋值、`return`、`for`）。`eval("lambda x: (y = x)")` 是语法错误。这是 Python 的有意设计：语言的语句与表达式严格分开，缩进驱动的块结构里放不下多行 lambda；要写多行就用 `def`，给它一个名字。副作用是：`lambda` 在回溯里显示成 `<lambda>`，没有名字，调试困难。

Python 的社区风格也因此偏向 **推导式和生成器表达式**，而不是 `map(lambda ...)`：`[x*2 for x in xs if x > 0]` 比 `list(map(lambda x: x*2, filter(lambda x: x > 0, xs)))` 更清晰，也更快。`lambda` 的主要使用场景缩小到短小的键函数：`sorted(xs, key=lambda p: p.age)`。

Python 的函数是动态对象，没有静态函数类型，类型注解用 `Callable[[int], int]` 描述，只供检查器使用。
