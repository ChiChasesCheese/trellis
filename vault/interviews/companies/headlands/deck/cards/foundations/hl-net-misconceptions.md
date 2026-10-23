---
id: hl-net-misconceptions
node: foundations.networking-basics
type: qa
step: 41
---
## Q
网络方面常见的八个误区是什么？

## A
1. 「`write` 返回了对方就收到了」：只是进了内核发送缓冲区；
2. 「TCP 保证消息送达所以不用处理半包」：TCP 只保证字节有序，**不保证**消息边界；
3. 「UDP 一定丢包所以不能用」：数据中心内丢包很少，应用层序号 + 缺口检测更灵活；
4. 「设了 `TCP_NODELAY` 就一定低延迟」：它只消除 Nagle 的延迟，还有延迟确认、拥塞窗口、系统调用、上下文切换、GC 暂停、锁争用；
5. 「`select()` 返回就是消息完整了」：只是此刻读不阻塞；
6. 「虚拟线程让 Java 变快了」：提高并发度，不是单请求延迟；
7. 用 `localhost` 回环的数字推测网线延迟：回环没有传播延迟，只代表软件栈开销；
8. 组播收不到：先查网卡选择、防火墙、IGMP snooping、`SO_REUSEADDR`、TTL。
