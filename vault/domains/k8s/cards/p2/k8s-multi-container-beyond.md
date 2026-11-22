---
id: k8s-multi-container-beyond
node: p2.t01.multi-container-pod-init-containers-native-sidec
type: qa
step: 3
tags: [拓展]
---
## Q
**Native sidecar · 2026 实践**｜拓展 · v1.33 GA

你在网上看到两种写 sidecar 的方式：放进 `containers`，或者放进 `initContainers` 加 `restartPolicy: Always`。2026 年该用哪种？

## A
**一句话：** 用 native sidecar（`initContainers` + `restartPolicy: Always`）。**v1.33 GA**。

| 版本 | 状态 |
|---|---|
| v1.28 起 | 书里说：Kubernetes 开始原生支持 sidecar |
| v1.33 | GA |

| 用途 | 为什么适合 native sidecar |
|---|---|
| 日志收集、指标代理 | 要在主容器启动前就绪、关闭时最后退出 |
| 服务网格的网络代理 | 如果 init 容器也需要联网，sidecar 要先于它们起来（init 容器排在它后面就能用上它） |
| Job 里的辅助进程 | 主容器结束后 sidecar 会被终止，Job 能正常完成 |

- **迁移：** 把原来 `containers` 里的 sidecar 挪到 `initContainers`，加一行 `restartPolicy: Always`。
- **仍然适合普通容器的：** 不需要这些顺序保证的并列容器。

<details class="pt" markdown="1"><summary>出处</summary>

kubernetes.io 发布博客 v1.33（KEP-753，sidecar GA）；KIA2 §5.5（native sidecar，自 v1.28）

</details>
