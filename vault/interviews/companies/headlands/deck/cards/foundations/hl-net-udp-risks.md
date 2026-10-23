---
id: hl-net-udp-risks
node: foundations.networking-basics
type: qa
step: 15
---
## Q
「UDP 不可靠」是否等于「一定丢包」？UDP 有哪两个特有风险，各怎么应对？

## A
内部数据中心网络里 UDP 丢包很少。可靠性靠**应用层**补：给消息编号、接收方检测缺口、缺失时请求重传。放在应用层，应用才能决定怎么补（等重传、忽略、还是用快照覆盖），比 TCP 的「一律等」灵活。

两个风险：
1. **接收缓冲区溢出**：`receive` 太慢，内核缓冲区（`SO_RCVBUF`）满了，新包被**静默丢弃**（Linux 上 `netstat -su` 的 `receive buffer errors` 增长）。对策：加大 `SO_RCVBUF`，接收线程只做最少的事、立刻取走交给别的线程，绑核。
2. **分片**：载荷 > MTU 的数据报被分片，任一片丢了整个作废。对策：每个数据报 ≤ 1472 字节。
