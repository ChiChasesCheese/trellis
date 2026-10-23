---
id: hl-j16-real-misc
node: java21.j16-concurrency-primitives
type: qa
step: 39
---
## Q
`byteArrayViewVarHandle` 在 `TickerCodec` 里做什么？`ConcurrentMerge.close()` 怎么保证幂等关闭？

## A
- `TickerCodec`：`BE_LONG = MethodHandles.byteArrayViewVarHandle(long[].class, ByteOrder.BIG_ENDIAN)`，`long word = (long) BE_LONG.get(buf, off)` 一次读出 8 字节（大端），不必逐字节拼。这里是 plain `get`，无并发语义，只为一次读 8 字节。
- `ConcurrentMerge`：`AtomicBoolean closed`，`close()` 里 `if (!closed.compareAndSet(false, true)) return;`：CAS 实现**幂等关闭**，多线程同时调 `close()` 只有一个真正执行。数据通道用 `ArrayBlockingQueue`（内部 `ReentrantLock` + `Condition`），生产者阻塞在 `put` 时虚拟线程可卸载。
