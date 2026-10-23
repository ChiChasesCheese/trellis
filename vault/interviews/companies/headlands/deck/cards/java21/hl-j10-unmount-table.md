---
id: hl-j10-unmount-table
node: java21.j10-virtual-threads
type: qa
step: 15
---
## Q
在 JDK 21 里，虚拟线程执行哪些操作会卸载（unmount）载体，哪些不会？

## A
- **会卸载**：`Thread.sleep`、`LockSupport.park`、`java.util.concurrent` 里的锁/队列/`Semaphore`/`CountDownLatch`；`Socket`、`SocketChannel`、`HttpClient` 等网络 I/O（JDK 内部已改成非阻塞 + 轮询器）。
- **不卸载，载体被占住**：文件 I/O（如 `FileInputStream.read`）。调度器会临时多开载体补偿，上限 `maxPoolSize`，默认 **256**。
- **不卸载，pinning（钉住）**：在 `synchronized` 块里阻塞、`Object.wait()`；执行 native 方法或 FFM 下行调用期间阻塞。
