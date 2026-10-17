---
id: amz-logger-logger-log-flow
node: amazon.amz-logger
type: qa
step: 3
tags: [grown]
---
## Q
在日志框架设计里，`Logger.log` 的主流程怎么写？级别过滤发生在哪几处？

## A
过滤两次：Logger 先按自己的门槛丢掉低级别日志（此时连 `LogRecord` 都不创建，省开销）；通过后交给每个 Handler，Handler 再按自己的门槛过滤——这样控制台只看 WARN 以上、文件记 DEBUG 以上。时钟注入，便于测试。
```python
class Logger:
    def log(self, level, msg):
        if level < self.level:
            return
        record = LogRecord(self.clock(), level, self.name, msg)
        for h in self.handlers:
            if level >= h.level:
                h.emit(h.formatter.format(record))
```
