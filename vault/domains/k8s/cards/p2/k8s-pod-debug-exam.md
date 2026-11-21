---
id: k8s-pod-debug-exam
node: p2.t01.pod-logs-exec-port-forward-ephemeral-containers
type: qa
step: 2
tags: [考点]
---
## Q
**与 Pod 交互 · 考点**｜考点 · 必会

一个 Pod 的 `RESTARTS` 在不断增加。`kubectl logs <pod>` 只看到刚启动的一两行，看不出为什么崩。你接下来怎么查？另外，镜像是不带 shell 的精简镜像，`kubectl exec -it <pod> -- sh` 报找不到 `sh`，怎么办？

## A
**日志：** 加 `--previous`，看上一个（已崩溃的）容器的输出。`logs` 默认给的是当前这个刚重启的容器。

```bash
kubectl logs mypod --previous            # 崩溃前最后的输出
kubectl describe pod mypod               # 看 Last State：退出码、原因（如 OOMKilled（内存超限被杀）、Error）
```

**没有 shell：** 用临时调试容器。

```bash
kubectl debug -it mypod --image=busybox:1.36 --target=app -- sh
```

| 问题 | 工具 |
|---|---|
| 容器崩溃，想看崩溃原因 | `logs --previous` + `describe` 里的 Last State 和退出码 |
| 容器里没有 sh | `kubectl debug` 加临时容器 |
| 想在本机浏览器访问一个没暴露的服务 | `port-forward` |
| 想看某个容器的输出 | 多容器时用 `-c` 指定 |

- **别用 exec 修东西：** 在运行的容器里手工改的东西，容器一重建就没了。排障完要回到改 manifest。

**出处：** KIA2 §5.3；KIA2 §6.1（container 状态里的 Last State 与退出码）
