---
id: bagu-k8s-pod-2-pending
node: a.linux.k8s-pod
type: qa
step: 2
---
## Q
**Kubernetes Pod · 一直 Pending**｜追问

面试官：「一个 Pod 一直是 Pending，没有任何日志。怎么查？常见原因有哪些？」

## A
**基本回答。** Pending 说明 Pod 还没被调度到任何节点，容器根本没启动，所以没有日志。看 `kubectl describe pod` 最下面的 Events，调度器会写明「多少个节点里，各有几个因为什么原因被排除」，再按原因去查节点资源、污点、亲和性或存储卷。
Events 里是 `FailedScheduling`，形如 `0/5 nodes are available: 3 Insufficient memory, 1 node(s) had untolerated taint ...`。原因：资源不足（只按 requests 算，不看实际用量；`describe node` 的 `Allocated resources` 看已申请量，GPU 这类扩展资源如 `nvidia.com/gpu` 同理）、污点没有对应容忍（如 `dedicated=gpu:NoSchedule`）、`nodeSelector` / `nodeAffinity` 没有匹配节点、PVC 没绑定（`unbound immediate PersistentVolumeClaims`）。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 258">
<rect x="6" y="8" width="150" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="81" y="29.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5 个节点</text>
<text x="168" y="29.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">调度器逐个过滤</text>
<line x1="81" y1="42" x2="81" y2="47" stroke-width="1.2" stroke="currentColor"/>
<polygon points="81,54 77.8,47 84.2,47" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="54" width="150" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="81" y="75.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">requests 放得下吗</text>
<text x="168" y="75.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">3 个：Insufficient memory</text>
<line x1="81" y1="88" x2="81" y2="93" stroke-width="1.2" stroke="currentColor"/>
<polygon points="81,100 77.8,93 84.2,93" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="100" width="150" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="81" y="121.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">污点能容忍吗</text>
<text x="168" y="121.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1 个：untolerated taint</text>
<line x1="81" y1="134" x2="81" y2="139" stroke-width="1.2" stroke="currentColor"/>
<polygon points="81,146 77.8,139 84.2,139" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="146" width="150" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="81" y="167.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">亲和性满足吗</text>
<text x="168" y="167.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1 个：亲和性不匹配</text>
<line x1="81" y1="180" x2="81" y2="185" stroke-width="1.2" stroke="currentColor"/>
<polygon points="81,192 77.8,185 84.2,185" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="192" width="150" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="81" y="213.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">剩 0 个</text>
<text x="168" y="213.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Pending：看 Events 原因</text>
<text x="6" y="254" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">按 requests 算，不是按节点实际用了多少</text>
</svg>
调度器把所有节点逐层过滤，每一层把不合格的节点和原因记下来；蓝色那步说明一个都不剩，原因就写在 Events 里。
**举个例子。** 一个新部署的任务 Pod 一直 Pending：
1. **看状态：** `kubectl get pod -o wide` 显示 `Pending`，NODE 一栏是 `<none>`，说明没被调度。
2. **看 Events：** `0/5 nodes are available: 3 Insufficient memory, 1 node(s) had untolerated taint {dedicated: gpu}, 1 node(s) didn't match Pod's node affinity/selector`。
3. **看资源：** Pod 的 `requests.memory` 写成了 `64Gi`，而普通节点每台只有 32 GiB 可分配，再空也放不下。
4. **定位：** 是复制配置时把另一个任务的 requests 带了过来，改成实际需要的 `4Gi` 后立即被调度。
5. **另外两类：** 污点那个节点是专用机，本来就不该放；亲和性那个节点标签不对，可以不管。
**代码。** 排查命令：
```bash
kubectl get pod <pod> -o wide                       # NODE 为 <none>：没调度上
kubectl describe pod <pod> | sed -n '/Events:/,$p'  # 只看事件
kubectl describe node <node> | grep -A 8 'Allocated resources'
kubectl get nodes -o custom-columns=NAME:.metadata.name,TAINTS:.spec.taints
kubectl get pvc                                     # STATUS 是否 Bound
```
**容易错。**
- **去找容器日志：** Pending 的 Pod 没有启动任何容器，`kubectl logs` 什么也拿不到，信息只在 Events 里。
- **看节点实际用量判断够不够：** `kubectl top node` 显示内存只用了 30%，Pod 照样调度不上，因为调度按 requests 计算，不按实际用量。
- **把 requests 写得过大：** 「保险起见多申请一点」会让集群看起来满了、实际很空，新 Pod 排队 Pending。
- **只看 Pod 不看上一级：** 配额不足时 Pod 都没被创建，要去看 Deployment 和 ReplicaSet 的事件。
**业务场景。** 支付对账月末批处理扩到 20 个 Pod，8 个一直 Pending，Events 是 `Insufficient memory`：批处理和在线服务共用节点池，requests 之和超过可分配量。临时给批处理单独节点池加污点，长期按实际用量重设 requests。
