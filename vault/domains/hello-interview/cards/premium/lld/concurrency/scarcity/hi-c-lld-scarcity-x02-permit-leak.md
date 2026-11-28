---
id: hi-c-lld-scarcity-x02-permit-leak
node: lld.concurrency.scarcity.exam
type: qa
step: 2
---
## Q
**并发稀缺资源 · 漏还许可的后果**｜考点 · 必会

`sem.acquire(); do_work(); sem.release()`，没有 `finally`。`do_work` 偶尔抛异常。许可数 5，抛 5 次之后会怎样？监控里看到什么？

## A
- **后果：** 5 个许可全部泄漏，之后每个线程都永远阻塞，服务挂起
- **监控：** 没有崩溃，没有错误日志，只有请求超时
- **修法：** `with sem:` 或 `try/finally`
- **排查：** 记录获取与持有时长，持有超过阈值告警；用有界信号量发现多还
