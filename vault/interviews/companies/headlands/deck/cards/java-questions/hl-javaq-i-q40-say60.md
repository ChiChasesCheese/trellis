---
id: hl-javaq-i-q40-say60
node: java-questions.i-network
type: qa
step: 11
---
## Q
用英文 60 秒回答：Explain TCP basics relevant to latency: handshake, Nagle's algorithm, delayed ACK, `TCP_NODELAY`.

## A
结构：TCP 提供可靠有序字节流 → Nagle 加延迟 ACK 叠加造成卡顿 → 修法：一条消息一次 write 加 NODELAY → 诚实限定：在 Mac 上没复现，要到目标 Linux 上用 ss -ti 和抓包确认。

> "TCP gives a reliable ordered byte stream: a three-way handshake, sequence numbers and acknowledgements, retransmission, and congestion control. For latency, the classic trap is Nagle's algorithm interacting with delayed ACKs: if you write a header and a body as two small writes, Nagle holds the second until the first is acknowledged, while the receiver delays that ACK waiting to piggyback - on Linux that can add tens of milliseconds. The fix is to send each message in one write and set `TCP_NODELAY`. In Java it's `setTcpNoDelay(true)`. I tried a two-write pattern on my Mac and didn't reproduce the stall - loopback behaves differently - so I'd confirm on the target Linux with `ss -ti` and a packet capture."
