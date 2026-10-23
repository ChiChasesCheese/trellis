---
id: hl-ld03-pitfalls
node: problems.ld03-async-tcp-channel
type: qa
step: 13
---
## Q
异步 TCP 通道题的常见误区和隐藏测试的边界清单是什么？

## A
**误区**：
1. 以为一次 `read` = 一条消息 → 长度前缀 + 增量解码器；
2. 忽略 `write` 返回值 / 写一部分就当写完 → 保留 `wbuf` 与位置，等 `OP_WRITE`；
3. `OP_WRITE` 一直开着 → CPU 100%；
4. 入站不限界 / 满了还读 → OOM；
5. 暂停读之后没人叫醒 → 通道偶发永久卡住（`poll` 腾出空间后 `wakeup`，阻塞版和自旋版都要验证）；
6. 忘了 `selectedKeys` 的语义（不清除 / 读旧 `readyOps`）→ `if (selectedKeys().remove(key))`；
7. 容量刚好小于最大帧 + 头 → 死锁，构造器校验 `>= maxFrame + 4`；
8. 长度字段不校验 → 恶意 4 字节让你分配 2 GB；
9. EOF 一律当正常结束 → 吞掉半条消息；
10. 关闭时不管接收缓冲区里的数据 → 内核发 RST；
11. 用 `Thread.sleep(100)` 判断「应该已经到了」→ 慢机器偶发失败，应带截止时间轮询；
12. 重连后假设消息不丢；重连：断线期间 `offer` 直接失败、pending 不设上限、`close` 之后还在重连、连接还没稳定就重置退避、上限为 `Long.MAX_VALUE` 时乘法溢出。

**边界清单**：
- 环：容量 1；写满再写；回绕分两段；`writeAll` 放不下一个字节都不写；`peekInt` 跨回绕、符号位；
- 成帧：空负载；恰好 `maxFrame`；`maxFrame+1`；负长度；`0x7FFFFFFF`；字节逐个到达；在每一个切分点切开三条消息；
- 通道 I/O：空消息、最大消息、几 MB 大消息（部分写）、1 万条按序、双向同时 5000 条、裸 socket 逐字节发送；
- 错误：非法帧头 ⟹ `FrameException` + 通道失败 + 之前的消息仍可取；对端在帧中间关闭 ⟹ `EOFException`；`close` 后 `offer` 抛异常；
- 半关闭、背压（接收方不读 ⟹ `offer` 最终 `false` 且有界；开始读后全部按序到达、数量相等；带超时的 `offer` 在对端读之后成功；最小缓冲区 2 万条）；
- 性能：100 万条 32 字节经环 + 解码器 < 2 s；20 万条经回环 < 5 s（实际远低于 1 s）。

**TLS 怎么接进来**：`SSLEngine` 的 `wrap`/`unwrap` 放在字节流和 `FrameDecoder` 之间（入站 `unwrap` → 喂解码器；出站 `wrap` → `wbuf`）；难点是 `BUFFER_UNDERFLOW` 和握手阶段的 `NEED_WRAP/NEED_UNWRAP/NEED_TASK`；环 + 中转缓冲 + I/O 线程的结构留出了放它的位置。

应用层确认 + 序号 + 重放可得 at-least-once，加去重得 effectively-once；心跳 / 空闲超时检测半开连接。
