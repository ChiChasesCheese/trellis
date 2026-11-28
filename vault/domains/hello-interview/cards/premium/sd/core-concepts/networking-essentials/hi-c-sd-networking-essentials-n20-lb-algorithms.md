---
id: hi-c-sd-networking-essentials-n20-lb-algorithms
node: sd.core-concepts.networking-essentials.notes
type: qa
step: 20
---
## Q
**网络基础 · 负载均衡算法与实现**｜摘要 · 必会

常见的调度算法有哪些？无状态服务和长连接服务各选哪个？负载均衡器有哪几类实现？

## A
- **算法：** 轮询（依次分发）、随机、最少连接（给活跃连接最少的服务器）、最短响应时间、IP 哈希（客户端 IP 决定目标，可用于会话保持）。
- **无状态服务：** 轮询或随机通常足够，因为没有哪台服务器会特别受欢迎。新服务器加入均衡器时，这些算法自然开始向它分发流量，不需特殊配置。
- **长连接服务（SSE、WebSocket）：** 最少连接是好选择，避免某一台服务器逐渐积累所有的活跃连接。
- **实现，硬件：** 如 F5 Networks BIG-IP。**软件：** HAProxy、NGINX、Envoy。**云：** AWS ELB / ALB / NLB、Google Cloud Load Balancing、Azure Load Balancer。
- **规模：** 硬件均衡器的吞吐高于软件均衡器。扩展均衡器几乎不是软件工程师面试的内容（网络专长岗位除外），吞吐很大时提一句硬件均衡器就是好的出路。
