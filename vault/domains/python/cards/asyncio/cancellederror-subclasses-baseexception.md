---
id: cancellederror-subclasses-baseexception
node: asyncio.cancellation
type: qa
source: python-docs
---
## Q
`asyncio.CancelledError` 直接继承自 `Exception` 还是 `BaseException`？这个继承关系有什么实际意义？

## A
直接继承自 `BaseException`（不是 `Exception`），所以像 `except Exception:` 这种宽泛的异常捕获不会意外吞掉取消信号——这是设计上刻意为之，保证「取消」这类控制流信号不会被业务代码的普通异常处理逻辑误伤。
