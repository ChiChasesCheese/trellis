---
id: logging-hierarchy-effective-level-propagate
node: engineering.logging-config
type: qa
source: python-docs
---
## Q
如果只给顶层 logger（比如 `foo`）设置了级别和处理器，子 logger（比如 `foo.bar.baz`）自己什么都没配置，它记录的日志会怎么处理？

## A
logger 没有显式设置级别时，会沿着按点号分隔的父子链条一路往上找，用第一个显式设置了级别的祖先的级别作为自己的「有效级别」（effective level）——根 logger 总有一个显式级别（默认 `WARNING`）兜底。同时子 logger 产生的日志记录默认会向上传播（propagate）给所有祖先 logger 关联的处理器去处理，所以通常只需要在顶层 logger 上配置一次处理器，子 logger 不用重复配置就能生效；除非把某个 logger 的 `propagate` 属性设为 `False`。
