---
id: problems-logger-formatter-split-from-handler
node: problems.components.logger
type: qa
step: 3
tags: [grown]
---
## Q
日志框架里，把"写到哪"（handler）和"写成什么样"（formatter）合成一个类有什么后果？拆开之后，handler 的 `emit` 为什么要同时收下格式化好的字符串**和**原始记录？

## A
合在一起，类的数量是两个维度的乘积：`JsonFileHandler`、`TextFileHandler`、`JsonConsoleHandler`……加一种格式就得加一排类。拆开之后是加法——handler 持有一个 formatter，两者各自扩展，在构造时组合，这就是桥接模式（Bridge）"把抽象和实现分离、让它们独立变化"的定义。

`emit(line, record)` 两个参数都要，是因为 handler 可能需要按级别分流（ERROR 走 stderr）。只给字符串的话，它只能去行里搜 `[ERROR]` 这样的子串——而这种写法在换成 JSON 格式化器的当天就会无声失效。**任何"把自己刚生成的字符串再解析回来"的代码都是设计出了问题的信号。**
