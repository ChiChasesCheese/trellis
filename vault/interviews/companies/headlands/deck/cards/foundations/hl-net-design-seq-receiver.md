---
id: hl-net-design-seq-receiver
node: foundations.networking-basics
type: qa
step: 50
---
## Q
设计：行情接收器从组播组收 UDP 包，每个包头有 8 字节序号，处理必须按序号递增。收到乱序或缺口怎么办？

## A
维护 `expectedSeq`：
- `seq == expected`：处理并 `expected++`，再检查缓冲里有无以 `expected` 开头的后续包；
- `seq > expected`：记缺口 [expected, seq)，暂存这个包（小的重排窗口，几毫秒），等 A/B 另一条线的同序号包；窗口超时仍缺则向回补通道请求重传，或等快照；
- `seq < expected`：重复包（A/B 另一份），丢弃。

另外定期心跳携带最新序号，以发现末尾丢失；接收线程里只收包和排序，不做重活，防止 `SO_RCVBUF` 溢出。
