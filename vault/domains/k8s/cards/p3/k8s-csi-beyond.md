---
id: k8s-csi-beyond
node: p3.t03.csi-controller-node-plugin-sidecars
type: qa
step: 3
tags: [拓展]
---
## Q
**CSI 的新变化 · 2026 实践**｜拓展 · v1.35 / v1.36

一个 node 上能挂的卷数量有上限，但 driver 启动后这个数字会变，scheduler 看到的是过期的数，结果 Pod 被安排上去又卡在 `ContainerCreating`。2026 年怎么解决？

## A
| 特性 | 状态 | 作用 |
|---|---|---|
| **mutable CSINode allocatable** | v1.34 beta（默认关）→ v1.35 仍 beta（默认开）→ **v1.36 stable**（KEP #4876） | `CSINode` 里 driver 报告的可挂卷数可以动态更新，kubelet 也会在 attach 因容量不足失败后自动更新，scheduler 用的是新数 |
| CSI driver 用 `secrets` 字段接收 ServiceAccount token | **v1.35 引入**（opt-in：CSIDriver 里设 `serviceAccountTokenInSecrets: true`，KEP #5538） | 以前放在 `volume_context`，容易被 driver 和调试工具明文记进日志；改放专用的 secrets 字段 |

- **以前的症状：** 「卷槽位在 driver 启动之后被占用」，scheduler 以旧的上限判断，Pod 落到容量不足的 node。
- **你要做的：** 升到 v1.36 之后无需额外配置，driver 也需要支持动态上报。
- **排查时：** `kubectl get csinode <node> -o yaml` 看 allocatable。

<details class="pt" markdown="1"><summary>出处</summary>

kubernetes.io 发布博客 v1.35（Mutable Volume attach limits，beta；CSI driver opt-in for service account tokens via secrets field）、v1.36（Mutable CSINode allocatable，Stable）

</details>
