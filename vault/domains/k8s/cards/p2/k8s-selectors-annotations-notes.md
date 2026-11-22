---
id: k8s-selectors-annotations-notes
node: p2.t03.field-selectors-annotations
type: qa
step: 1
tags: [摘要]
---
## Q
**Field selector 与 annotation**｜摘要 · 必会

label selector 已经能过滤对象，为什么还有 field selector？annotation 和 label 又差在哪？

## A
| | label | annotation | field selector |
|---|---|---|---|
| 是什么 | 键值，用来**识别和分组** | 键值，存**说明性信息** | 按对象**自带字段**的值过滤 |
| 能用来过滤吗 | 能 | **不能** | 能 |
| 值的限制 | 值最多 63 字符，不能有空白 | 值可达 256 KB，任意字符（必须是字符串） | 字段由对象类型决定，`metadata.name`、`metadata.namespace` 总是支持 |

```bash
# 某个 node 上的 Pod
kubectl get pods --field-selector spec.nodeName=kind-worker
# 所有 namespace 里没在 Running 的 Pod
kubectl get pods -A --field-selector status.phase!=Running
# 只看告警事件
kubectl get events --field-selector type=Warning
kubectl annotate pod kiada created-by='alice@example.com'
```

- **field selector 能写什么：** 没有官方清单，试一下，不支持 kubectl 会报错；`kubectl explain` 看字段名。manifest 里也能用：node affinity 的 `matchFields` 按 node 的字段（如 `metadata.name`）匹配。
- **annotation 的典型用途：** 描述、联系人、Git 提交、构建时间；工具的开关；新特性在加正式字段之前先用 annotation 试，几个版本后才变成字段（旧 annotation 随后弃用）。
- **看 annotation：** `kubectl get` 不显示，用 `kubectl describe` 或 `-o yaml`。`kubectl.kubernetes.io/last-applied-configuration` 是 kubectl 自己加的。

<details class="pt" markdown="1"><summary>出处</summary>

KIA2 §7.4–7.5

</details>
