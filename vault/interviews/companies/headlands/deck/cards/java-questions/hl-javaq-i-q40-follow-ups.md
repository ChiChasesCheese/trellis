---
id: hl-javaq-i-q40-follow-ups
node: java-questions.i-network
type: qa
step: 4
---
## Q
追问：为什么交易系统更爱用长连接？行情用 TCP 还是 UDP？
Why are long-lived connections better for trading systems? TCP vs UDP for market data?

## A
- **长连接**：避免三次握手的 RTT 和慢启动，可预热拥塞窗口。
- **行情用 UDP 多播**：无连接、无重传延迟；丢包用序号检测，并另路补发。
- **订单用 TCP**：要可靠、有序。
