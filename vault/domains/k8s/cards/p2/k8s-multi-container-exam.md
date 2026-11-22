---
id: k8s-multi-container-exam
node: p2.t01.multi-container-pod-init-containers-native-sidec
type: qa
step: 2
tags: [考点]
---
## Q
**Init containers 与 native sidecars**｜考点 · 必会

一个批处理任务（Job，跑完就该结束的 Pod）里有两个容器：做事的 `worker` 和做日志转发的 `shipper`。`worker` 跑完退出了，Pod 却一直不结束，Job 一直不算完成。为什么？怎么改？

## A
**原因：** `shipper` 是个一直跑的普通容器，永远不退出。只要还有一个容器在跑，Pod 就不会结束，Job 也就一直等着。

**改法：** 把 `shipper` 改成 native sidecar：

```yaml
spec:
  initContainers:
  - name: shipper
    image: log-shipper:1.0
    restartPolicy: Always      # native sidecar
  containers:
  - name: worker
    image: batch:1.0
```

| | 普通容器当 sidecar | native sidecar |
|---|---|---|
| 主容器退出后 | sidecar 继续跑，Pod 不结束 | Kubernetes 在主容器都结束后会终止 sidecar，Pod 才能结束 |
| 启动 | 和主容器同时 | 先于主容器 |
| 崩溃 | 看 Pod 的 restartPolicy | 自己被重启 |

- **反过来的坑：** init container 不能是常驻的，它必须能退出，否则主容器永远不启动。要常驻，就用 `restartPolicy: Always` 让它成为 sidecar。

<details class="pt" markdown="1"><summary>出处</summary>

KIA2 §5.5；Job 与 native sidecar 的关系见 kubernetes.io 发布博客 v1.33

</details>
