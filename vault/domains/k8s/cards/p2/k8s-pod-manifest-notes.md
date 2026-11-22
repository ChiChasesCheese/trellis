---
id: k8s-pod-manifest-notes
node: p2.t01.pod-manifest
type: qa
step: 1
tags: [摘要]
---
## Q
**Pod manifest**｜摘要 · 必会

用 YAML 创建一个 Pod，最小的 manifest 长什么样？创建之后读回来的对象为什么比你写的长得多？

## A
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: kiada
spec:
  containers:
  - name: kiada
    image: luksa/kiada:0.1
    ports:
    - containerPort: 8080   # 只是说明，不影响能否访问
```

```bash
kubectl apply -f pod.kiada.yaml   # 创建（也用来更新）
kubectl get pod kiada             # READY / STATUS / RESTARTS
kubectl get pod kiada -o yaml     # 读回完整对象
kubectl describe pod kiada        # 详情 + 底部 Events
```

| 部分 | 写的时候 | 读回来的时候 |
|---|---|---|
| `metadata` | 只有 name | 多出 uid、创建时间、labels、managedFields 等 |
| `spec` | 一个容器 | 补上默认值（restartPolicy、DNS 策略、`nodeName` 等） |
| `status` | 没有 | 由 kubelet 等组件写入 |

- **起草模板：** `kubectl run kiada --image=luksa/kiada:0.1 --dry-run=client -o yaml > mypod.yaml`，`--dry-run=client` 只输出定义，不创建。
- **不会写的字段：** `kubectl explain pods` 查。
- **为什么用 YAML 文件：** 可重复部署，放进版本库有变更历史；JSON 也行，YAML 能写注释。
- **`containerPort` 只是文档：** 不写也能访问，写错也不会拦；但写上并起名字，别人一看就知道端口，后面 Service 也可以按名字引用。

<details class="pt" markdown="1"><summary>出处</summary>

KIA2 §5.2.1–5.2.3

</details>
