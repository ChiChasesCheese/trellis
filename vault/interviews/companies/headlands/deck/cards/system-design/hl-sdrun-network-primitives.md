---
id: hl-sdrun-network-primitives
node: system-design.how-to-run
type: qa
step: 29
---
## Q
交易系统网络里的内核旁路、市场数据组播、订单入口、co-location 各是什么？

## A
- **内核旁路**：绕过内核协议栈，应用直接从网卡环形队列读写（DPDK 轮询模式驱动；Solarflare OpenOnload / ef_vi 一类用户态栈）。省系统调用、中断、内核到用户的拷贝、调度唤醒；代价是独占核心 100% 忙等、特殊网卡和驱动、调试困难、Java 要借 JNI / FFM 或对 socket 透明的用户态栈。
- **市场数据组播**：交易所用 UDP 组播把行情同时发给所有订阅者（一份数据，网络复制），不可靠，靠**序号 + 缺口检测 + A/B 双路冗余 + 快照 / 重传通道**保证完整。
- **订单入口**：TCP 会话（FIX 或交易所专有二进制协议），带会话序号、心跳、断线重发；常见安全网**断线即撤（cancel-on-disconnect）**。
- **co-location**：服务器放进交易所机房，物理距离几十米，往返几微秒；交叉连接线缆长度也被当作公平性的一部分。
