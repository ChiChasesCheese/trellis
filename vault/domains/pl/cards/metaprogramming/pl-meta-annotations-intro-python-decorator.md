---
id: pl-meta-annotations-intro-python-decorator
node: metaprogramming.annotations-decorators
type: qa
step: 3
---
## Q
Python 的装饰器（decorator）是什么？`@timed` 这一行背后到底发生了什么，一个小场景里它怎样工作？

## A
**前提**：Python 的函数是对象，可以当参数传、当返回值返回，也可以在函数里定义函数。这些性质叫一等函数（first-class function），装饰器就建立在它上面。

**是什么**：装饰器是一个「接收函数、返回函数」的函数。在 `def` 上方写 `@timed`，等价于定义完函数之后立刻执行 `slow = timed(slow)`，名字 `slow` 从此指向 `timed` 返回的新函数。

**心智模型**：给函数套一层外壳。外壳里能在调用前后做事，再调用原函数，它「记得」原函数是因为闭包（closure，内层函数能访问外层函数的局部变量）。

```python
def timed(f):
    def wrapper(*args):
        t = time.perf_counter()
        r = f(*args)
        print(f"{f.__name__} took {(time.perf_counter()-t)*1e3:.1f} ms")
        return r
    return wrapper

@timed
def slow(n): return sum(range(n))
```

调用 `slow(5_000_000)` 的真实输出：`slow took 22.1 ms`（一次本机测量），然后是求和结果 `12499997500000`。`slow` 的调用方没有改动，但每次调用都被计时了。

**要记住的一点**：装饰器在函数定义时执行一次（模块导入时），不是在每次调用时；它能做缓存、重试、鉴权、注册路由（Flask 的 `@app.route`）。`@d` 只是语法糖，你完全可以手写 `slow = timed(slow)`，没有任何隐藏机制。
