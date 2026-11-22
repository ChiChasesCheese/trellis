---
id: k8s-kube-proxy-exam
node: p4.t04.kube-proxy-service-dataplane-iptables-nftables
type: qa
step: 2
tags: [考点]
---
## Q
**切到 nftables**｜考点 · 必会

你们的集群有 8000 个 Service，iptables 模式下 Service 变化后规则同步很慢，新连接的第一个包延迟偏高。打算换成 nftables。要先检查什么？切换要重启 node 吗？

## A
**为什么 iptables 在这里吃力：** 包要顺序对照所有 Service 规则，查找是 O(n)；Service 或端点一变，大量规则要重写。nftables 用 map 查找，近似 O(1)，同步也只写有变化的部分。

| 先检查 | 原因 |
|---|---|
| **内核版本 ≥ 5.13** | nftables 模式在旧内核上不工作 |
| node 上的 `nft` 命令版本不能太旧（早于 1.0.0 有 bug） | 避免干扰系统上其他用 nftables 的东西 |
| CNI 和 NetworkPolicy 的实现是否支持 nftables 模式 | 它们若直接操作或覆盖 kube-proxy 的 iptables 规则就会出问题 |
| 监控是否按 iptables 规则取数 | 没更新的观测工具在 nftables 模式下可能看到更少的数据 |
| **行为差异：** nftables 模式下，**NodePort 只在 node 的默认 IP 上可达**，不再是 `127.0.0.1` 和所有 IP | 依赖 localhost:NodePort 的做法会坏 |

**怎么切：** kube-proxy 配置里写 `mode: nftables`（或参数 `--proxy-mode nftables`），然后**重启 kube-proxy 的 Pod**；**不用重启 node**，它启动时会清掉旧的 iptables 或 ipvs 规则。

- **显式写出 mode：** 文档建议每个集群都显式配置，免得将来默认值改成 nftables 时，升级悄悄换掉你的后端。
- **从 ipvs 迁移：** ipvs 已弃用，推荐迁到 nftables；内核太旧用不了 nftables 的，改用 iptables。

<details class="pt" markdown="1"><summary>出处</summary>

kubernetes.io 博客 2025-02-28「NFTables mode for kube-proxy」（内核 5.13、nft 版本、NodePort 差异、切换方式）；Reference › Virtual IPs and Service Proxies

</details>
