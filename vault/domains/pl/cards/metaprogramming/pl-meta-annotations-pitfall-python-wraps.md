---
id: pl-meta-annotations-pitfall-python-wraps
node: metaprogramming.annotations-decorators
type: qa
step: 11
---
## Q
Python 装饰器会让被装饰函数丢掉什么？叠加多个装饰器时，执行顺序是怎样的？

## A
装饰器返回的是一个新函数，原函数被替换了。如果不处理，原函数的名字、文档和签名都会丢失：

```python
def timed(f):
    def wrapper(*a, **k): return f(*a, **k)
    return wrapper
# foo.__name__ -> 'wrapper', foo.__doc__ -> None
# inspect.signature(foo) -> (*a, **k)
```

真实输出：`wrapper None`，签名显示为 `(*a, **k)`。后果是：日志里所有函数都叫 `wrapper`；依赖函数名或签名的框架（Flask 的路由注册、`pytest` 的参数注入、`inspect`）行为出错或报重名。

**修复**：在 `wrapper` 上加 `@functools.wraps(f)`，它会复制 `__name__`、`__doc__`，并设置 `__wrapped__`，`inspect.signature` 会顺着它还原为 `(x: int) -> int`。

**叠加顺序**：`@tag("A")` 在上、`@tag("B")` 在下，等价于 `tag("A")(tag("B")(z))`。下面的先包，所以上面的在最外层、先执行；真实输出是 `ABz`。把鉴权和缓存叠在一起时，这个顺序决定未授权用户是否能命中缓存，写反了就是安全问题。

经验：任何装饰器的第一行都应该是 `@functools.wraps`，叠加超过两层时给每一层写一个测试，断言顺序。
