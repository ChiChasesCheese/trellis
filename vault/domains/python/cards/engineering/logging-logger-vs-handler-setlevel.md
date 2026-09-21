---
id: logging-logger-vs-handler-setlevel
node: engineering.logging-config
type: qa
source: python-docs
---
## Q
`logging` 里 `Logger.setLevel()` 和 `Handler.setLevel()` 都能设置级别，为什么需要两个？它们分别在过滤流程的哪个环节起作用？

## A
logger 的级别决定「这条事件要不要往下继续处理、传给它的处理器」——这是第一道关卡；处理器的级别决定「这条已经到达该处理器的事件，要不要真的被这个处理器输出」——这是第二道关卡，同一个 logger 可以挂多个级别设置不同的处理器（比如一个只输出 ERROR 以上到邮件，另一个把 DEBUG 以上都写进文件）。一条日志要同时通过 logger 的级别门槛和某个具体处理器的级别门槛，才会被那个处理器真正输出。
