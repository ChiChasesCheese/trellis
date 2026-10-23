---
id: hl-net-tcp-reliability
node: foundations.networking-basics
type: qa
step: 8
---
## Q
TCP 怎么检测并重传丢失的段？超时重传和快速重传有什么区别？为什么丢包会带来延迟尖刺？

## A
接收方回复的 ACK 表示「我期待的下一个字节序号」。发送方发了 seq=1000、1100、1200 三段，第 2 段丢了，接收方收到第 1、3 段后一直回 `ACK=1100`，发送方发现重复 ACK 或超时就重传 seq=1100。

- **超时重传**：发送后一段时间（RTO，由 RTT 估计）没收到 ACK 就重发。Linux 最小 RTO 是 **200 ms**，一次丢包可能带来 200 ms 延迟尖刺；
- **快速重传**：连续收到 3 个重复 ACK 就立刻重传，不等超时。
