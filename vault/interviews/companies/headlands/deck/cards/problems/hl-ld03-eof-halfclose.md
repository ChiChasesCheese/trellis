---
id: hl-ld03-eof-halfclose
node: problems.ld03-async-tcp-channel
type: qa
step: 9
---
## Q
EOF、半关闭（half-close）和 RST 是什么？`finishSending`、EOF 落在帧中间、优雅关闭分别怎么处理？

## A
- 对端 `close()`（或 `shutdownOutput()`）→ 发 **FIN**；本端 `read` 返回 **-1**（EOF）。EOF 是「对端不会再发了」，**不等于「我也该关了」**：TCP 全双工，可只关一个方向（**半关闭**）；`shutdownOutput()` 本端不再发送但仍可接收，`finishSending()` 就是它（先刷完已接受的消息）；
- **RST**：连接被重置。原因：对端进程崩溃；向已关闭端口发数据；**`close()` 时接收缓冲区里还有没读的数据**——内核发 RST 而非 FIN，对端未读完的数据可能被丢。所以**优雅关闭**是先 `shutdownOutput`，等对端 EOF，再 `close`。
- **EOF 恰在一帧中间**（读到了头和半个内容）= 流被截断，是错误（`failure()` 是 `EOFException`），不是正常结束；通道关闭，但之前收齐的完整帧仍可 `poll`。判断依据：`hasTruncatedTail()`。

语义：
- `isPeerClosed()` 变 true，之后仍可 `poll` 剩余消息、仍可 `offer`（半关闭）；不在 EOF 时立刻 `close`，对端可能只是半关闭，我们这边还有话说；
- `isDrained()` = 不会再有新消息且缓冲区里没有完整消息；
- `finishSending()`：状态变 `FINISHING`（之后 `offer` 抛 `IllegalStateException`）；I/O 线程等出站环和 `wbuf` 都空了再 `shutdownOutput()` 发 FIN；**本端已发 FIN 且对端也 EOF ⟹ 自动关闭**（`failure()` 为 null）；
- `close()`：立刻关闭，未发送的数据丢弃，幂等，唤醒所有等待者；
- 帧头非法：`poll` 抛 `FrameException`，通道失败，之前的消息仍可取。

样例：`client` 发 1000 条 `new byte[10]` 后 `finishSending()`，server 一直 `poll` 到返回 null，然后 `isDrained() == true`、`isPeerClosed() == true`；对端先收齐全部再看到 EOF；对端仍能回话；双方 `finishSending` ⟹ 两端关闭且 `failure() == null`。

测试方法：不依赖 `sleep` 判断正确性，只用带截止时间的轮询等待「最终发生」的事件；确定性消息（序号可校验）；裸 socket 逐字节发送；一次写入「两条半」；`close` 唤醒阻塞的 `poll(30_000)`。

常见误区：EOF 一律当正常结束（吞掉半条消息）；关闭时不管接收缓冲区里的数据（发 RST，对端丢掉未读数据）。

对端掉电（没有 FIN 也没有 RST）：TCP 区分不了「暂时没消息」和「对方没了」，要靠应用层心跳；`SO_KEEPALIVE` 默认空闲两小时才探测，粒度太粗；也可读写超时。
