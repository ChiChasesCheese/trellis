---
id: hl-net-time-wait
node: foundations.networking-basics
type: qa
step: 11
---
## Q
TCP 关闭连接要几次挥手？`TIME_WAIT` 是什么、持续多久、频繁短连接会有什么后果？

## A
关闭用四次挥手（FIN / ACK）。**主动关闭的一方**进入 `TIME_WAIT`，保持约 **60 秒**（Linux），目的是防止延迟到达的旧包被新连接误收。

频繁新建和关闭短连接会让大量 `TIME_WAIT` 耗尽端口，所以再一次：用长连接。
