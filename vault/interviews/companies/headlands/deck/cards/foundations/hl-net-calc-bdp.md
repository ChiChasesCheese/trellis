---
id: hl-net-calc-bdp
node: foundations.networking-basics
type: qa
step: 46
---
## Q
计算：RTT 20 ms、带宽 100 Mbps 的 TCP 连接，窗口至少多大才能充分利用链路？1500 字节的包在 10 Gbps 和 1 Gbps 上串行化延迟各多少？

## A
- BDP = 100×10⁶ bit/s ÷ 8 × 0.02 s = 12.5 MB/s × 0.02 s = **250 KB**；窗口小于它，发送方会停下来等 ACK，链路填不满。
- 串行化：1500 × 8 = 12000 bit；10 Gbps：12000 / 10¹⁰ = **1.2 µs**；1 Gbps：**12 µs**。
