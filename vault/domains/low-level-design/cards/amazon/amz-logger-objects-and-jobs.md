---
id: amz-logger-objects-and-jobs
node: amazon.amz-logger
type: qa
step: 2
tags: [grown]
---
## Q
在日志框架设计里应该有哪几个对象？各自只负责一件什么事？

## A
`LogRecord`：一条日志的数据（时间、级别、名字、消息），不可变。`Logger`：按名字存在，持有门槛级别和 Handler 列表，负责「要不要记」。`Formatter`：`record → 字符串`，只负责排版。`Handler`：持有一个 Formatter，负责「写到哪」（控制台、文件）。切分依据：记什么、怎么排版、写到哪，三件事各自独立变化。
