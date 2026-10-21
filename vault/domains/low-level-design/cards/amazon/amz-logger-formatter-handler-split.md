---
id: amz-logger-formatter-handler-split
node: amazon.amz-logger
type: qa
step: 4
tags: [grown]
---
## Q
在日志框架设计里，为什么排版（Formatter）和输出（Handler）要拆开，而不是每个 Handler 自己排版？

## A
有 M 种格式（文本、JSON、带颜色）和 N 个目的地（控制台、文件、网络）时，合在一起要写 M×N 个子类；拆开只要 M+N 个，且任意组合。新增 JSON 格式只写一个 `JsonFormatter`，控制台和文件的 Handler 一行不改；这是用组合代替继承的典型取舍。
