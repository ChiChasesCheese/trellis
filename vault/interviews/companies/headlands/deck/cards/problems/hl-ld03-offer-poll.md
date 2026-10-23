---
id: hl-ld03-offer-poll
node: problems.ld03-async-tcp-channel
type: qa
step: 7
---
## Q
`offer` 和 `poll`（含带超时版本）怎么写？`readPaused`、`wakeup` 在什么条件下调用，为什么在锁外？

## A
```java
public boolean offer(byte[] msg) {
    lock.lock();
    boolean wasEmpty;
    try {
        requireSendable();                          // 已 close / finishSending / 失败 → IllegalStateException
        wasEmpty = out.isEmpty();
        if (!FrameCodec.encode(out, msg, cfg.maxFrame())) return false;   // 暂时满了
    } finally { lock.unlock(); }
    if (wasEmpty) selector.wakeup();                // 从空变非空才需唤醒
    return true;
}
public byte[] poll() {
    boolean wake; byte[] m;
    lock.lock();
    try {
        m = nextLocked();
        wake = m != null && readPaused;
        if (wake) readPaused = false;
    } finally { lock.unlock(); }
    if (wake) selector.wakeup();                    // 锁外
    return m;
}
public byte[] poll(long timeoutMs) throws InterruptedException {
    long nanos = TimeUnit.MILLISECONDS.toNanos(timeoutMs);
    boolean wake = false; byte[] m;
    lock.lock();
    try {
        for (;;) {
            m = nextLocked();
            if (m != null || inboundFinishedLocked() || nanos <= 0) break;
            nanos = changed.awaitNanos(nanos);
        }
        if (m != null && readPaused) { readPaused = false; wake = true; }
    } finally { lock.unlock(); }
    if (wake) selector.wakeup();
    return m;
}
```
- `IllegalStateException` 与 `false` 区分：`false` 是「暂时满了，稍后再来」，异常是「通道已不能发」；`offer` 满了抛异常而不是返回 false 是错的，反过来通道已关闭时只返回 false 也是错的；
- `offer` 返回 `true` 表示已编码进出站环，保证按序写进 socket（除非连接失败）；
- `poll(timeout)` 范式：`for(;;) { 先检查条件; 不满足就 await }`，`awaitNanos` 返回剩余时间；
- `readPaused`：I/O 线程因入站环满暂停读时置位；`poll()` 取走一条消息（腾出空间）后清除并在**锁外**调用 `wakeup()`，只有「确实暂停了读」才唤醒，省掉每次 `poll` 的系统调用。**非阻塞 `poll()` 和 `poll(timeout)` 都要唤醒**，自旋 `poll()` 的消费者也要能恢复暂停的读；
- 对端关闭或本端关闭之后，**已缓冲的完整消息仍可取**；帧头非法 ⟹ `poll` 抛 `FrameException`，通道失败（`failure()` 是它）；
- `close()` 唤醒所有阻塞在 `poll(timeout)`/`offer(msg, timeout)`/`awaitClosed` 的线程。

`MessageServer`：一个 accept 线程加阻塞队列；`accept(timeoutMs)` 超时返回 `null`；port 0 = 内核分配临时端口；`wrap(SocketChannel, cfg)` 接管已连接的 socket；`connect(addr, cfg, timeoutMs)`。
