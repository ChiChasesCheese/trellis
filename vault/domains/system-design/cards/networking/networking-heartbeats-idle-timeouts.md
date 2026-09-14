---
id: networking-heartbeats-idle-timeouts
node: networking.realtime
type: qa
---
## Q
Why do long-lived connections need application-level ping/pong when TCP already has keepalive?

## A
A dead peer with no traffic is pure silence — indistinguishable from idle. TCP keepalive defaults to **2 hours**, is often disabled by middleboxes, and says nothing about whether the *application* is alive.

App-level heartbeats every ~30 s do two jobs:

- **Detect half-open connections** (peer crashed, network path gone) within seconds — miss N pongs → close and reclaim the socket, registry entry, and queues.
- **Refresh idle timers** in NATs, LBs, and proxies, which commonly kill connections idle for ~60 s.

Heartbeat interval must therefore be shorter than the smallest idle timeout on the path.

## Q zh
为什么长生命周期连接需要应用级 ping/pong 当 TCP 已经有 keepalive？

## A zh
死对等体没有流量是纯沉默 — 与空闲无法区分。TCP keepalive 默认为**2 小时**，通常被中间盒禁用，并且对**应用**是否活着一无所知。

应用级心跳每约 30 s 做两项工作：

- **检测半开连接**（对等体崩溃、网络路径消失）在数秒内 — 缺少 N 个 pong → 关闭并回收套接字、注册表条目和队列。
- **刷新 NAT、LB 和代理中的空闲定时器**，这些通常会杀死空闲约 60 s 的连接。

心跳间隔因此必须短于路径上最小的空闲超时。
