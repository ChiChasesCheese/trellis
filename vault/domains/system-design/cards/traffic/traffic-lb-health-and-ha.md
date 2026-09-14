---
id: traffic-lb-health-and-ha
node: traffic.load-balancing
type: qa
---
## Q
The load balancer is itself a single point of failure. How is the LB tier made highly available, and what health-check subtlety prevents it from making outages worse?

## A
HA: **redundant LB pairs sharing a virtual IP** (VRRP/keepalived failover), or **anycast/ECMP** spreading one IP across an LB fleet; DNS with multiple records as the coarse outer layer.

Health-check subtlety: distinguish **"this instance is down" from "everything is down."** If all backends fail checks (e.g. a shared dependency blips), removing them all serves 100% errors — use fail-open thresholds ("if >50% unhealthy, keep routing to all") and checks that test the process, not its dependencies.

## Q zh
负载均衡器本身是单点故障。LB 层如何实现高可用，什么健康检查微妙阻止它使故障更糟？

## A zh
HA：**冗余 LB 对共享虚拟 IP**（VRRP/keepalived 故障转移），或**anycast/ECMP** 跨 LB 舰队传播一个 IP；DNS 带多个记录作为粗外层。

健康检查微妙：区分**"这个实例宕机"与"一切都宕机"。** 如果所有后端检查失败（例如共享依赖打嗝），移除它们都服务 100% 错误 — 使用失败打开阈值（"如果 >50% 不健康，继续路由到所有"）和检查测试进程而不是其依赖的检查。
