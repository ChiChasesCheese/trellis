---
id: hl-javaq-rubric-i-network
node: java-questions.rubric
type: qa
step: 13
---
## Q
回答网络（TCP、NIO / epoll、低延迟网络）的问题时，强、一般、弱的答案各有什么特征？

## A
- **强**：TCP 握手 / 确认 / 重传 / 拥塞控制；Nagle + 延迟 ACK 的相互作用与"一条消息一次 write + `TCP_NODELAY`"；`Selector` / epoll 反应器 vs 线程每连接 vs 虚拟线程；epoll 为什么优于 select；低延迟网络清单（二进制协议、忙轮询、绑核、UDP 多播、内核旁路），并诚实说出 Java 在内核旁路上弱；能做限定，如"我在 macOS 上没复现 40 ms，那是 Linux 常见现象"。
- **一般**：知道 NODELAY，知道 NIO 比 BIO 并发高，说不出为什么。
- **弱**：把 `TCP_NODELAY` 说成"更快的协议"；认为 NIO"更快"而不是"更能扩展"。
