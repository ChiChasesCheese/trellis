---
id: hl-ld03-do-write
node: problems.ld03-async-tcp-channel
type: qa
step: 16
---
## Q
`doWrite` 怎么处理部分写？为什么一轮最多写 16 次，写完后为什么要 `signalAll`？

## A
```java
private void doWrite() throws IOException {
    for (int round = 0; round < 16; round++) {            // 限制一轮写多少，别饿死读
        if (!wbuf.hasRemaining()) {
            lock.lock(); try { wbuf.clear(); out.read(wbuf); wbuf.flip(); changed.signalAll(); } finally { lock.unlock(); }
            if (!wbuf.hasRemaining()) return;
        }
        int n = ch.write(wbuf);                           // 可能只写一部分，剩下的留在 wbuf 等下一次 OP_WRITE
        if (n == 0) return;
    }
}
```
- **部分写**：出站环字节先拷到 16 KB 的 `wbuf`（直接缓冲区）；写出多少 `position` 前进多少；没写空保持原样，下次 `OP_WRITE` 继续写 `wbuf`，写空了才从环再取。新手最常漏：扔掉 `write` 返回值，或写一部分就丢弃剩余（几 MB 大消息丢尾巴）；
- 每次从环里取走数据后 `changed.signalAll()`，唤醒阻塞在 `offer(msg, timeout)` 的线程；
- **所有系统调用（`read/write/select`）在锁外**；临界区只做内存拷贝。
