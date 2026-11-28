---
id: hi-c-lld-logging-service-b01-stdlib-shape
node: lld.problem-breakdowns.logging-service.beyond
type: qa
step: 2
---
## Q
**日志库 · Python：标准库 logging 的同一形状**｜拓展 · 加分

Python 的 `logging` 和这套设计怎么对应？它在热路径上做了哪些我们没做的事？

## A
**模式。** 策略加组合：Logger、Handler（目的地加锁）、Formatter 三者分工，和这套设计一一对应。

```python
import io
import logging

buf = io.StringIO()
h = logging.StreamHandler(buf)                       # Handler = Destination + Sink 的合体
h.setLevel(logging.WARNING)                          # 阈值在 handler 上，而不是 logger 上
h.setFormatter(logging.Formatter("%(levelname)s %(threadName)s %(message)s"))
log = logging.getLogger("demo")                      # 按名字取，同名同实例（注册表）
log.setLevel(logging.DEBUG)
log.addHandler(h)

log.info("skip %s", "me")                            # 低于 handler 阈值：不写
log.warning("keep %s", "me")                         # 写出
print(buf.getvalue().strip())                        # WARNING MainThread keep me
print(h.lock)                                        # 每个 handler 自带一把 RLock
```
- **每个 handler 一把锁：** `Handler.handle` 先获取自己的锁再调用 `emit`，正是"每目的地一把锁"。它用的是可重入锁（RLock），原因：sink 内部可能再打日志，同一线程要能重入同一把锁，否则自己等自己而死锁。
- **惰性格式化：** 传 `log.info("x %s", obj)` 而不是 `log.info(f"x {obj}")`。参数在记录真正被某个 handler 处理前不会拼成字符串，被过滤掉的 DEBUG 调用几乎不付代价；f-string 不管有没有人要都先拼好。
- **有效级别缓存：** `Logger.isEnabledFor` 对有效级别做缓存，配置变化时清空，对应层级 logger 里"缓存有效级别"的做法。
- **何时不用：** 自己写的小库不要重做这些；这套设计的价值是让你能解释它们为什么存在。
