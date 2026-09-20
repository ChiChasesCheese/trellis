---
id: problems-logger-filter-is-a-plain-function
node: problems.components.logger
type: qa
step: 9
tags: [grown]
---
## Q
日志框架要支持"把 `/healthz` 健康检查的访问日志扔掉"这类规则，而且加规则时不许改动 logger 的任何代码。在 Python 里，过滤器该定义成一个抽象基类（`class Filter(ABC)`）还是一个函数类型？

## A
函数类型：`Filter = Callable[[LogRecord], bool]`，handler 上存一个过滤器元组，全部返回真才放行。

```python
handler.add_filter(lambda r: r.context.get("path") != "/healthz")
```

一个只有一个方法、没有共享实现、多数情况下连状态都没有的接口，在 Python 里就是一个函数——为它写抽象基类只是把 Java 的写法搬过来。需要带状态时（"同一条消息一分钟内只放行一次"），闭包或者一个带 `__call__` 的类照样满足这个类型，调用方一行都不用改。这也是这个设计"可扩展"的证据：加过滤器只动 handler，logger、formatter、记录结构全都不碰。
