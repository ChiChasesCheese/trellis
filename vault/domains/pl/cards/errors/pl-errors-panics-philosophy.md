---
id: pl-errors-panics-philosophy
node: errors.panics
type: qa
step: 4
---
## Q
Go 为什么说 `panic` 不是异常，Rust 为什么把 panic 与 `Result` 严格分开？「让它崩溃」又是什么思路？

## A
**Go：panic 是 bug 的信号，不是错误处理。** Go 的 FAQ 明确说，没有常规的异常机制，是因为异常把正常的失败（如打不开文件）也混进了特殊的控制流。`panic`/`recover` 存在，但约定是：包的内部可以用 panic 做深层递归的快速退出（`encoding/json` 就这样做），**但不能让 panic 越过包的 API 边界**，对外必须转成 `error`。

标准库里典型的 `recover` 用法是 `net/http`：处理某个请求的 handler 发生 panic，服务器 `recover` 后记录日志、关闭该连接，不让整个服务挂掉。这是边界保护，不是业务错误处理。

**Rust：类型表达预期的失败，panic 表达 bug。** `Result` 用于调用者应该考虑的情形，`panic!`/`unwrap`/越界用于「如果发生就说明代码错了」。`expect("config validated at startup")` 的价值在于，那条消息记录了你的假设：不变量是什么、为什么它应当成立。

**Erlang：让它崩溃（let it crash）。** 把系统切成大量小而隔离的进程，每个进程只写正常路径，出错就让它死，由监督者按策略重启。理由是：在出错的进程里写防御代码，既复杂，又基于一个已经被破坏的状态；重启回到已知的干净状态更可靠。Kubernetes 重启崩溃的 Pod、Go 服务由进程管理器拉起，都是同一种思路在基础设施层的体现。

三者共通的信念：**对 bug，不要试图优雅地继续，应当快速、明显地失败，并依靠外层的隔离与重启来恢复服务**。争议在于「外层」是哪一层：函数、goroutine、线程、进程还是容器。
