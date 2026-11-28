---
id: hi-c-lld-logging-service-n09-sink
node: lld.problem-breakdowns.logging-service.notes
type: qa
step: 9
---
## Q
**日志库 · Sink：只负责把字符串变成字节**｜摘要 · 必会

`Sink` 的职责边界是什么？为什么它不过滤、不格式化、不加锁？

## A
- **接口：** 只有一个方法 `write(formatted)`。`ConsoleSink` 写标准输出，`FileSink` 追加写文件。
- **故意很笨：** 过滤、格式化、加锁都在上一层的 `Destination` 里。sink 只负责"把字符串变成目标上的字节"。
- **好处一：** 需求里说的远程目的地，只需新增一个写网络端点的 `RemoteSink`，其他类一个都不用改。
- **好处二：** 测试容易，传一个把调用记下来的假 sink 即可，不用真的写文件。
- **依赖方向：** 高层的工作流类 `Destination` 依赖 `Sink` 和 `Formatter` 这两个抽象，而不是 `ConsoleSink`、`JsonFormatter` 这样的具体类，这是依赖倒置（Dependency Inversion）。
- **缓冲和编码：** 交给语言自己的输出流，sink 只管调用对的方法。
