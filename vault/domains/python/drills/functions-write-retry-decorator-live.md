---
nodes: [functions.decorator-patterns, functions.decorators, functions.functools, functions.scope-closure]
tags: [drill, interview]
---
# Drill：现场写一个 `@retry(times, exceptions, backoff)` 装饰器

面试官要求你现场写一个通用的重试装饰器，可以直接用在任意函数或类方法上：

```python
@retry(times=3, exceptions=(TimeoutError,), backoff=lambda n: 0.1 * n)
def call_flaky_api(...): ...
```

**限制与要求**
- 15 分钟内写出能跑的版本，不许查文档；`functools` 之外不许用第三方库。
- 必须保留被装饰函数的元数据（`__name__`、`__doc__`）。
- 必须支持装饰实例方法（`self` 要正确传给原函数）。
- 必须让「休眠函数」可注入，写完之后要能在测试里秒级跑完整个重试流程。
- 先说结论（三层嵌套结构），再写代码，不要边想边写。

**分关要求**（一关做完再看下一关）
- 第 1 关（约 8 分钟）：写出装饰器本体，覆盖上面四条限制。
- 第 2 关（约 4 分钟）：装饰一个类的实例方法，验证 `self` 正确传递；说明如果用「带 `__call__` 的类」实现装饰器，为什么装饰方法时 `self` 会丢失。
- 第 3 关（约 3 分钟）：追问——`@lru_cache` 叠在 `@retry` 外层还是内层，对「重试失败后再成功」的调用结果有什么不同？给一个用 `for` 循环批量生成多个 retry 包装函数导致「迟绑定」出 bug 的例子。

**评分点（强答案会命中）**
- 除了重试次数，必须能配置「只重试哪些异常类型」和「退避策略」，否则会把编程错误也悄悄重试掉，或对故障下游造成二次冲击 [[retry-decorator-design-requirements]]
- 用 `functools.wraps` 保留元数据；不加的话 `__name__`/`__doc__` 变成 `wrapper` 自己的，调试和按函数名做路由/缓存的上层逻辑会出错 [[functools-wraps-preserves-metadata]] [[missing-wraps-failure-mode]]
- 带参数的装饰器要嵌套三层：外层接收 `times`/`exceptions`/`backoff`，中间层接收 `func`，最内层 `wrapper(*args, **kwargs)` 执行重试循环再转发调用 [[parameterized-decorator-three-layers]] [[decorator-factory-expansion]]
- 用带 `__call__` 但没有 `__get__` 的类实现装饰器时，`obj.method` 拿到的是装饰器实例本身而不会自动绑定 `self`，因为它没有实现描述符协议 [[class-decorator-loses-self-binding]]
- 把 `sleep`/取时间的函数做成装饰器的可选参数（默认 `time.sleep`），测试时注入假时钟或立即返回，才能确定性、毫秒级跑完重试逻辑 [[decorator-testability-inject-clock]]
- 叠放多个装饰器时离 `def` 最近的先包一层：`@lru_cache` `@retry` 等价于 `f = lru_cache(retry(f))`，缓存包在最外层，会把「重试失败又成功」的最终结果按参数缓存下来；调换顺序则每次调用都重新走一遍重试逻辑 [[decorator-stacking-order]]
- `lru_cache` 要求所有参数可哈希，叠加时传进去的参数不能是 list/dict 这类不可哈希对象 [[lru-cache-requires-hashable-args]]
- `for` 循环里用同一个自由变量批量生成闭包时，闭包捕获的是变量本身而不是当时的值，调用时才去外层读取当前值，所以全部返回最后一次迭代的结果 [[loop-closure-late-binding-trap]]

**参考答案**
第 1 关：

```python
import functools
import time

def retry(times, exceptions=(Exception,), backoff=lambda n: 0, sleep=time.sleep):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times:
                        raise
                    sleep(backoff(attempt))
        return wrapper
    return decorator
```

三层结构对应「装饰器参数→真正的装饰器→wrapper」；`func(*args, **kwargs)` 里的 `*args` 第一个元素天然就是实例方法的 `self`，因为函数式装饰器包的是未绑定的函数本身，Python 的描述符协议在 `instance.method` 时才把它转成绑定方法，`self` 的传递不受装饰器影响。

第 2 关：如果改成 `class retry: def __call__(self, func): ...` 这种类装饰器且不实现 `__get__`，装饰实例方法后 `obj.method(x)` 会变成调用「装饰器实例.`__call__`(x)」，`self`（也就是 `obj`）不会被自动传入，需要额外实现 `__get__` 做绑定。

第 3 关：`@lru_cache` `@retry` 展开为 `f = lru_cache(retry(f))`——`retry(f)` 先生成带重试的 `wrapper`，`lru_cache` 包在它外面；调用时先查缓存，缓存未命中才真正跑一遍完整的重试循环，命中之后的调用不会再触发任何重试或 sleep。若把顺序换成 `@retry` `@lru_cache`，则是每次尝试都各自查一次内层缓存，重试之间会互相利用缓存，语义完全不同。迟绑定的例子：`decorators = [retry(times=n) for n in range(1, 4)]` 若写成 `[lambda: retry(times=n) for n in range(1, 4)]` 再统一调用，所有 lambda 里的 `n` 都会读到循环结束时的最后一个值，需要 `lambda n=n: retry(times=n)` 或工厂函数固定住。

**尝试记录**
| 日期 | 用时 | 卡在哪 | 下次 |
|---|---|---|---|
