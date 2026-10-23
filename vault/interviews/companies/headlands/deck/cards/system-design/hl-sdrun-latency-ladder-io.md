---
id: hl-sdrun-latency-ladder-io
node: system-design.how-to-run
type: qa
step: 11
---
## Q
内核网络栈单跳、内核旁路、同机房往返、NVMe fsync、光纤和微波的传播延迟各是多少？

## A
- 内核 TCP / UDP 单跳（收或发）：几 µs 到十几 µs，内核旁路要省的就是它；
- 内核旁路收发：约 1 µs 或更低；
- 同机房网络往返（RTT）：普通约 50–500 µs，同机架 / 直连更低，这是复制日志到另一台机器的价格；
- NVMe 一次 fsync：数十 µs 到 ms，不稳定，热路径不 fsync 或做 group commit；
- 光在光纤里约 **5 µs / km**（约 200,000 km/s，真空光速的 2/3），物理距离就是延迟，这是 co-location 的理由；
- 微波（近似真空）约 3.4 µs / km：芝加哥–纽约约 1,150 km，微波约 4 ms，光纤约 7 ms。

用法例：「写日志到本地 NVMe 并 fsync 数十 µs 起步，我的预算只有 10 µs，所以热路径只做内存追加，持久化放另一个线程，靠复制 + 重放保证安全。」
