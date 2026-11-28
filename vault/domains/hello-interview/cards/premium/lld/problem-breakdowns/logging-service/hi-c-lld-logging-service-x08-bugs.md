---
id: hi-c-lld-logging-service-x08-bugs
node: lld.problem-breakdowns.logging-service.exam
type: qa
step: 6
---
## Q
**日志库 · 找错：四个常见实现缺陷**｜考点 · 必会

下面四种写法各有什么问题：(a) `Logger.log` 里 `with self._lock:` 包住整个分发；(b) `Record` 是可变对象，某个 formatter 为了省事改了 `message`；(c) 每个目的地异常处理里直接 `pass`；(d) `FileSink.write` 每次都 `open(path, "a")`。

## A
- **(a)：** 全局锁，慢目的地阻塞所有日志调用，格式化也被锁住；锁应跟着 sink 走。
- **(b)：** 同一条记录发给多个目的地，一个 formatter 改了消息，后面的目的地看到被改过的内容，且并发读写没有同步。记录应该只读，formatter 返回新字符串。
- **(c)：** 静默失败，文件目的地坏了没人知道。至少在 stderr 写一行诊断，并限量。
- **(d)：** 每次写都付出一次 `open` 系统调用和文件句柄分配，开销远大于写本身；应该构造时打开一次、保留句柄，并在合适时机 `flush`。
- **共同点：** 前三条都是"共享状态没有被明确归属"；说出归属（锁属于 sink，记录归属创建者且只读，错误归属目的地）能一次性解决。
