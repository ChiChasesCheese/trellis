---
id: hl-ld03-io-loop
node: problems.ld03-async-tcp-channel
type: qa
step: 6
---
## Q
`TcpMessageChannel` 的 I/O 主循环 和 `doRead` 怎么写？读的上限为什么取入站环空位？

## A
```java
private void ioLoop() {
  try {
    for (;;) {
      int ops = 0;
      lock.lock();
      try {
        if (state == CLOSED) break;
        if (state == FINISHING && !finSent && out.isEmpty() && !wbuf.hasRemaining()) {
            ch.shutdownOutput(); finSent = true;               // 发 FIN：对端 read 返回 -1
        }
        if (finSent && peerClosed) { state = CLOSED; changed.signalAll(); break; }
        readPaused = !peerClosed && in.free() == 0;
        if (!peerClosed && in.free() > 0) ops |= OP_READ;
        if (!finSent && (wbuf.hasRemaining() || !out.isEmpty())) ops |= OP_WRITE;
      } finally { lock.unlock(); }
      key.interestOps(ops);
      selector.select();
      if (selector.selectedKeys().remove(key)) {
          if (key.isReadable()) doRead();
          if (key.isWritable()) doWrite();
      }
    }
  } catch (Throwable t) { lock.lock(); try { failLocked(t); } finally { lock.unlock(); } }
  finally { ch.close(); selector.close(); lock.lock(); try { state = CLOSED; changed.signalAll(); } finally { lock.unlock(); } }
}
private void doRead() throws IOException {
    int room; lock.lock(); try { room = in.free(); } finally { lock.unlock(); }
    if (room == 0) return;
    rbuf.clear(); rbuf.limit(Math.min(rbuf.capacity(), room));   // 读的量不超过入站环空位，feed 一定吃得下
    int n = ch.read(rbuf);                                       // 系统调用在锁外
    if (n < 0) { /* peerClosed = true；hasTruncatedTail() → failLocked(EOFException) */ }
    else if (n > 0) { rbuf.flip(); lock.lock(); try { in.feed(rbuf); changed.signalAll(); } finally { lock.unlock(); } }
}
```
- 读的上限取入站环空位，`feed` 一定吃得下；**所有系统调用（`read/write/select`）在锁外**，临界区只做内存拷贝；读到 EOF 且有不完整尾巴 → `EOFException`。
