---
id: pl-conc-ioruntimes-pitfall-no-timeout
node: concurrency.io-runtimes
type: qa
step: 10
---
## Q
一个连接的对端只建立连接、然后沉默，没有设置读超时的 `Read` 会怎样？为什么“便宜的阻塞”恰恰让这个 bug 在生产里更隐蔽？

## A
goroutine、虚拟线程、协程都很便宜，所以一个停在 `Read` 上的任务**几乎不会引起告警**：不占 OS 线程，几 KB 内存，CPU 为零。但它也永远不会结束，连接数和内存缓慢累积，直到出现 fd 耗尽（`too many open files`）、内存增长、连接池被占满。

Go 实测：客户端连上之后沉默：
```go
func serve(c net.Conn, deadline bool, done chan<- string) {
	buf := make([]byte, 16)
	if deadline { c.SetReadDeadline(time.Now().Add(200 * time.Millisecond)) }
	_, err := c.Read(buf)
	done <- fmt.Sprint("Read returned: ", err)
}
```
输出：
```
deadline = false -> still blocked after 1s; goroutines: 2
deadline = true -> Read returned: read tcp 127.0.0.1:50446->127.0.0.1:50448: i/o timeout
```
没有截止时间的那个 goroutine 永远停在那里；有截止时间的在 200 毫秒后收到 `i/o timeout` 并可以清理资源。

**为什么隐蔽**：线程模型下，这类问题很快因为线程耗尽而爆炸，变成容易发现的故障；轻量任务模型把症状推迟到数小时甚至数天后才出现，那时根因已经难找。

**相同的陷阱在各语言里的样子**：
- **Java**：`Socket.read()` 默认无限等待，`setSoTimeout` 之后抛 `SocketTimeoutException: Read timed out`；`HttpClient` 要同时设连接超时和请求超时。
- **Rust**：`TcpStream::read().await` 不会自己超时，要用 `tokio::time::timeout(dur, fut)`。
- **Python**：`await reader.read()` 同样无限等待，要用 `asyncio.timeout()` 或 `wait_for`。

**防线**：
1. 每个网络操作都有超时，并作为代码评审的检查项；
2. 服务端设置空闲连接超时和最大连接生命周期；
3. 监控活跃连接数和任务数（Go 的 `runtime.NumGoroutine`、`pprof` 的 goroutine profile），任何随时间单调上升的曲线都是泄漏的信号。
