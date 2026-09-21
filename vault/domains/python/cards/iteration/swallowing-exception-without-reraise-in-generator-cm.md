---
id: swallowing-exception-without-reraise-in-generator-cm
node: iteration.context-managers
type: qa
source: python-docs
---
## Q
用 `@contextmanager` 写的上下文管理器如果用 `except` 捕获了 `with` 块抛出的异常、只打了条日志就没有再 `raise`，会发生什么？

## A
这等同于对应的 `__exit__()` 返回了真值：`with` 语句会认为异常已经被处理，转而正常吞掉这个异常继续往下执行，调用方完全感知不到刚才出过错。如果只是想记录异常而不是吞掉它，生成器里捕获后必须显式重新 `raise`，否则会制造一个异常悄悄消失的隐蔽 bug。
