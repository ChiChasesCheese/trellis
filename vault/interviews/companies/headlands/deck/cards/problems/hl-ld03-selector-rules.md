---
id: hl-ld03-selector-rules
node: problems.ld03-async-tcp-channel
type: qa
step: 5
---
## Q
NIO `Selector` 的四条使用纪律是什么？为什么「就绪不等于完成」，`OP_WRITE` 为什么不能常开，兴趣集由谁修改？

## A
**非阻塞**：`read` 没数据立刻返回 0；`write` 发送缓冲区满时返回 0 或只写一部分。**`Selector`**：一个线程盯着很多套接字，问内核「哪些就绪」；`select()` 睡眠直到有套接字就绪或别的线程 `selector.wakeup()`。兴趣集：`OP_READ`（有数据可读）、`OP_WRITE`（发送缓冲区有空位）。

1. **就绪 ≠ 完成**：`OP_READ` 只表示「现在读不会阻塞」，不表示「一条完整消息到了」；
2. **`OP_WRITE` 不要常开**：有空位它就一直就绪，`select()` 立刻返回，循环变 100% CPU 忙等；只在「还有数据要写」时打开，写完就关；
3. **谁改兴趣集**：只有 I/O 线程改；别的线程设状态 + `selector.wakeup()`，由 I/O 线程在循环顶部**重算**。`wakeup()` 是「粘性」的：当时没有 `select` 在进行，下次 `select` 立刻返回——不丢唤醒；
4. **`selectedKeys` 和 `readyOps`**：只有被选中 key 的 `readyOps` 是新鲜的；被 `wakeup` 叫醒时没有 key 被选中，`readyOps()` 可能是上一轮的旧值。所以写 `if (selector.selectedKeys().remove(key)) { 看 readyOps }`。

每轮循环顶部（锁内）按状态重算：
```
OP_READ  ⇐ 对端没关闭 且 入站环还有空位
OP_WRITE ⇐ 还没发 FIN 且 (wbuf 里还有数据 或 出站环非空)
```
兴趣集为 0 时 `select()` 睡到 `wakeup()`，是预期。应用线程改变状态（`offer`、`poll` 腾出空间、`close`）就 `wakeup()`；「该关注什么」的决定都在一个线程里，没有竞态。`offer` 只有出站环**从空变非空**才 `wakeup`（非空时 I/O 线程已在等 `OP_WRITE`），且设置兴趣集和读 `out.isEmpty()` 在同一把锁里。

找 bug 题：`while (true) { selector.select(); for (k : selectedKeys()) { if readable doRead(); if writable doWrite(); } }`——①没有 `selectedKeys().clear()`/迭代器 `remove`，key 一直留在集合里，下一轮没就绪也被处理（读旧 `readyOps`）；②没按状态更新兴趣集；③没处理 `wakeup`，`offer` 后无法叫醒 I/O 线程。

C++/epoll：NIO 对应用表现为**水平触发**（LT）：还有数据没读完，下次 `select` 仍报就绪，所以可少读一点（受入站环空位限制）不丢事件；边缘触发（ET）要求读到 `EAGAIN`，否则丢事件。

NIO vs 虚拟线程：每连接一线程在 C10K 下栈内存（约 1 MB 虚地址）和调度吃力；`Selector` 一线程服务大量连接，同一个 Selector 可注册多个通道。
