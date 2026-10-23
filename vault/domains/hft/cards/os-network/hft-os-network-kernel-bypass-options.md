---
id: hft-os-network-kernel-bypass-options
node: os-network.kernel-bypass
type: qa
step: 2
---
## Q
实现内核旁路有哪几种常见的技术（OpenOnload、ef_vi、DPDK、RDMA）？它们各自的定位有什么不同？

## A
| 技术 | 特点 | 适合 |
|---|---|---|
| OpenOnload | Solarflare（现属 AMD）网卡的用户态协议栈，通过 `LD_PRELOAD` 拦截标准 socket 调用，**应用代码几乎不用改** | 想以最小代价把现有 socket 程序加速到约 1–2 µs |
| ef_vi | 同一厂商网卡的底层 API，直接操作收发队列，没有 socket 语义，由应用自己解析包 | 追求极限延迟、愿意自己写收发代码（约 1 µs 或更低） |
| DPDK | 通用的用户态包处理框架，用轮询驱动接管支持的网卡，数据路径全在用户态，需要自己实现或集成 UDP/TCP 栈 | 需要跨厂商网卡、做高吞吐包处理（如网络设备、监控） |
| RDMA | 网卡之间直接读写对方内存，绕过双方 CPU，延迟约 1–2 µs | 数据中心内部机器之间的通信，较少用在交易所接入 |

选择思路：
- 交易所接入（收组播行情、发 TCP 订单）常见的是 OpenOnload 与 ef_vi 一类的厂商方案；
- 想少改代码，用 OpenOnload；想榨干延迟，用 ef_vi；
- DPDK 更常见于网络设备和高吞吐场景。

重点不是背名字，而是明白它们都在做同一件事：把网卡队列交给用户态轮询。
