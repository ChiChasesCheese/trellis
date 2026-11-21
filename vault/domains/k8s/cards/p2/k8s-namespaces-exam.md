---
id: k8s-namespaces-exam
node: p2.t03.namespaces
type: qa
step: 2
tags: [考点]
---
## Q
**Namespaces · 考点**｜考点 · 必会

你在 `dev` 命名空间里有一个 Service 叫 `db`。`prod` 里的应用写 `db:5432` 连不上，写什么才对？另外，你对着 `dev` 命名空间执行 `kubectl delete namespace dev`，会发生什么？

## A
**连接：** `db` 这种短名字只在**本命名空间**内解析。跨命名空间要写 `db.dev`（或完整的 `db.dev.svc.cluster.local`）。

| 操作 | 结果 |
|---|---|
| `db` | 在 `prod` 里找 `prod` 的 `db`，找不到 |
| `db.dev` | 指向 `dev` 命名空间里的 `db` |
| `kubectl delete namespace dev` | `dev` 里**所有**对象（Pod、Service、ConfigMap（存放配置键值的对象，第 3 部分细讲）、Deployment 等）全部被删，没有二次确认 |

- **名字唯一性：** 同一命名空间内同类型对象不能同名；不同命名空间可以。
- **提醒：** 删命名空间是最危险的 kubectl 命令之一。操作前先看 `kubectl config get-contexts`，确认当前指向哪个集群。
- **不属于命名空间：** Node、PersistentVolume（集群级的持久存储卷，第 3 部分细讲） 这类集群范围对象，不会被它删掉。

**出处：** KIA2 §7.1；Poulton ch5（default namespaces，cross-namespace）
