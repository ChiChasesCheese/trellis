---
id: logging-getlogger-name-convention
node: engineering.logging-config
type: qa
source: python-docs
---
## Q
每个模块开头写 `logger = logging.getLogger(__name__)`，这样做的好处是什么？

## A
`__name__` 就是当前模块的完整点分路径（如 `mypkg.sub.mod`），logging 的 logger 名字本身就是用点号分隔的层级命名空间；用 `__name__` 作为 logger 名字，logger 的层级结构就自动和代码的包/模块结构一致。这样从日志输出里的 logger 名字就能立刻看出事件来自哪个模块，也能针对某个子包单独调整日志级别或加处理器（handler），而不必给每个 logger 手写一个名字。
