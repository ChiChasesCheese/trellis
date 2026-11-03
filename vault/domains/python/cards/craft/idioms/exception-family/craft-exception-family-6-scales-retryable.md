---
id: craft-exception-family-6-scales-retryable
node: craft.idioms.exception-family
type: qa
step: 6
---
## Q
**异常家族 · 从异常类层次到 4xx / 5xx 错误码**｜写法

进程内，调用方靠异常类型决定怎么办。服务跨网络后，异常对象过不去，只剩状态码和一段 JSON。同一套「可重试 / 不可重试」的分类要怎么搬过去？

## A
**要点。** 进程内，异常类层次就是分类：`except Unavailable` 重试，`except BadRequest` 直接报错。跨网络，类层次变成**协议里的错误码**，并且必须显式声明「能不能重试」，因为客户端看不到服务端的类。4xx（请求本身有问题）不可重试，重试一百次结果相同；5xx 与 429（限流）可以退避后重试。

```python
class ApiError(Exception):
    retryable = False                 # 类属性：是否值得再试，由异常类型自己声明

class BadRequest(ApiError):           # 4xx：同样的请求再发一百次也一样失败
    pass

class Unavailable(ApiError):          # 5xx / 429：等一会儿可能就好
    retryable = True

def call_with_retry(fn, attempts: int = 3):
    for i in range(1, attempts + 1):
        try:
            return fn()
        except ApiError as e:
            if not e.retryable or i == attempts:
                raise                  # 不可重试的立刻抛，重试用尽也抛
            print(f"  第 {i} 次失败 ({type(e).__name__})，重试")

calls = iter([Unavailable(), Unavailable(), "ok"])
def flaky():
    r = next(calls)
    if isinstance(r, Exception):
        raise r
    return r

print("服务暂时不可用:", call_with_retry(flaky))
try:
    call_with_retry(lambda: (_ for _ in ()).throw(BadRequest("amount<=0")))
except BadRequest as e:
    print("BadRequest 不重试，直接抛出:", e)
```

实际输出：

```
  第 1 次失败 (Unavailable)，重试
  第 2 次失败 (Unavailable)，重试
服务暂时不可用: ok
BadRequest 不重试，直接抛出: amount<=0
```

**变化。** 重试安全的前提是操作幂等（见幂等键）：对 5xx 重试时，服务端可能其实已经执行了。所以「可重试」这个标签只有配上幂等键才成立。

**代价。** 把 409 之类「稍后再试可能成功」的冲突与 4xx 混为一谈，客户端会放弃本可成功的请求；把 5xx 全当可重试，会在故障时放大流量。

**信号。** 一个模块的失败需要被调用方分流处理，而不是统一报错。
