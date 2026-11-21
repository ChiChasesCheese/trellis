---
id: k8s-controller-prereq
node: p1.t04.controller
type: qa
step: 1
tags: [先修]
---
## Q
**Controller 是什么 · 先修**｜先修 · 必会

`kubectl apply` 只是把一份 YAML 交给了 API server。之后是谁真的去创建 Pod、换掉坏掉的 Pod？这类角色叫什么？

## A
**一句话：** controller 是一个一直在跑的程序。它盯着某一类对象，发现现实和对象里写的 `spec` 不一样，就动手把现实改过去。

| Controller | 盯着什么 | 做什么 |
|---|---|---|
| Deployment controller | Deployment | 按模板建 ReplicaSet，升级时新旧交替 |
| ReplicaSet controller | ReplicaSet | 保证 Pod 数量刚好等于 `replicas` |
| Node controller | Node | 机器失联了，把它标成不可用 |

- **住在哪：** 内置的 controller 都在 control plane 的 **kube-controller-manager** 进程里。
- **怎么知道变化：** 只和 API server 说话。它 **watch** API server，有变化会被通知；要改东西，也只通过 API server。
- **它不做什么：** 不决定 Pod 放哪台机器（那是 **scheduler**），也不真的启动容器（那是每台 node 上的 **kubelet**）。
- **为什么这样设计：** 每个 controller 只管一件事，坏了一个不影响别的。你也能自己写 controller 管自己的对象（第 8 部分的 operator）。

**下一张：** controller 的工作方式就是 reconcile loop（下一张细讲）。

**出处：** Poulton ch2；kubernetes.io Concepts › Controllers
