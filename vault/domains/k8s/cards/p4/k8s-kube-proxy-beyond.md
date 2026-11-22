---
id: k8s-kube-proxy-beyond
node: p4.t04.kube-proxy-service-dataplane-iptables-nftables
type: qa
step: 3
tags: [拓展]
---
## Q
**kube-proxy 模式的时间线 · 2026 实践**｜拓展 · v1.33 / v1.35 / v1.37

你的 kube-proxy 配置还是 `mode: ipvs`。2026 年它什么处境？默认值会变吗？

## A
| 时间 | 事件 |
|---|---|
| v1.31 起 | 传 `--proxy-mode nftables` 即可启用（先前为 beta） |
| **v1.33** | nftables 后端 **GA**；为了兼容，Linux 默认仍是 iptables（KEP-3866） |
| **v1.35** | **ipvs 模式弃用**：kube-proxy 启动时打警告；官方让 Linux node 开始迁到 nftables（KEP-5495） |
| v1.37 | 发布博客再次确认 ipvs 弃用时间表：ipvs 将在 **v1.40 起默认关闭**（可用 feature gate 重新开启），**v1.43 完全移除**；默认仍是 iptables，将来会改成 nftables |

```yaml
# KubeProxyConfiguration
mode: nftables     # 显式写，不要依赖默认值
```

- **行动：** 先在测试集群确认内核、CNI 都支持，再逐个节点池切换，**mode 一定显式写**。
- **ipvs 为什么退场：** 内核 IPVS 接口和 Service API 不太匹配，维护成本高；nftables 性能不输它。
- **开箱即用的变化：** 有些 CNI 自己实现 Service 转发，完全不用 kube-proxy（下一卡）。

**出处：** kubernetes.io 发布博客 v1.33（nftables GA，iptables 仍为默认，KEP-3866）、v1.35（Deprecation of ipvs mode，KEP-5495）；v1.37 发布博客（Deprecating kube-proxy's support for ipvs mode，KEP-5495）；Reference › Virtual IPs and Service Proxies（v1.40 起默认关闭、v1.43 移除）
