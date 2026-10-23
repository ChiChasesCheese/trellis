---
id: hl-net-headers-mss
node: foundations.networking-basics
type: qa
step: 3
---
## Q
以太网上 TCP 最大段长（MSS）是多少？UDP 数据报不分片的最大载荷是多少？为什么交易所行情包刻意不超过它？

## A
各层头部：以太网头 14 B、IPv4 头 20 B、TCP 头至少 20 B、UDP 头 8 B。MTU 为 1500。

- TCP：MSS = 1500 − 20 − 20 = **1460 字节**；
- UDP：1500 − 20 − 8 = **1472 字节**。

载荷超过 MTU 的数据报会被 IP 层分片，任一片丢了整个数据报作废，所以交易所行情包通常刻意不超过 1472 字节。
