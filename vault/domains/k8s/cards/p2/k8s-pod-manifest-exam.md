---
id: k8s-pod-manifest-exam
node: p2.t01.pod-manifest
type: qa
step: 2
tags: [考点]
---
## Q
**改 Pod manifest · 考点**｜考点 · 必会

你把 `pod.kiada.yaml` 里的 `containerPort` 改成 9999 再 `kubectl apply`，应用还能通过 8080 访问吗？又把容器的 `image` 改成新版本呢？

## A
| 修改 | 结果 | 原因 |
|---|---|---|
| `containerPort: 9999`（应用实际仍监听 8080） | **还能访问 8080** | 这个字段只是说明，不控制网络 |
| 改 `image` | 允许，kubelet 会按新镜像重启这个容器 | 镜像是少数可原地改的字段 |
| 改大多数其他 `spec` 字段（如加一个新容器） | **apply 失败，被拒绝** | Pod 的 spec 大部分不可变 |

- **apply 既创建又更新：** 改文件再 apply 就是更新；但 Pod 的很多字段不可变，更新失败就删了重建。
- **实际工作中：** 不直接改 Pod，而是改 Deployment 的 Pod 模板，让它换一批新 Pod（第 5 部分）。
- **验证改动前：** `kubectl diff -f pod.kiada.yaml` 可以看会变什么；`kubectl explain pod.spec.containers` 看字段说明。

**出处：** KIA2 §5.2.2（apply 更新对象，部分字段不可变）、§5.2.1（containerPort 仅作说明）
