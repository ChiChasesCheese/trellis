---
id: hl-ld03-reconnect
node: problems.ld03-async-tcp-channel
type: qa
step: 11
---
## Q
`ReconnectingClient` 的 `offer`、pending 队列、管理线程怎么设计？重连后的语义（at-most-once）为什么要诚实说明，怎么升级为不丢？

## A
`offer` 永远先进有界 `pending`（保证顺序），按已编码字节（`4 + len` 之和）计，上限 `cfg.outCapacity()`，放不下返回 `false`；断线期间 `offer` 仍成功（直到装满）；`close` 之后抛 `IllegalStateException`。

后台一个线程（本参考用虚拟线程，`Thread.ofVirtual().name(...).start(...)`，里面是「连接 → 等待 → 退避」的直线阻塞代码）：
```java
private void run() {
    while (!isClosed()) {
        TcpMessageChannel ch;
        try { ch = TcpMessageChannel.connect(addr, cfg, 2_000); }
        catch (IOException e) { failedAttempts++; if (!sleep(backoff.next())) return; continue; }
        lock.lock(); try { if (closed) { ch.close(); return; } current = ch; connectCount++; backoff.reset(); } finally { lock.unlock(); }
        pump(ch);
        lock.lock(); try { current = null; abandonedBytes += ch.unsentBytes(); } finally { lock.unlock(); }
        ch.close();
    }
}
private void pump(TcpMessageChannel ch) {          // 持客户端锁
    while (!closed && ch.isOpen() && !ch.isPeerClosed()) {
        while (!pending.isEmpty()) {
            byte[] m = pending.peekFirst();
            boolean accepted;
            try { accepted = ch.offer(m); } catch (IllegalStateException channelDied) { return; }
            if (!accepted) break;                  // 通道出站环满了：等一会儿再试
            pending.pollFirst(); pendingBytes -= FrameCodec.HEADER + m.length;
        }
        wake.await(10, TimeUnit.MILLISECONDS);     // 周期性醒来检查连接是否还活着 / 出站环是否腾出空间
    }
}
```
- 连接成功后把 `pending` 按序搬进当前通道；通道断开（`!isOpen()` 或 `isPeerClosed()`，应用协议无半关闭，对端 EOF 当断线）⟹ 丢掉旧通道 ⟹ 退避后重连；连接失败 `failedAttempts++`，按 `Backoff` 等待；
- `poll()` 返回当前连接上的入站消息，断线期间 null；状态：`isConnected()`、`connectCount()`、`failedAttempts()`、`abandonedBytes()`、`pendingBytes()`；
- `close()`：关闭当前通道、唤醒管理线程、之后不再重连、`offer` 抛异常、幂等。

**诚实的语义**：已经交给旧通道（进了它的出站环 / 内核缓冲区）的消息，连接断掉时**可能丢失**。TCP 只保证一条连接存续期间的有序不丢，不保证对端应用处理了；你不知道对端处理到哪。本类是 **at-most-once 的尽力而为**，丢失字节累计在 `abandonedBytes()`。`offer` 返回 `true` 只表示进入了本进程的有界 pending 队列，不是对端收到。

**升级为不丢**：应用层递增序号 + 接收方周期性确认已收到的最大连续序号 + 发送方保留未确认消息（有界重传缓冲，满了向上背压）；重连时握手交换「我收到哪了」，发送方从那里重发，接收方按序号去重——at-least-once + 去重 = effectively-once；FIX 会话层就这么做。持久化发送队列后 `true` 才能表示「已持久化」。

测试：服务端踢掉连接 ⟹ 自动重连并继续收发；服务端整个下线 ⟹ 断线期间 `offer` 成功，重新上线（同一端口）后按序全部到达；`pending` 有界（10 条 × 50 字节 = 500）；`close` 后不再重连。
