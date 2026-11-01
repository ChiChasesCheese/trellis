---
id: hi-sd-networking-essentials-6-lb-algo-health
node: sd.core-concepts.networking-essentials
type: qa
step: 6
---
## Q
**负载均衡算法与健康检查**｜系统设计 · 核心概念

专用负载均衡器通常提供哪些调度算法？无状态服务和长连接服务各该选哪个？健康检查有哪两种？

## A
**要点。** 常见算法：轮询（Round Robin）、随机、最少连接（Least Connections）、最短响应时间、IP 哈希（会话保持）。

**取舍。** 无状态服务用轮询或随机即可，新增服务器后流量会自然分过去，不需要额外配置。提供 SSE 或 WebSocket 的服务用最少连接，避免连接逐渐堆在少数几台机器上。

**健康检查。** 负载均衡器定期探测后端并摘除故障节点，这是高可用的基础。TCP 检查只看能否建立连接，便宜；L7 检查发一个 HTTP 请求，要求返回 200，能识别应用层的 500 或无响应。

**实现。** 硬件均衡器（如 F5）可扛上亿级 QPS，软件均衡器（HAProxy、NGINX、Envoy）和云上均衡器（ALB、NLB）较弱。面试里很少要求自己扩展均衡器，吞吐太大时提一句硬件即可。
