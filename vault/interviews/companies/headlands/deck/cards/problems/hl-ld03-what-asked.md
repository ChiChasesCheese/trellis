---
id: hl-ld03-what-asked
node: problems.ld03-async-tcp-channel
type: qa
step: 1
---
## Q
异步 TCP 消息通道（Asynchronous TCP Message Channel）题要做什么？四个 Part 和共同约定是什么？

## A
行情网关与策略（或订单网关与交易所）之间只有一条 TCP 连接。TCP 提供**可靠有序的字节流，不是消息流**：写两条各 10 字节的消息，对端可能一次 `read` 到 20 字节（合并），也可能先 13 再 7（在消息中间切开）；`write` 在发送缓冲区快满时只写一部分（**部分写**）；对端读得慢则内核缓冲区装满、TCP 窗口缩到 0、背压一路传回；连接可能断。要在字节流上做**有界**的接口：`boolean offer(byte[] msg)` 满了返回 `false`；`byte[] poll()` 没有返回 `null`。关键词：bounded、local circular buffers、partial-I/O framing。

- **Part 1**：`ByteRing`、`FrameCodec`、`FrameDecoder`，纯内存：字节环、4 字节大端长度前缀成帧、增量解码器；
- **Part 2**：`TcpMessageChannel`、`MessageServer`，一个 `Selector` I/O 线程 + 出站环 + 入站解码器，部分读写、EOF、`finishSending`（半关闭）、`close`；
- **Part 3**：背压与有界性：接收方不读时 `offer` 返回 `false`；入站环满时停止读 socket；最小缓冲区压力测试；
- **Part 4**：`Backoff`、`ReconnectingClient`：指数退避，断线重连，断线期间有界 pending 队列。

**共同约定**：帧格式 `[len:int32 大端][payload:len 字节]`，`len` 合法范围 `[0, maxFrame]`，空负载合法；`ChannelConfig(maxFrame, outCapacity, inCapacity)`，`outCapacity`、`inCapacity` 必须 `>= maxFrame + 4`，紧凑构造器校验；测试在 `127.0.0.1` + 内核分配临时端口跑；**不允许依赖 `Thread.sleep` 的时序判断正确性**，只允许用截止时间的轮询；`offer` 返回前已把字节拷进出站环；`TCP_NODELAY` 必须开。

`offer`：消息超过 `maxFrame` → `IllegalArgumentException`；通道已 `close`/`finishSending`/失败 → `IllegalStateException`（与「暂时满了」的 `false` 区分）。

考点：TCP 是字节流；有界 = 每一层都有上限且「满」一路传到对端；`Selector` 的纪律；正确的失败语义；并发测试方法。
