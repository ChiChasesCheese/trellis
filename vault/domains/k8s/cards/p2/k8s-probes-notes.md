---
id: k8s-probes-notes
node: p2.t02.restart-policy-probes-liveness-readiness-startup
type: qa
step: 1
tags: [摘要]
---
## Q
**Probes 与 restart policy · 摘要**｜摘要 · 必会

liveness、readiness、startup 三种 probe 各问什么？探针失败时分别会发生什么？

## A
| Probe | 问的问题 | 失败后果 |
|---|---|---|
| **liveness** | 应用还活着吗？ | kubelet **重启**容器 |
| **readiness** | 现在能接流量吗？ | 从 Service 的后端里**摘掉**，不重启；恢复后加回来 |
| **startup** | 启动完了吗？ | 通过之前，liveness 和 readiness 都不执行；一直失败则重启容器 |

```yaml
containers:
- name: app
  image: kiada:1.0
  startupProbe:            # 慢启动应用：给足启动时间
    httpGet: {path: /healthz, port: 8080}
    failureThreshold: 30
    periodSeconds: 10
  livenessProbe:
    httpGet: {path: /healthz, port: 8080}
    periodSeconds: 5
    failureThreshold: 3
  readinessProbe:
    httpGet: {path: /ready, port: 8080}
    periodSeconds: 5
```

- **探针方式：** HTTP GET、在容器里执行命令（exec）、TCP 连接某个端口。
- **参数：** `initialDelaySeconds` 第一次探测前等多久；`periodSeconds` 多久探一次；`failureThreshold` 连续失败几次才算失败。
- **restartPolicy：** Pod 级别，`Always`（默认）/`OnFailure`/`Never`，决定容器退出后要不要重启。Job 的 Pod 用 `OnFailure` 或 `Never`。
- **CrashLoopBackOff：** 容器反复崩溃时，kubelet 的重启间隔指数增长。

**出处：** KIA2 §6.2（Keeping containers healthy）；kubernetes.io Tasks › Configure Liveness, Readiness and Startup Probes
