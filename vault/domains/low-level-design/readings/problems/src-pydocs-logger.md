---
nodes: [problems.components.logger]
url: https://docs.python.org/3/library/logging.html
---
# logging — Logging facility for Python（标准库文档）

值得读：本题所有"语义要说准"的地方的权威出处。重点三处：`Logger.getEffectiveLevel()`（沿
`parent` 向上找第一个不是 `NOTSET` 的级别，都没有就用根的级别，根默认 `WARNING`）、
`Logger.propagate` 与 `callHandlers`（**记录沿祖先 logger 链向上交给沿途每个 handler，而且
向上走时不再判祖先 logger 的级别**——这条几乎人人记反），以及 `logging.handlers` 里
`QueueHandler`/`QueueListener`/`RotatingFileHandler` 的现成形态。本题解在第 1、2 条上与它完全
一致并写了测试钉死；唯一故意的偏离是用 `level: LogLevel | None` 取代 `NOTSET = 0`，因为 0 同时
表示"一个级别"和"没设过"是这份 API 里最容易误用的一处。
