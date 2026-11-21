---
id: k8s-pv-pvc-beyond
node: p3.t03.pv-pvc-storageclass-dynamic-provisioning
type: qa
step: 3
tags: [拓展]
---
## Q
**存储新特性 · 2026 实践**｜拓展 · v1.34 / v1.36 GA

一块在线的盘要调整性能参数（比如 IOPS），以前通常要新建卷再迁移数据。近几个版本，Kubernetes 在存储上还有哪些已经 GA 的改进？

## A
| 特性 | 作用 | 版本 |
|---|---|---|
| **VolumeAttributesClass** | 通过一个类对象修改卷的参数（比如性能档位），不用重建卷、不停机 | v1.34 GA |
| **卷扩容失败的恢复** | 扩容 PVC 失败后，可以把请求的大小改回去，从失败中恢复，不再卡死 | v1.34 GA |
| **VolumeGroupSnapshot** | 给多个卷在同一时刻做一致的组快照 | v1.36 GA |

```yaml
# PVC 通过 volumeAttributesClassName 引用一个类，换类就换参数
spec:
  volumeAttributesClassName: gold
```

- **和 StorageClass 的区别：** StorageClass 在**创建**时决定供给方式；VolumeAttributesClass 在**之后**改卷的参数。
- **前提：** 底层的 CSI 驱动要支持。
- **用途：** 数据库在线调整磁盘性能；有多个卷的应用（数据加日志）要一致的备份。

**出处：** kubernetes.io 发布博客 v1.34（VolumeAttributesClass GA，KEP-3751；volume expansion failure recovery GA）、v1.36（VolumeGroupSnapshot GA）
