---
id: infra-mesh-sidecar-intercept
node: infra.mesh
type: qa
---
## Q
Mechanically, what does a service-mesh sidecar do to a pod's traffic — and why does intercepting at that point enable every mesh feature?

## A
At pod startup, iptables rules are installed that transparently **redirect all inbound and outbound TCP through an L7 proxy (Envoy) running in the same pod**. The application is unmodified and unaware — it thinks it's talking to the network.

Because every byte now crosses a proxy on both ends of a call, the mesh can: terminate/originate **mTLS**, parse HTTP/gRPC for **per-request metrics and traces**, enforce **retries, timeouts, and authz policy**, and route by header or percentage — all pushed from a control plane as config, with zero application code.

## Q zh
机械上，服务网格 sidecar 对 pod 的流量做什么——为什么在那一点截取启用每个网格特性？

## A zh
在 pod 启动，iptables 规则被安装，它透明地**将所有入站和出站 TCP 重定向到同一 pod 中运行的 L7 proxy（Envoy）**。应用被无修改并无感知——它认为在与网络说话。

因为每个字节现在跨越调用两端的 proxy，网格可以：终止/发起 **mTLS**，解析 HTTP/gRPC 为**每请求指标和跟踪**，强制**重试、超时和 authz 策略**，并按头或百分比路由——全部从控制平面作为配置推送，零应用代码。
