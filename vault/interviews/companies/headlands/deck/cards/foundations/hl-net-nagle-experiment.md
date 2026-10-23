---
id: hl-net-nagle-experiment
node: foundations.networking-basics
type: qa
step: 24
---
## Q
在 macOS 回环上做 Nagle 实验：写-写-读的请求回复、连续写 20 万次 1 字节，结果各是什么？这说明什么，面试怎么说才诚实？

## A
- 写-写-读（4 字节 header + 40 字节 body，等 44 字节回显）：`TCP_NODELAY=false` 121 µs，`true` 78 µs。**没有复现 40 ms 停顿**，两者都是百微秒量级，方向也不稳定（另几次 85 对 148、119 对 109），macOS 回环对延迟确认的处理与 Linux 不同。
- 连续写 20 万次 1 字节：`NODELAY=false` 92 ms，`true` 341 ms；开着 Nagle 快 **3.7 倍**（另几次 88 对 495 ms，5.6 倍，方向稳定）。

结论：Nagle 不是「坏东西」，对批量写小块的吞吐有益；问题只出在请求 / 响应的交互式小消息。面试可说「Linux 上典型约 40 ms」，但不要说成「我测过」。
