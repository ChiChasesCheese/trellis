---
id: k8s-selectors-annotations-exam
node: p2.t03.field-selectors-annotations
type: qa
step: 2
tags: [考点]
---
## Q
**YAML 报错**｜考点 · 必会

在 Pod 的 `metadata.annotations` 里写了 `revision: 3` 和 `managed: yes`，`kubectl apply` 报 `unable to decode yaml` 之类难懂的错误。原因是什么？怎么改？

## A
**原因：** annotation 的值必须是**字符串**。YAML 会把 `3` 解析成数字，把 `yes` 解析成布尔值，类型不对，API 解码失败。

```yaml
metadata:
  annotations:
    revision: "3"        # 数字要加引号
    managed: "yes"       # 像布尔的词（true/false/yes/no）也要加
    created-by: alice@example.com
```

| 情形 | 要不要引号 |
|---|---|
| 普通文本 | 不需要 |
| 数字、`true`/`false`、`yes`/`no` 等 | **必须** |
| JSON 或 YAML 片段、Base64 | 作为字符串放进去，可以很长 |

- **label 值同理：** label 值也必须是字符串（且有长度和字符限制）。
- **想按它过滤呢：** annotation 不能做 selector；需要筛选的信息放 label，说明性的放 annotation。
- **annotation 键的规则** 与 label 键相同。

<details class="pt" markdown="1"><summary>出处</summary>

KIA2 §7.5.2「Specifying annotations in the object manifest」（需加引号的警告）

</details>
