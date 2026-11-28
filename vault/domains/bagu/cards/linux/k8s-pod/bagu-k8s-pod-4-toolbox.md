---
id: bagu-k8s-pod-4-toolbox
node: a.linux.k8s-pod
type: qa
step: 4
---
## Q
**Kubernetes Pod · 排查命令各看什么**｜加分

面试官：「describe、logs、events、exec、debug、port-forward 这几个 kubectl 命令，分别在排查的哪一步用，各能看到什么？」

## A
**基本回答。** `describe` 看状态和事件，先回答「它处在什么状态、为什么」；`logs` 看容器自己的输出；`get events` 看整个命名空间按时间排列的事件；`exec` 进入正在运行的容器里看；`debug` 在容器没有调试工具或已经崩溃时，挂一个带工具的临时容器；`port-forward` 绕过服务和网关，直接连到某一个 Pod 上验证。
常用参数：`logs --previous` 看崩溃前的日志，`-f` 跟随，`--since=10m`、`--tail=200` 限范围；初始化容器失败（`Init:CrashLoopBackOff`）要加 `-c <init容器>`。`kubectl get events --sort-by=.lastTimestamp` 事件默认只保留 1 小时，要趁早或导出到日志系统。`exec` 要求容器在运行且镜像里有 shell；精简镜像用 `kubectl debug -it <pod> --image=busybox:1.36 --target=<container>` 挂临时容器（ephemeral container），能看到目标容器的进程。`port-forward` 用来判断问题在 Pod 还是在 Service、Ingress 这些转发层。
**举个例子。** 一个服务发布后延迟升高、部分请求超时：
1. **看全局：** `kubectl get pod -o wide` 发现 3 个 Pod 里有 1 个 READY 是 `0/1`，它被摘掉了流量，全部请求压在另外两个上。
2. **看状态：** `describe` 显示就绪探针失败，Events 里是 `Readiness probe failed: connection refused`，应用端口还没开始监听。
3. **看日志：** `logs` 显示应用卡在启动阶段，一直在重试连接配置中心。
4. **进去验证：** `exec` 进容器 `nc -zv config-center 8848` 连不上，另两个 Pod 能连上；这个 Pod 落在新扩容的节点上，那批节点所在子网的安全组没有放行配置中心的端口。
5. **绕过转发层确认：** 修正安全组后，对这个 Pod `port-forward` 直连它的健康检查接口，返回正常，READY 变成 `1/1`，延迟恢复。
**代码。** 常用组合：
```bash
kubectl describe pod <pod>
kubectl logs <pod> -c app --previous --tail=200
kubectl get events --sort-by=.lastTimestamp --field-selector involvedObject.name=<pod>
kubectl exec -it <pod> -c app -- sh
kubectl debug -it <pod> --image=busybox:1.36 --target=app
kubectl port-forward pod/<pod> 8080:8080
```
**容易错。**
- **先 exec 进去乱翻：** 容器已经崩溃时 exec 进不去，而 describe 和 `logs --previous` 早就写着原因。
- **多容器 Pod 不加 `-c`：** 有边车容器（sidecar）时，不指定容器看到的可能是别的容器的日志。
- **事件过了一小时再查：** 事件已经被清理，只能靠导出的日志。
- **在生产容器里装工具：** `exec` 进去 `apt install` 会改变现场，也可能被安全策略禁止，用 `kubectl debug` 的临时容器代替。
