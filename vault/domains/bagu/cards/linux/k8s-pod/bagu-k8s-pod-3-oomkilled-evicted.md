---
id: bagu-k8s-pod-3-oomkilled-evicted
node: a.linux.k8s-pod
type: qa
step: 3
---
## Q
**Kubernetes Pod · OOMKilled 与驱逐**｜追问

面试官：「OOMKilled 和 Evicted 都和内存有关，有什么区别？分别怎么查、怎么防？」

## A
**基本回答。** OOMKilled 是一个容器用的内存超过了它自己的 limit，内核在这个容器里杀进程，容器在原节点重启；Evicted 是整个节点内存紧张，kubelet 把整个 Pod 赶走，Pod 变成失败状态，由控制器在别处重建。前者调 limit 或修泄漏，后者合理设置 requests 和 QoS 等级。
OOMKilled：limit 是写进容器 cgroup 的硬上限，超了内核 OOM Killer 杀进程，退出码 137，`describe` 的 Last State 显示 `OOMKilled`。Evicted：节点 `memory.available` 低于驱逐阈值（默认 `<100Mi`）时 kubelet 驱逐 Pod，状态 `Failed`、Reason `Evicted`。驱逐顺序：先看谁实际用量超过 requests，再看优先级；QoS 里 BestEffort（没设 requests / limits）最先走，Burstable 居中，Guaranteed（requests = limits）最后。防 OOMKilled：limit 按真实峰值加余量设，JVM 用 `-XX:MaxRAMPercentage=75`；防 Evicted：requests 贴近真实用量，核心服务用 Guaranteed，节点留 `--system-reserved`、`--kube-reserved`。页缓存计入 cgroup 内存但可回收，kubelet 判断压力看 working set。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="85" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">容器级</text>
<rect x="4" y="26" width="162" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">容器超过自己的</text>
<text x="85" y="60" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">内存 limit</text>
<line x1="85" y1="70" x2="85" y2="79" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85,86 81.8,79 88.2,79" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="4" y="86" width="162" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">内核 OOM Killer</text>
<text x="85" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">杀掉容器里的进程</text>
<line x1="85" y1="130" x2="85" y2="139" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85,146 81.8,139 88.2,139" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="4" y="146" width="162" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="85" y="164" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">OOMKilled，退出码 137</text>
<text x="85" y="180" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">同一节点原地重启</text>
<text x="255" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">节点级</text>
<rect x="174" y="26" width="162" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点整体</text>
<text x="255" y="60" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">内存不足</text>
<line x1="255" y1="70" x2="255" y2="79" stroke-width="1.2" stroke="currentColor"/>
<polygon points="255,86 251.8,79 258.2,79" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="174" y="86" width="162" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">kubelet 驱逐</text>
<text x="255" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">整个 Pod</text>
<line x1="255" y1="130" x2="255" y2="139" stroke-width="1.2" stroke="currentColor"/>
<polygon points="255,146 251.8,139 258.2,139" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="174" y="146" width="162" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="255" y="164" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Evicted，Pod 失败</text>
<text x="255" y="180" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">控制器在别处重建</text>
<text x="6" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">驱逐顺序：BestEffort → 超出 requests 的</text>
<text x="6" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Burstable → Guaranteed</text>
</svg>
左边是容器自己超限，右边是节点整体不够；蓝色那步是你在 `kubectl` 里看到的结果。
**举个例子。** 一个视频转码服务：
1. **现象一：** 某个 Pod RESTARTS 是 12，`describe` 的 Last State 是 `OOMKilled`、Exit Code 137。转码 4K 视频时峰值内存 3.5 GiB，而 limit 只有 2Gi。把 limit 调到 4Gi，并限制单个 Pod 同时处理的任务数。
2. **现象二：** 同一节点上另外几个 Pod 状态变成 `Evicted`，消息是节点内存不足。它们都是没写 requests 的 BestEffort 调试任务，在节点紧张时最先被赶走。
3. **区分方法：** `kubectl get pod <pod> -o jsonpath='{.status.containerStatuses[*].lastState.terminated.reason}'` 看是不是 `OOMKilled`；`kubectl get pod <pod> -o jsonpath='{.status.reason}'` 看是不是 `Evicted`。
4. **清理：** 被驱逐的 Pod 记录不会自己消失，`kubectl delete pod --field-selector=status.phase=Failed` 批量清掉。
**代码。** 常用命令：
```bash
kubectl describe pod <pod> | grep -A 5 'Last State'     # OOMKilled、Exit Code 137
kubectl get pod -A --field-selector=status.phase=Failed  # 找被驱逐的 Pod
kubectl describe node <node> | grep -A 6 Conditions      # MemoryPressure 是否为 True
kubectl top pod --containers                             # 当前用量（需要 metrics-server）
kubectl get pod <pod> -o jsonpath='{.status.qosClass}'   # Guaranteed / Burstable / BestEffort
```
**容易错。**
- **看到 137 就以为一定是内存超限：** 137 只说明被 SIGKILL，停止时超过优雅退出时间被强杀也是 137，要看 Reason。
- **只调大 limit：** limit 调大而 requests 不变，节点上能放的 Pod 更多、实际更挤，可能从 OOMKilled 变成整个节点被驱逐。
- **以为驱逐会重启容器：** 驱逐是把 Pod 删除，换节点重建；OOMKilled 才是原地重启容器。
- **不设 requests 和 limits：** 成为 BestEffort，节点一紧张最先被驱逐，而且可能挤占别人的内存。
**业务场景。** 转码服务在活动期间上传量翻倍，单 Pod 并发任务变多、峰值内存超 limit，反复 OOMKilled；同节点没设 requests 的离线任务被驱逐。处理：限制单 Pod 并发、按峰值设 limit，离线任务带上 requests 并调度到单独节点池。
