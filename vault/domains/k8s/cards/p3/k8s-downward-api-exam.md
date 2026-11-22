---
id: k8s-downward-api-exam
node: p3.t01.downward-api
type: qa
step: 2
tags: [考点]
---
## Q
**该用哪种注入**｜考点 · 必会

一个服务要：1）知道自己跑在哪个 node 上（写日志用）；2）把 Pod 的全部 labels 写成文件给 sidecar 读取；3）按内存 limit 设置 JVM 堆大小。分别怎么做？有一项不能照想的做，是哪个？

## A
| 需求 | 做法 | 能不能 |
|---|---|---|
| 所在 node 名 | env：`fieldRef: spec.nodeName` | 能（只支持 env） |
| 全部 labels 成文件 | `downwardAPI` volume，`fieldPath: metadata.labels` | 能（全部 labels 只支持文件，一行一个 `key="value"`） |
| 按内存 limit 设堆 | env：`resourceFieldRef: limits.memory`，`divisor: 1Mi` 之类 | 能 |
| 把 node 名写进**文件** | `spec.nodeName` 放进 downwardAPI volume | **不能**，这类字段只能进环境变量 |

- **想让 sidecar 在 label 变化后看到新值：** 文件会更新，环境变量不会（env 在容器启动时固定下来）。
- **在 volume 里引用资源字段：** 必须写 `containerName`；env 里默认就是所在容器。
- **别让 sidecar 去调 API server 查这些信息：** 那要额外的 RBAC 权限，Downward API 不需要。

<details class="pt" markdown="1"><summary>出处</summary>

KIA2 §8.4 表 8.5/8.6；§9.5.5（volume 里要写 containerName）

</details>
