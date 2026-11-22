---
id: k8s-service-clusterip-exam
node: p4.t01.service-clusterip
type: qa
step: 2
tags: [考点]
---
## Q
**Service 与 ClusterIP**｜考点 · 必会

下面两个 Service 都「创建成功」，但访问不通。分别为什么？
```yaml
# A：Pod 的标签是 app: kiada，容器监听 8080
spec:
  selector: {app: kiadaa}
  ports: [{port: 80, targetPort: 8080}]
---
# B：Pod 的标签是 app: kiada，容器监听 8080
spec:
  selector: {app: kiada}
  ports: [{port: 80, targetPort: 80}]
```

## A
| | 问题 | 现象 | 怎么查 |
|---|---|---|---|
| A | selector 多写了一个 `a`，匹配不到任何 Pod | 后端列表是空的，连接被拒或超时 | `kubectl get endpointslices -l kubernetes.io/service-name=kiada`，没有地址 |
| B | `targetPort` 写成了 80，Pod 里没人听 | 有后端，但连接被拒绝 | 对照容器真正监听的端口 |

```bash
kubectl get endpointslices -l kubernetes.io/service-name=kiada
kubectl get pods -l app=kiada      # 先确认 selector 真的能选到 Pod
```

- **规律：** Service 不会因为「选不到 Pod」报错，只是后端为空。
- **排查顺序：** selector 能选到 Pod 吗 → 这些 Pod Ready 吗 → `targetPort` 对吗。
- **`port` 与 `targetPort` 不同是正常的：** 外面连 80，里面转到 8080。

<details class="pt" markdown="1"><summary>出处</summary>

KIA2 §11.1；Poulton ch9

</details>
