---
id: mlp-coding-pc03-followups
node: coding.pc03
step: 2
type: qa
---
## Q
**装饰器：追问与变体**｜编程轮

写完几个装饰器后，面试官常问"这个实现有什么局限""为什么这样放状态"。有哪些追问？

## A
- **为什么要 `functools.wraps`：** 不加的话，被装饰函数的 `__name__` 变成 `wrapper`、文档字符串丢失；叠多个装饰器或做运行时内省时会出错。
- **`@retry` 比 `@timed` 多一层的原因：** `@timed` 是 `func = timed(func)`；`@retry(3)` 先执行 `retry(3)` 得到装饰器，再用它包函数，所以是工厂、装饰器、wrapper 三层。看 `@` 后面有没有括号就能区分。
- **`memoize` 的局限：** 缓存键是调用的形状，不是绑定后的签名，`f(5)`、`f(5, 0)`、`f(5, b=0)` 即使结果相同也是三个缓存条目；参数必须可哈希；缓存只增不减，长期运行会占满内存，需要上限（如 `functools.lru_cache(maxsize=...)`）。
- **状态放哪一层：** 每装饰一个函数就新建一份状态（闭包里建 `cache`、`calls`），不要放模块全局或可变默认参数，否则所有被装饰的函数共用一个缓存或一个限流窗口。
- **用类写带状态的装饰器：** 状态放实例属性，`__call__` 里处理调用，用 `functools.update_wrapper(self, func)` 保留元数据：

```python
class Counted:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func, self.calls = func, 0
    def __call__(self, *args, **kwargs):
        self.calls += 1
        return self.func(*args, **kwargs)
```

- **指数退避：** `backoff` 可以是函数，`sleep(backoff(attempt))`，例如 `lambda a: 0.1 * 2 ** a`。
- **会多花一个测试用例的边界：** `times=0` 或 `n<1` 在装饰时抛 `ValueError`；不在 `exceptions` 里的异常第一次就冒泡；窗口边界（刚好过了 `per_seconds` 的那次调用应该放行）；两个被装饰的函数互不影响。

**英文答法。**
- "Without `functools.wraps` the function's **name and docstring** are lost."
- "State lives in the **closure**, one copy per decorated function, never in a global."
- "This `memoize` keys on the **call shape**, so it needs hashable arguments and has no size bound."
