---
id: hl-net-write-journey
node: foundations.networking-basics
type: qa
step: 5
---
## Q
一个字节从应用 `write` 到网线经历哪几步？`write` 返回意味着什么？接收缓冲区满了会怎样？

## A
发送方向：
1. 应用 `write(sock, buf)`，一次系统调用（几百 ns）；
2. 内核把数据拷贝进 socket 发送缓冲区（`SO_SNDBUF`），`write` 在这里就返回了；
3. TCP 切段、加序号和校验和，决定现在能不能发（拥塞窗口、对端接收窗口、Nagle）；
4. IP 加头并查路由表；
5. 网卡驱动放进发送环形队列（TX ring），网卡 DMA 取走发出。

接收方向反过来：网卡 → DMA 写接收环 → 中断或轮询 → 内核协议栈 → socket 接收缓冲区（`SO_RCVBUF`）→ 应用 `read` 拷贝到用户缓冲区。

两个后果：
- `write` 返回 ≠ 对方收到了，只代表数据进了内核缓冲区；
- 接收缓冲区满了，TCP 让对方慢下来，UDP 则**直接丢包**。
