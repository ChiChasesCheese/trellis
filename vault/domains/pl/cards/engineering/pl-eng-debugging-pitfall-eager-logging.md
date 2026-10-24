---
id: pl-eng-debugging-pitfall-eager-logging
node: engineering.debugging
type: qa
step: 10
---
## Q
关闭了 DEBUG 级别的日志，为什么服务的 CPU 仍然被日志拖慢？调用时拼接字符串和传参数给日志库有什么区别？

## A
日志库只会跳过**输出**，不能跳过你在调用前**已经算好的参数**。`log.debug(f"state={json.dumps(state)}")` 里，f-string 和 `json.dumps` 在 `debug` 被调用之前就执行了，不管 DEBUG 开没开。

Python 实测（DEBUG 关闭，`state` 是 200 个键的字典，每次调用的耗时）：
```python
log.setLevel(logging.INFO)                               # DEBUG is off
log.debug(f"state={json.dumps(state)}")   # 22.43 us per call
log.debug("state=%s", state)              #  0.04 us per call
```
急切拼接比惰性传参慢约 500 倍。热点路径每秒几万次，这就是白白烧掉的一个核。

**各语言的规则**：
- **Python**：用 `%s` 风格的参数（`log.debug("x=%s", x)`），日志库在确认级别启用后才格式化；或者先 `if log.isEnabledFor(logging.DEBUG):`。
- **Java**：SLF4J 用 `log.debug("x={}", x)`，不要写 `"x=" + x`；昂贵的参数用 lambda 供应器（`log.atDebug().addArgument(() -> compute()).log(...)`）。
- **Go**：`slog` 的 `Debug` 在级别不满足时直接返回，参数已按值传入；昂贵的计算要先 `if log.Enabled(ctx, slog.LevelDebug)`，或实现 `LogValuer` 让值延迟求值。
- **Rust**：`tracing` 的宏在级别未启用时不会求值参数，这是宏相比函数的一个优势。

另外两个常见的日志事故：
1. **日志本身成为瓶颈**：同步写磁盘/控制台、全局锁；在高并发下要用异步日志或采样。
2. **不要在日志里调用可能抛异常或有副作用的方法**（比如 `obj.toString()` 触发懒加载），日志语句不该改变程序行为。

做法：评审时把“日志参数的求值成本”当作检查项；热路径上先量一下，用 profile 确认日志占 CPU 的比例。
