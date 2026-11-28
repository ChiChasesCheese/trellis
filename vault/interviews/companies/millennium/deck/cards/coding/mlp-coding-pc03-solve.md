---
id: mlp-coding-pc03-solve
node: coding.pc03
step: 1
type: qa
---
## Q
**装饰器：题与解**｜编程轮

写几个装饰器：`@timed` 记录每次调用耗时，`@memoize` 缓存算过的结果，`@retry(times=3)` 失败时自动重试，最后一个带状态的 `@rate_limited(n, per_seconds)` 限制函数在时间窗口内最多被调用 n 次。

## A
**一句话思路。** 装饰器 `@f` 等价于 `func = f(func)`：裸装饰器是"函数包函数"；带参数的 `@retry(3)` 要多一层，先 `retry(3)` 返回真正的装饰器；需要记状态时，状态放在闭包变量或装饰器实例上，而不是全局。

```python
import functools, time
from collections import deque

def memoize(func):
    cache = {}                                       # 状态放闭包：每个被装饰的函数各有一份
    @functools.wraps(func)                           # 保留 __name__、__doc__
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))  # 参数必须可哈希
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        wrapper.last_seconds = time.perf_counter() - start   # 每次调用都刷新
        return result
    return wrapper

def retry(times, exceptions=(Exception,), backoff=0, sleep=lambda s: None):
    if times < 1:
        raise ValueError("times must be >= 1")       # 装饰时就报错，不等到调用
    def decorator(func):                             # 多出来的这一层：真正的装饰器
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:                   # 只重试指定类型，其他异常直接冒泡
                    if attempt == times:
                        raise                        # 次数用完，抛出最后一次的原异常
                    sleep(backoff)                   # sleep 注入：测试不用真等
        return wrapper
    return decorator

class RateLimitExceeded(Exception):
    pass

def rate_limited(n, per_seconds, clock=time.monotonic):
    def decorator(func):
        calls = deque()                              # 最近 per_seconds 内的调用时间戳
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = clock()
            while calls and now - calls[0] >= per_seconds:
                calls.popleft()                      # 惰性淘汰：下一次调用时才清理
            if len(calls) >= n:
                raise RateLimitExceeded()
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

t = [0.0]
f = rate_limited(2, 10, clock=lambda: t[0])(lambda: "ok")
out = []
for now in (0, 1, 2, 10):
    t[0] = now
    try:
        out.append(f())
    except RateLimitExceeded:
        out.append("limited")
print(out)   # ['ok', 'ok', 'limited', 'ok']
```

**复杂度。** `memoize` 查询均摊 O(1)，空间随不同参数增长；`rate_limited` 每次调用均摊 O(1)，空间 O(n)。

**边写边讲。**
- "`@retry(times=3)` calls `retry(3)` first, so I need **one extra layer**: factory, decorator, wrapper."
- "I validate `times` at **decoration time**, because that is a configuration error."
- "I **inject** `sleep` and `clock`, so tests are deterministic and never really wait."
