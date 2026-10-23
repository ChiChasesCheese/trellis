---
id: hl-javaq-i-q40-experiment
node: java-questions.i-network
type: qa
step: 3
---
## Q
用 NIO Selector 服务端加阻塞客户端、把 8 字节请求拆成两次 4 字节写的实验里，开关 `TCP_NODELAY` 各是多少微秒？为什么没复现 40 ms？面试时该怎么说？

## A
- `TCP_NODELAY=true`：两次小写后等回应，**17.0 µs**/请求（n=20000）。
- `TCP_NODELAY=false`：**21.0 µs**/请求（n=200）。
- **没有复现经典的 40 ms 卡顿**：macOS 的 loopback 与 Linux 的延迟 ACK / Nagle 实现不同，两种设置只差约 20%。
- 面试时**讲机制**，不要说"我测过 40 ms"；要确认就在目标 Linux 上用 `ss -ti` 加抓包。
- 其他要点：拥塞控制（慢启动、拥塞窗口）影响新连接吞吐；`SO_RCVBUF / SO_SNDBUF` 缓冲大小；`SO_REUSEADDR`；`TIME_WAIT`；重传（RTO）造成的尾延迟尖刺；`ss -ti` 看 rtt、cwnd、retrans。
