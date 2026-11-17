---
id: errors-retry-which-errors
node: errors.retry
type: qa
step: 1
---
## Q
调用远程服务失败以后，哪些错误值得重试？为什么不能写 `except Exception` 然后一律重试？

## A
**只重试瞬时错误，其余立刻失败**

- **瞬时错误（transient）**：超时、连接被重置、被限流（429）、服务暂时不可用（503），过一会儿同一个请求可能成功；
- **永久错误（permanent）**：参数错、没有权限、对象不存在、余额不足，再发一万次结果相同，重试只会放大负载；
- **用白名单**：列出可重试的类型，以后新冒出的异常默认不重试，宁可失败得明白；
- **别按父类放行**：`TimeoutError`、`ConnectionError` 和 `FileNotFoundError` 都是 `OSError` 的子类，`except OSError` 会把“文件不存在”也重试；
- **缺陷不该重试**：`TypeError`、`KeyError` 是我们自己的 bug，重试三次只会把一个错误变成三个。

```python
RETRYABLE = (TimeoutError, ConnectionError)          # 白名单

def retryable(exc: Exception) -> bool:
    return isinstance(exc, RETRYABLE)

print(retryable(TimeoutError()), retryable(ConnectionResetError()))   # True True
print(retryable(FileNotFoundError()), retryable(ValueError()))        # False False
print(issubclass(FileNotFoundError, OSError))        # True：所以不能整个 OSError 一起放行
```

<details class="pt"><summary>延伸</summary>

HTTP 里同理：429、502、503、504 通常可重试，其余 4xx 不可。服务端最好直接在错误码里标 `retryable`，客户端查表，不靠猜状态码。

</details>

**知识点：**重试与退避（Retry & Backoff）
