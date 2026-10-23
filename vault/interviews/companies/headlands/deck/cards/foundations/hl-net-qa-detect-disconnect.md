---
id: hl-net-qa-detect-disconnect
node: foundations.networking-basics
type: qa
step: 45
---
## Q
面试题：TCP 连接断开后应用怎么知道？对端机器直接断电呢？

## A
推荐答法：
- `read` 返回 **-1**：对端正常关闭，发了 FIN；
- 抛 `IOException`：RST 或超时；
- 对端机器直接断电则**没有任何包**，本端只能靠应用层心跳或 TCP keepalive（默认两小时）发现，所以交易网关都有**应用层心跳**。
