---
id: amz-logger-what-and-three-questions
node: amazon.amz-logger
type: qa
step: 1
tags: [grown]
---
## Q
日志框架（Logger）要你设计什么？开场先问哪三个澄清问题？

## A
日志框架让业务代码调用 `logger.info(msg)`，由框架决定这条日志要不要记、长什么样、写到哪里。三问：(1) 输出到几个目的地（控制台、文件、多个同时）——决定要不要 Handler 列表；(2) 要不要按级别过滤、按模块名分层——决定 Logger 是否带名字和门槛级别；(3) 格式固定还是可换（文本、JSON）——决定格式化要不要独立成类。
